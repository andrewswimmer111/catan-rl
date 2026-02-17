class Vertex:
    """
    Represents a vertex on the gameboard

    Attributes:
        x (int): The x-coordinate
        y (int): The y-coordinate
        ids (List<Tuple<Int>>): A set of ids, where an ID is a tile + offset
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.ids = []

    def add_id(self, id):
        self.ids.add(id)

    def get_first_id(self):
        return self.ids[0]


class VertexCollection:
    """
    Docstring for VertexCollection
    Represents a collection of vertices

    implements for loops
    implement getById
    implement adding
    """

    def __init__(self):
        self.collection: list[Vertex] = []

    def __iter__(self):
        return iter(self.collection)
    
    def __getitem__(self, index):
        return self.collection[index]
    
    def __len__(self):
        return len(self.collection)
    
    def append(self, vertex):
        self.collection.append(vertex)
    
    # Real methods
    def get_by_id(self, id):
        for vertex in self.collection:
            if id in vertex.ids:
                return vertex
        # throw exception: id does not exist for vertex


