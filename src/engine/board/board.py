from tile import Tile
from vertex import Vertex
from math import sqrt

class Board:
    """
    Represents the game board
    """

    def __init__(self):
        self.tiles: list[Tile] = []
        self.vertices: list[Vertex] = []
        self.edges = []

    def create_regular_board(self):
        self.tiles = self.createTiles()
        self.vertices = self.createVertices()


    def create_tiles(self, R=2):
        tiles = []
        for q in range(-R, R + 1):
            r_min = max(-R, -q - R)
            r_max = min(R, -q + R)
            for r in range(r_min, r_max + 1):
                tiles.append(Tile(q, r))
        return tiles
    
    def create_vertices(self):

        # Holds vertex coodinates -> vertex object
        created_vertices = {}

        HALF = 1 / 2
        SQRT3_OVER_2 = sqrt(3) / 2

        corner_offset = {
            "N":  (0,  1),
            "NE": ( SQRT3_OVER_2,  HALF),
            "SE": ( SQRT3_OVER_2, -HALF),
            "S":  (0, -1),
            "SW": (-SQRT3_OVER_2, -HALF),
            "NW": (-SQRT3_OVER_2,  HALF),
        }
        offsets = ["N", "NE", "SE", "S", "SW", "NW"]

        for tile in self.tiles:
            for i in offsets:
                vertex_coord = tile.getCartesianCoords() + corner_offset[i]

                if vertex_coord in created_vertices:
                    tile.addVertex(created_vertices[vertex_coord])
                else:
                    vertex = Vertex(vertex_coord[0], vertex_coord[1])
                    tile.addVertex(vertex)
                    created_vertices[vertex_coord] = vertex