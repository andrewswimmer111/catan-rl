from engine.board.tile import Tile, TileCollection
from engine.board.vertex import Vertex, VertexCollection
from engine.board.edge import Edge, EdgeCollection

from math import sqrt

class Board:
    """
    Represents the game board
    """

    def __init__(self):
        self.tiles: TileCollection = TileCollection()
        self.vertices: VertexCollection = VertexCollection()
        self.edges: EdgeCollection = EdgeCollection()

    def create_regular_board(self):
        self.create_tiles()
        self.create_vertices()
        self.create_edges()



    # ---- Helpers Below -----

    def create_tiles(self, R=2):
        for q in range(-R, R + 1):
            r_min = max(-R, -q - R)
            r_max = min(R, -q + R)
            for r in range(r_min, r_max + 1):
                self.tiles.append(Tile(q, r))
    

    def create_vertices(self):

        # Holds vertex coodinates -> vertex object
        created_vertices: dict[tuple[int, int], Vertex] = {}

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
            for i, offset in enumerate(offsets):
                vertex_coord = tile.get_cartesian_coords() + corner_offset[offset]
                vertex_id = (tile.get_axial_coords() + (i,))    # Example id for tile (0, 0) wilth offset S: (0, 0, 3)x

                if vertex_coord in created_vertices:
                    vertex = created_vertices[vertex_coord]
                else:
                    vertex = Vertex(vertex_coord[0], vertex_coord[1])
                    self.vertices.append(vertex)
                    created_vertices[vertex_coord] = vertex

                tile.assign_vertex(vertex, i)
                vertex.add_id(vertex_id)


    def create_edges(self):
        for tile in self.tiles:
            q, r = tile.get_axial_coords()
            if r <= 0:
                vertex = tile.vertices[0]

                self.edges.append(Edge(vertex, tile.vertices[1]))
                self.edges.append(Edge(vertex, tile.vertices[5]))
                
                if r >= -1:
                    tile_above = self.tiles.get_by_axial_coords(q, r - 1)

                    if tile_above is not None:
                        self.edges.append(Edge(vertex, tile_above.vertices[1]))

            if r == 0 and q % 2 == 0:

                self.edges.append(Edge(tile.vertices[1], tile.vertices[2]))
                self.edges.append(Edge(tile.vertices[5], tile.vertices[4]))

            if r >= 0:
                vertex = tile.vertices[3]

                self.edges.append(Edge(vertex, tile.vertices[2]))
                self.edges.append(Edge(vertex, tile.vertices[4]))

                if r <= 1:
                    tile_below = self.tiles.get_by_axial_coords(q, r + 1)
                    if tile_below is not None:
                        self.edges.append(Edge(vertex, tile_below.vertices[4]))
