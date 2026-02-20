import collections
import pytest

from engine.board.board import Board
from engine.board.components import Resource


@pytest.fixture
def board():
    b = Board()
    b.create_regular_board()
    b.setup_regular_board()
    return b


def test_resource_distribution_counts(board):
    """
    Ensure resource counts match the standard Catan distribution:
      WOOD x4, SHEEP x4, WHEAT x4, BRICK x3, ORE x3, desert (None) x1
    """
    resources = [t.resource for t in board.tiles]

    counts = collections.Counter(resources)

    assert counts[Resource.WOOD] == 4, f"WOOD count wrong: {counts[Resource.WOOD]}"
    assert counts[Resource.SHEEP] == 4, f"SHEEP count wrong: {counts[Resource.SHEEP]}"
    assert counts[Resource.WHEAT] == 4, f"WHEAT count wrong: {counts[Resource.WHEAT]}"
    assert counts[Resource.BRICK] == 3, f"BRICK count wrong: {counts[Resource.BRICK]}"
    assert counts[Resource.ORE] == 3, f"ORE count wrong: {counts[Resource.ORE]}"
    assert counts[None] == 1, f"Desert (None) count wrong: {counts[None]}"

    # total tiles sanity
    assert sum(counts.values()) == len(board.tiles) == 19


def test_probabilities_assigned_and_multiset_matches(board):
    """
    There are 18 number tokens in the official Catan set (desert gets no number).
    Verify:
      - exactly 18 tiles have a non-None probability
      - the multiset of assigned probabilities equals the official list
    """
    official = [5, 2, 6, 3, 8, 10, 9, 12, 11, 4, 8, 10, 9, 4, 5, 6, 3, 11]

    probs = []
    for t in board.tiles:
        p = t.number
        # treat 0 or falsy explicitly as a valid value only if not None
        if p is not None:
            probs.append(p)

    assert len(probs) == len(official), f"expected {len(official)} assigned probabilities, got {len(probs)}"

    # Compare multisets (order doesn't matter because desert may shift placement)
    assert collections.Counter(probs) == collections.Counter(official), (
        f"Assigned probability multiset does not match official tokens.\n"
        f"Assigned: {collections.Counter(probs)}\nExpected: {collections.Counter(official)}"
    )


def test_desert_has_no_probability(board):
    """
    Ensure the single desert tile has no probability token assigned.
    """
    desert_tiles = [t for t in board.tiles if t.resource is None]
    assert len(desert_tiles) == 1, "expected exactly one desert tile"

    desert_prob = desert_tiles[0].number
    assert desert_prob is None, "desert tile should not have a probability/token assigned"