from engine.resources.resources import Resource
from math import sqrt


class Vertex:
    """
    Represents a vertex on the gameboard

    Attributes:
        x (int): The x-coordinate
        y (int): The y-coordinate
        ids (List<Tuple<Int>>): A list of ids, where an ID is a tile + offset
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ids = []
        self.tiles = []

    def add_id(self, id):
        self.ids.append(id)

    def get_first_id(self):
        return self.ids[0]
    
    def add_tile(self, tile):
        self.tiles.append(tile)


class Edge:
    """
    Represents an edge between two vertices
    """

    def __init__(self, v1, v2):
        self.v1 = v1
        self.v2 = v2


class Tile:
    """
    Represents a resource tile in the gameboard

    Attributes:
        q (int): The q-axial-coordinate.
        r (int): The r-axial-coordinate.
        resource (Resource): The resource type.
        vertices (List<Vertex>): The adjacent vertices, in order by offset. vertices[0] = vertex 0 with offest north/ 
    """

    def __init__(self, q, r):
        self.q: int = q
        self.r: int = r
        self.resource: Resource = None
        self.number: int = None
        self.vertices = [None] * 6

    def assign_vertex(self, vertex_obj, offset):
        # check offest. Throw error if not 1-6
        self.vertices[offset] = vertex_obj

    def set_resource(self, resource):
        self.resource = resource

    def set_number(self, number):
        self.number = number

    def get_cartesian_coords(self):
        center_x = sqrt(3) * (self.q + self.r/2)
        center_y = 3/2 * self.r
        return (center_x, center_y)

    def get_axial_coords(self):
        return (self.q, self.r)
