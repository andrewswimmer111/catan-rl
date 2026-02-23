from engine.board.collections import VertexCollection, EdgeCollection, TileCollection
from engine.board.components import Vertex, Edge, Tile
from engine.resources.resources import Resource

from utility.helpers import elementwise_add_tuples, quantize_point

from math import sqrt
import random


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

    def setup_regular_board(self):
        self.assign_tile_resources()
        self.assign_tile_probabilities()

    def get_tiles_with_number(self, number: int) -> list[Tile]:
        res = []
        for tile in self.tiles:
            if tile.number == number:
                res.append(tile)
        return res

    # -------- Helpers Below ---------

    # -- Board setup

    def assign_tile_resources(self):
        self.check_tiles_created()

        resources = (
            [Resource.WOOD] * 4 +
            [Resource.SHEEP] * 4 +
            [Resource.WHEAT] * 4 +
            [Resource.BRICK] * 3 +
            [Resource.ORE] * 3 +
            [None] * 1  # desert
        )
        random.shuffle(resources)
        for tile, resource in zip(self.tiles, resources):
            tile.set_resource(resource)


    def assign_tile_probabilities(self):
        self.check_tiles_created()
        self.check_tiles_have_resources()

        tile_map = {
            tile.get_axial_coords(): tile for tile in self.tiles
        }
        spiral_coords = self._get_spiral_coords()
        prob_index = 0
        
        for coord in spiral_coords:
            tile = tile_map.get(coord)
            if tile is None:
                raise Warning("Spiral coord contained tile that does not exist")
            
            if tile.resource is not None:
                tile.set_number(PROBABILITIES[prob_index])
                prob_index += 1


    def _hex_ring(self, center, radius):
        if radius == 0:
            return [center]

        results = []

        q = center[0] + HEX_DIRECTIONS[4][0] * radius
        r = center[1] + HEX_DIRECTIONS[4][1] * radius

        for direction in range(6):
            dq, dr = HEX_DIRECTIONS[direction]
            for _ in range(radius):
                results.append((q, r))
                q += dq
                r += dr

        return results
    
    def _get_spiral_coords(self):
        coords = []
        for radius in reversed(range(0, 3)):  # radius, radius-1, ..., 1, 0
            coords.extend(self._hex_ring((0, 0), radius))
        return coords


    # -- Board creation --

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

        for tile in self.tiles:
            for i, offset in enumerate(OFFSETS):
                raw_coord = elementwise_add_tuples(
                    tile.get_cartesian_coords(), CORNER_OFFSETS[offset])
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
                vertex.add_tile(tile)

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
                edge = Edge(v1, v2)

                self.edges.append(edge)
                v1.add_edge(edge)
                v2.add_edge(edge)


    def check_tiles_created(self):
        if len(self.tiles) == 0:
            raise ValueError("Tiles must be created.")

    def check_vertices_created(self):
        if len(self.vertices) == 0:
            raise ValueError("Vertices must be created.")
        
    def check_tiles_have_resources(self):
        none_counter = 0
        for tile in self.tiles:
            if tile.resource is None:
                none_counter += 1
        if none_counter != 1:
            raise ValueError("Tiles must have exactly one desert (None resource).")
        

# ------- Constants ---------

HEX_DIRECTIONS = [
        (1, 0),
        (1, -1),
        (0, -1),
        (-1, 0),
        (-1, 1),
        (0, 1),
]

HALF = 1 / 2
SQRT3_OVER_2 = sqrt(3) / 2

CORNER_OFFSETS = {
    "N":  (0,  1),
    "NE": (SQRT3_OVER_2,  HALF),
    "SE": (SQRT3_OVER_2, -HALF),
    "S":  (0, -1),
    "SW": (-SQRT3_OVER_2, -HALF),
    "NW": (-SQRT3_OVER_2,  HALF),
}
OFFSETS = ["N", "NE", "SE", "S", "SW", "NW"]

PROBABILITIES = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]
