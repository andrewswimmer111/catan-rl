from engine.board.board import Board
from engine.board.components import Vertex, Edge

def can_place_building(board, vertex: Vertex, player):
    """
    Validates that a building can be placed on the vertex

    Rules to placing a building on a vertex:
    - Vertex must exist
    - Vertex must be unoccupied
    - Vertex must be at least 2 edges away from any other building
    - Vertex must be connected to by a road owned by the same player
    """
    
    
    if not _check_vertex_exists(board, vertex):
        raise ValueError("The referenced vertex does not exist on the board.")
    
    if vertex.has_building():
        return False
    
    if _check_adjacent_vertices_have_building(vertex):
        return False
    
    if not _check_vertex_connected_to_valid_road(vertex, player):
        return False
    
    return True
    

def can_place_road(board, edge: Edge, player):
    """
    Validates that a road can be build on the edge provided

    Rules to place a road on an edge:
    - Edge must exist on the board
    - Edge must be unoccupied
    - Edge must be connected to a building owned by the same player OR
    - Edge must be connected to a road owned by the same player
    """

    if not _check_edge_exists(board, edge):
        raise ValueError("The referenced edge does not exist on the board.")
    
    if edge.has_road():
        return False
    
    building_connection = _check_edge_connected_to_valid_building(edge, player)
    road_connection = _check_edge_connected_to_valid_road(edge, player)
    
    if not building_connection and not road_connection:
        return False
    
    return True
        

# ---- Building logic ----
def _check_adjacent_vertices_have_building(vertex: Vertex):
    for edge in vertex.edges:
        adjacent_v = edge.get_other_vertex(vertex)
        if adjacent_v.has_building():
            return True
    return False

def _check_vertex_connected_to_valid_road(vertex: Vertex, player):
    for edge in vertex.edges:
        if edge.has_road() and edge.get_road_player() == player:
            return True
    return False

def _check_vertex_exists(board: Board, vertex: Vertex):
    vid = vertex.get_first_id()
    if board.vertices.exists_by_id(vid):
        return True
    else:
        return False
    

# ---- Road logic ---- 
def _check_edge_connected_to_valid_road(edge: Edge, player) -> bool:
    """
    Return True if any edge adjacent to the given `edge` is owned by `player`.

    Adjacent edges are those that share a vertex with `edge`, excluding `edge` itself.
    """
    for vertex in edge.get_vertices():
        for adjacent in vertex.edges:
            if adjacent is edge:
                continue
            if adjacent.has_road() and adjacent.get_road_player() == player:
                return True
    return False
        

def _check_edge_connected_to_valid_building(edge: Edge, player):
    for vertex in edge.get_vertices():
        if vertex.has_building() and vertex.get_building_player() == player:
            return True
    return False

def _check_edge_exists(board: Board, edge: Edge):
    if board.edges.exists_by_vertices(edge.v1, edge.v2):
        return True
    else:
        raise ValueError("The referenced edge does not exist on the board.")
