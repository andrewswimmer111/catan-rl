import pytest

from engine.board.board import Board
from engine.board.components import Vertex, Edge
from engine.board.buildables import Building, Road, City, Settlement

from engine.game_logic import rules


@pytest.fixture
def empty_board():
    b = Board()
    b.create_regular_board()
    b.setup_regular_board()
    return b


@pytest.fixture
def building_factory():
    def _create(player_id=None, vertex=None):
        return Building(player_id, vertex)
    return _create


@pytest.fixture
def road_factory():
    def _create(player_id=None, edge=None):
        return Road(player_id, edge)
    return _create

@pytest.fixture
def city_factory():
    def _create(player_id=None, vertex=None):
        return City(player_id, vertex)
    return _create

@pytest.fixture
def settlement_factory():
    def _create(player_id=None, vertex=None):
        return Settlement(player_id, vertex)
    return _create

def test_non_existent_throws_error(empty_board):
    fake_v1 = Vertex(-1, -1)
    fake_v2 = Vertex(-2, -2)
    fake_edge = Edge(fake_v1, fake_v2)

    with pytest.raises(ValueError, match="does not exist"):
        rules.can_place_settlement(empty_board, fake_v1, "1")

    with pytest.raises(ValueError, match="does not exist"):
        rules.can_place_road(empty_board, fake_edge, "1")


def test_placement_on_occupied_space_returns_false(empty_board):
    r1, b1 = Road(None, None), Building(None, None)
    v, e = empty_board.vertices[0], empty_board.edges[0]

    v.set_building(b1)
    e.set_road(r1)

    assert rules.can_place_settlement(empty_board, v, "1") is False, "Building cannot be placed on occupied vertex"
    assert rules.can_place_road(empty_board, e, "1") is False, "Road cannot be placed on occupied edge"


def test_building_placement_without_road_returns_false(empty_board):
    v = empty_board.vertices[0]
    assert rules.can_place_settlement(empty_board, v, "1") is False, "Building cannot be placed without a connecting road"


def test_building_placement_with_neighbor_building_returns_false(empty_board, building_factory, road_factory):
    # pick two vertices that share an edge
    v1_id = (0, 0, 1)
    v2_id = (0, 0, 2)

    v1 = empty_board.vertices.get_by_id(v1_id)
    v2 = empty_board.vertices.get_by_id(v2_id)
    assert v1 is not None and v2 is not None, "Test assumes those vertex ids exist"

    e = empty_board.edges.get_by_vertices(v1, v2)
    assert e is not None, "Test assumes there is an edge between v1 and v2"

    # place a building on v1 owned by player "1"
    b = building_factory("1", v1)
    v1.set_building(b)

    # place an unrelated road on the connecting edge owned by player "2" (so the player "2" attempts to place nearby)
    r = road_factory("2", e)
    e.set_road(r)

    # player "2" should not be allowed to place a building on v2 because adjacent building exists
    assert rules.can_place_settlement(empty_board, v2, "2") is False


def test_building_placement_with_road_returns_true(empty_board, building_factory, road_factory):
    # choose a vertex and an adjacent edge, then give that edge a road for player "1"
    # find a vertex that has at least one incident edge
    v = next((vv for vv in empty_board.vertices if len(vv.edges) > 0), None)
    assert v is not None, "board must have a vertex with edges"

    # pick one adjacent edge
    adj_edge = v.edges[0]
    # ensure no building currently at v
    if hasattr(v, "set_building"):
        v.set_building(None)

    # give the adjacent edge a road for player "1"
    r = road_factory("1", adj_edge)
    adj_edge.set_road(r)

    # now the player with the road should be able to place a building at v (assuming distance rule ok)
    assert rules.can_place_settlement(empty_board, v, "1") is True


def test_road_placement_without_linkage_returns_false(empty_board):
    # pick an edge that has no adjacent roads or buildings (new board should have none)
    e = next((ee for ee in empty_board.edges if not ee.has_road()), None)
    assert e is not None

    # ensure neither adjacent vertices have player's building and adjacent edges have player's road
    assert rules.can_place_road(empty_board, e, "1") is False


def test_road_placement_with_building_returns_true(empty_board, building_factory, road_factory):
    # pick a vertex and one of its edges
    v = next((vv for vv in empty_board.vertices if len(vv.edges) > 0), None)
    assert v is not None
    e = v.edges[0]

    # place a building for player "1" on that vertex
    b = building_factory("1", v)
    v.set_building(b)

    # Now placing a road on the adjacent edge for player "1" should be allowed
    assert rules.can_place_road(empty_board, e, "1") is True


def test_road_placement_with_road_returns_true(empty_board, road_factory):
    # pick an edge, give one of its neighboring edges a road for player "1"
    e = next((ee for ee in empty_board.edges), None)
    assert e is not None

    # find an adjacent edge through a shared vertex
    adj = None
    for vertex in e.get_vertices():
        for candidate in vertex.edges:
            if candidate is not e:
                adj = candidate
                break
        if adj:
            break
    assert adj is not None, "Need an adjacent edge for test"

    # give adjacent edge a road owned by player "1"
    r = road_factory("1", adj)
    adj.set_road(r)

    # now player "1" should be able to place a road on e
    assert rules.can_place_road(empty_board, e, "1") is True

def test_upgrade_empty_vertex_returns_false(empty_board):
    v = empty_board.vertices[0]
    assert(rules.can_upgrade_settlement(empty_board, v, "1") is False)

def test_upgrade_vertex_with_city_returns_false(empty_board, city_factory):
    v = empty_board.vertices[0]
    b = city_factory("1", v)
    v.set_building(v)
    assert(rules.can_upgrade_settlement(empty_board, v, "1") is False)

def test_upgrade_vertex_with_wrong_player_returns_false(empty_board, settlement_factory):
    v = empty_board.vertices[0]
    s = settlement_factory("1", v)
    v.set_building(s)
    assert(rules.can_upgrade_settlement(empty_board, v, "2") is False)


def test_upgrade_vertex_correct_returns_true(empty_board, settlement_factory):
    v = empty_board.vertices[0]
    s = settlement_factory("1", v)
    v.set_building(s)
    assert(rules.can_upgrade_settlement(empty_board, v, "1") is True)
