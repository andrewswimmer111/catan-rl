import pytest

from engine.board.board import Board

@pytest.fixture
def regular_board():
    b = Board()
    b.create_regular_board()
    return b

def test_board_creation_throws_no_exceptions(regular_board):
    assert(True)


