from enum import Enum
from collections import Counter

class Resource(Enum):
    WOOD = "wood"
    BRICK = "brick"
    WHEAT = "wheat"
    SHEEP = "sheep"
    ORE = "ore"


class ResourcePool:
    def __init__(self, initial=None):
        self.counts = Counter(initial or {})  # Resource -> int

    def can_withdraw(self, resource: Resource, amount: int) -> bool:
        return self.counts[resource] >= amount

    def withdraw(self, resource: Resource, amount: int) -> None:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        if not self.can_withdraw(resource, amount):
            raise ValueError("not enough resources")
        self.counts[resource] -= amount

    def add(self, resource: Resource, amount: int) -> None:
        if amount < 0:
            raise ValueError("amount must be non-negative")
        self.counts[resource] += amount


class Bank(ResourcePool):
    pass

class ResourceHand(ResourcePool):
    pass