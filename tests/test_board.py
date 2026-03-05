"""Tests for board.py: board representation and generation."""

from rosencrantz.board import Board, generate_board


def test_neighbors_corner():
    board = Board(size=4, total_mines=0)
    assert len(board.neighbors(0, 0)) == 3


def test_neighbors_edge():
    board = Board(size=4, total_mines=0)
    assert len(board.neighbors(0, 1)) == 5


def test_neighbors_interior():
    board = Board(size=4, total_mines=0)
    assert len(board.neighbors(1, 1)) == 8


def test_neighbors_excludes_self():
    board = Board(size=3, total_mines=0)
    assert (1, 1) not in board.neighbors(1, 1)


def test_generate_board_mine_count():
    board = generate_board(size=5, mines=4, seed=42)
    mine_count = sum(
        1 for r in range(5) for c in range(5)
        if board.cells[r][c].is_mine
    )
    assert mine_count == 4


def test_generate_board_seed_reproducibility():
    b1 = generate_board(size=5, mines=4, seed=42)
    b2 = generate_board(size=5, mines=4, seed=42)
    for r in range(5):
        for c in range(5):
            assert b1.cells[r][c].is_mine == b2.cells[r][c].is_mine
            assert b1.cells[r][c].is_revealed == b2.cells[r][c].is_revealed


def test_generate_board_adjacent_mines_correct():
    board = generate_board(size=5, mines=4, seed=42)
    for r in range(5):
        for c in range(5):
            cell = board.cells[r][c]
            if cell.is_mine:
                continue
            actual = sum(
                1 for nr, nc in board.neighbors(r, c)
                if board.cells[nr][nc].is_mine
            )
            assert cell.adjacent_mines == actual, (
                f"Cell ({r},{c}): adj_mines={cell.adjacent_mines}, actual={actual}"
            )


def test_hidden_revealed_partition():
    board = generate_board(size=5, mines=4, seed=42)
    hidden = board.hidden_cells
    revealed = board.revealed_cells
    assert len(hidden) + len(revealed) == 25


def test_mines_remaining():
    board = Board(size=3, total_mines=2)
    board.cells[0][0].is_mine = True
    board.cells[0][0].is_revealed = True
    board.cells[1][1].is_mine = True
    assert board.mines_remaining == 1


def test_to_grid_string_format():
    board = generate_board(size=3, mines=1, seed=42)
    grid = board.to_grid_string()
    lines = grid.strip().split("\n")
    assert len(lines) == 3


def test_to_formal_string_contains_info():
    board = generate_board(size=3, mines=1, seed=42)
    formal = board.to_formal_string()
    assert "Revealed:" in formal
    assert "Hidden:" in formal
    assert "Mines remaining:" in formal
