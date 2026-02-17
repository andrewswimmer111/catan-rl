from vertex import Vertex

class Edge:
    """
    Represents an edge between two vertices
    """

    def __init__(self, v1, v2):
        self.vertices: list[Vertex] = [v1, v2]