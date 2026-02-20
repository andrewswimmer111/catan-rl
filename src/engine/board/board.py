from engine.board.collections import VertexCollection, EdgeCollection, TileCollection
from engine.board.components import Vertex, Edge, Tile

from utility.helpers import elementwise_add_tuples, quantize_point

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

        self.check_tiles_created()

        # Holds vertex coodinates -> vertex object
        created_vertices: dict[tuple[int, int], Vertex] = {}

        HALF = 1 / 2
        SQRT3_OVER_2 = sqrt(3) / 2

        corner_offset = {
            "N":  (0,  1),
            "NE": (SQRT3_OVER_2,  HALF),
            "SE": (SQRT3_OVER_2, -HALF),
            "S":  (0, -1),
            "SW": (-SQRT3_OVER_2, -HALF),
            "NW": (-SQRT3_OVER_2,  HALF),
        }
        offsets = ["N", "NE", "SE", "S", "SW", "NW"]

        for tile in self.tiles:
            for i, offset in enumerate(offsets):
                raw_coord = elementwise_add_tuples(
                    tile.get_cartesian_coords(), corner_offset[offset])
                vertex_coord = quantize_point(raw_coord)
                # Example id for tile (0, 0) wilth offset S: (0, 0, 3)
                vertex_id = (tile.get_axial_coords() + (i,))

                if vertex_coord in created_vertices:
                    vertex = created_vertices[vertex_coord]
                else:
                    vertex = Vertex(vertex_coord[0], vertex_coord[1])
                    self.vertices.append(vertex)
                    created_vertices[vertex_coord] = vertex

                tile.assign_vertex(vertex, i)
                vertex.add_id(vertex_id)

    def create_edges(self):
        """
        Create all unique edges on the board.

        For each hex tile we consider the 6 edges between consecutive vertices:
        (0,1), (1,2), (2,3), (3,4), (4,5), (5,0)

        We deduplicate using the vertex object's id() (or you can use
        a unique vertex attribute if available) so a shared edge between two
        neighboring tiles is only created once.
        """

        self.check_tiles_created()
        self.check_vertices_created()

        seen = set()  # holds tuples (min_id, max_id) for created edges

        for tile in self.tiles:
            verts = tile.vertices

            for i in range(6):
                v1 = verts[i]
                v2 = verts[(i + 1) % 6]

                key = frozenset((v1, v2))   # works because sets are unordered

                if key in seen:
                    continue

                seen.add(key)
                self.edges.append(Edge(v1, v2))


    def check_tiles_created(self):
        if len(self.tiles) == 0:
            raise ValueError("Tiles must be created.")

    def check_vertices_created(self):
        if len(self.vertices) == 0:
            raise ValueError("Vertices must be created.")