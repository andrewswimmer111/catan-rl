import pytest

from engine.board.board import Board

@pytest.fixture
def regular_board():
    b = Board()
    b.create_regular_board()
    return b

def test_board_creation_throws_no_exceptions(regular_board):
    assert(True)

def test_correct_num_tiles(regular_board):
    assert(len(regular_board.tiles) == 19)

def test_correct_num_vertices(regular_board):
    assert(len(regular_board.vertices) == 54)

def test_correct_num_edges(regular_board):
    assert(len(regular_board.edges) == 72)