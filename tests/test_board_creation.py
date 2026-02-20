import pytest

from engine.board.board import Board
from engine.board.components import Vertex, Edge, Tile


@pytest.fixture
def regular_board():
    b = Board()
    b.create_regular_board()
    return b


def test_board_creation_throws_no_exceptions(regular_board):
    assert True, "Board creation throws exception"


def test_correct_num_tiles(regular_board):
    assert len(regular_board.tiles) == 19, "Incorrect number of tiles created"


def test_correct_num_vertices(regular_board):
    assert len(regular_board.vertices) == 54, "Incorrect number of vertices created"


def test_correct_num_edges(regular_board):
    assert len(regular_board.edges) == 72, "Incorrect number of edges created"


# ---- Additional sanity checks below ----


def test_each_tile_has_six_vertices(regular_board):
    for tile in regular_board.tiles:
        verts = tile.vertices
        assert len(verts) == 6, f"Tile {getattr(tile, 'get_axial_coords', lambda: '?')()} does not have 6 vertices"


def test_tile_axial_coords_unique(regular_board):
    axial_coords = [tuple(tile.get_axial_coords()) for tile in regular_board.tiles]
    assert len(axial_coords) == len(set(axial_coords)), "Duplicate tile axial coordinates found"


def test_vertices_referenced_by_tiles_are_board_vertices(regular_board):
    board_vertices_set = set(regular_board.vertices)
    for tile in regular_board.tiles:
        for v in tile.vertices:
            assert v in board_vertices_set, "A tile references a vertex not present in board.vertices"


def test_each_consecutive_tile_vertex_pair_has_an_edge(regular_board):
    """
    For every tile, the six consecutive vertex pairs (0-1,1-2,...,5-0) should
    correspond to an Edge in the board.edges collection.
    """
    # Build a set of undirected vertex-pair keys present in edges
    edge_keys = set()
    for e in regular_board.edges:
        v1, v2 = e.v1, e.v2
        edge_keys.add(frozenset((v1, v2)))

    for tile in regular_board.tiles:
        verts = tile.vertices
        for i in range(6):
            v1 = verts[i]
            v2 = verts[(i + 1) % 6]
            assert frozenset((v1, v2)) in edge_keys, "Missing edge for tile vertex pair"


def test_edges_connect_board_vertices_and_no_duplicates(regular_board):
    """
    Ensure every edge connects two Vertex instances that belong to the board,
    and that there are no duplicated edges.
    """
    board_vertices_set = set(regular_board.vertices)
    seen_keys = set()
    for e in regular_board.edges:
        v1, v2 = e.v1, e.v2

        assert isinstance(v1, Vertex) and isinstance(v2, Vertex), "Edge endpoints are not Vertex instances"
        assert v1 in board_vertices_set and v2 in board_vertices_set, "Edge endpoint not in board.vertices"

        key = frozenset((v1, v2))
        assert key not in seen_keys, "Duplicate edge detected"
        seen_keys.add(key)