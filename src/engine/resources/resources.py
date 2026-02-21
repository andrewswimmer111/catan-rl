from enum import Enum

class Resource(Enum):
    WOOD = "wood"
    BRICK = "brick"
    WHEAT = "wheat"
    SHEEP = "sheep"
    ORE = "ore"


class ResourceStack():

    def __init__(self, resource: Resource, number: int):
        self.resource = resource
        self.number = number

    def check_withdrawal_amount(self, amount):
        if self.number >= amount:
            return True
        return False
    
    def withdraw(self, amount):
        if self.check_withdrawal_amount():
            self.number -= amount
            # assign amount
        else:
            print("Invalid amount of resources left")

    def add(self, amount):
        self.number += amount


class ResourceDistributer():
    # distributes the correct amount of resources
    # maybe identifies how many 
    pass