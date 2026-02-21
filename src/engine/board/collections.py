from typing import TypeVar, Callable, Optional, Generic
from engine.board.components import Vertex, Tile, Edge

T = TypeVar("T")


class Collection(Generic[T]):
    """
    Generic collection providing common list-like / query behaviour.

    Implemented using a Python list
    """

    def __init__(self):
        self.collection: list[T] = []

    def __iter__(self):
        return iter(self.collection)

    def __getitem__(self, index):
        return self.collection[index]

    def __len__(self):
        return len(self.collection)

    def append(self, tile):
        self.collection.append(tile)

    # Real logic:
    def _find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Return first item matching predicate, or None.
        """
        for item in self.collection:
            if predicate(item):
                return item
        return None

    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        return self._find(predicate)

    def get(self, predicate: Callable[[T], bool]) -> T:
        item = self._find(predicate)
        if item is None:
            raise KeyError("Item not found.")
        return item

    def exists(self, predicate: Callable[[T], bool]) -> bool:
        return self._find(predicate) is not None


class VertexCollection(Collection[Vertex]):

    def find_by_id(self, id):
        return self.find(lambda v: id in v.ids)

    def get_by_id(self, id):
        return self.get(lambda v: id in v.ids)

    def exists_by_id(self, id):
        return self.exists(lambda v: id in v.ids)


class TileCollection(Collection[Tile]):

    def find_by_axial_coords(self, q, r):
        return self.find(lambda t: t.get_axial_coords() == (q, r))

    def get_by_axial_coords(self, q, r):
        return self.get(lambda t: t.get_axial_coords() == (q, r))

    def exists_by_axial_coord(self, q, r):
        return self.exists(lambda t: t.get_axial_coords() == (q, r))


class EdgeCollection(Collection[Edge]):

    def _edge_key(self, v1, v2):
        """Canonical, order-independent key for an undirected edge."""
        return frozenset((v1, v2))

    def exists_by_vertices(self, v1, v2) -> bool:
        key = self._edge_key(v1, v2)
        return self.exists(lambda e: self._edge_key(e.v1, e.v2) == key)

    def find_by_vertices(self, v1, v2) -> Optional[Edge]:
        key = self._edge_key(v1, v2)
        return self.find(lambda e: self._edge_key(e.v1, e.v2) == key)

    def get_by_vertices(self, v1, v2) -> Edge:
        key = self._edge_key(v1, v2)
        return self.get(lambda e: self._edge_key(e.v1, e.v2) == key)
