from engine.board.board import Board
from engine.board.components import Vertex, Edge

def can_place_building(board, vertex, player):
    """
    Validates that a building can be placed on the vertex

    Rules to placing a building:
    - Must be connected to by a road
    - Must be at least 2 edges away from any other building
    """
    
    _validate_vertex_exists()
    


def can_place_road(board, vertex, player):
    pass

def validate_house_connected(board, vertex, plaeer):
    pass

def validate_road_connected():
    pass


def _validate_vertex_exists(board: Board, vertex: Vertex):
    vid = vertex.get_first_id()
    if board.vertices.exists_by_id(vid):
        return True
    else:
        raise ValueError("The referenced vertex does not exist on the board.")
    
def _validate_edge_exists(board: Board, edge: Edge):
    if board.edges.exists_by_vertices(edge.v1, edge.v2):
        return True
    else:
        raise ValueError("The referenced edge does not exist on the board.")
