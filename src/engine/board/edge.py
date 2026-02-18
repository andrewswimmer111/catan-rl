from engine.board.vertex import Vertex

class Edge:
    """
    Represents an edge between two vertices
    """

    def __init__(self, v1, v2):
        self.vertices: list[Vertex] = [v1, v2]

class EdgeCollection:
    """
    Docstring for EdgeCollection
    """

    def __init__(self):
        self.collection: list[Edge] = []

    def __iter__(self):
        return iter(self.collection)
    
    def __getitem__(self, index):
        return self.collection[index]
    
    def __len__(self):
        return len(self.collection)
    
    def append(self, tile):
        self.collection.append(tile)