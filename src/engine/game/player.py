from engine.resources.resources import ResourceHand

class Player():

    def __init__(self, player_id: int):
        self.id = player_id
        self.vp = 0
        self.resources = ResourceHand()
        self.roads = []
        self.buildings = []
        
    def add_resource(self, resource, amount):
        self.resources.add(resource, amount)


