from engine.resources.resources import Resource
from math import sqrt

class Tile:
    """
    Represents a resource tile in the gameboard

    Attributes:
        q (int): The q-axial-coordinate.
        r (int): The r-axial-coordinate.
        resource (Resource): The resource type.
        vertices (List<Vertex>): The adjacent vertices
    """
    def __init__(self, q, r):
        self.q: int = q
        self.r: int = r
        self.resource: Resource = None
        self.number: int = None
        self.vertices = []

    def add_vertex(self, vertex):
        self.vertices.append(vertex)
    
    def set_vertices(self, vertices):
        self.vertices = vertices

    def set_resource(self, resource):
        self.resource = resource

    def set_number(self, number):
        self.number = number

    def get_cartesian_coords(self):
        center_x = sqrt(3) * (self.q + self.r/2)
        center_y = 3/2 * self.r
        return (center_x, center_y)