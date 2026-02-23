class Building:

    vp = 0
    collection_amount = 0
    
    def __init__(self, player, vertex):
        self.player = player
        self.vertex = vertex


class Settlement(Building):
    vp = 1
    collection_amount = 1


class City(Building):
    vp = 2
    collection_amount = 2


class Road:
    def __init__(self, player, edge):
        self.player = player
        self.edge = edge
