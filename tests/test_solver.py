"""Tests for solver.py: ground truth computation correctness."""

import pytest

from rosencrantz.board import Board
from rosencrantz.solver import GroundTruth, SolverTimeout, solve


def _make_board(
    size: int,
    mines: int,
    mine_positions: set[tuple[int, int]],
    revealed_positions: set[tuple[int, int]],
) -> Board:
    """Construct a board with known mine placements and revealed cells."""
    board = Board(size=size, total_mines=mines)
    for r, c in mine_positions:
        board.cells[r][c].is_mine = True
    for r in range(size):
        for c in range(size):
            if board.cells[r][c].is_mine:
                continue
            count = sum(
                1 for nr, nc in board.neighbors(r, c)
                if board.cells[nr][nc].is_mine
            )
            board.cells[r][c].adjacent_mines = count
    for r, c in revealed_positions:
        board.cells[r][c].is_revealed = True
    return board


def test_solve_fully_determined():
    """3x3 board with 1 mine at (0,0), all others revealed: |C(B)|=1, P=1.0."""
    mine_pos = {(0, 0)}
    revealed = {(r, c) for r in range(3) for c in range(3)} - mine_pos
    board = _make_board(3, 1, mine_pos, revealed)
    gt = solve(board)
    assert gt.valid_configurations == 1
    assert gt.probabilities[(0, 0)] == 1.0


def test_solve_determined_safe_and_mine():
    """Board where constraints fully determine all hidden cells."""
    # 3x3, 1 mine at (0,1). Reveal (0,0), (0,2), (1,0), (1,1), (1,2).
    # All revealed cells' constraints force (0,1) to be the mine.
    mine_pos = {(0, 1)}
    revealed = {(0, 0), (0, 2), (1, 0), (1, 1), (1, 2)}
    board = _make_board(3, 1, mine_pos, revealed)
    gt = solve(board)
    assert gt.valid_configurations == 1
    assert gt.probabilities[(0, 1)] == 1.0
    assert gt.probabilities[(2, 0)] == 0.0
    assert gt.probabilities[(2, 1)] == 0.0
    assert gt.probabilities[(2, 2)] == 0.0


def test_solve_simple_ambiguous():
    """3x3, 1 mine, reveal (0,0)=0, (1,1)=1, (0,2)=0.
    Constraints force mine to one of bottom row cells: each has P=1/3.
    """
    mine_pos = {(2, 1)}
    revealed = {(0, 0), (0, 2), (1, 1)}
    board = _make_board(3, 1, mine_pos, revealed)
    gt = solve(board)
    assert gt.valid_configurations == 3
    # Top row neighbors of (0,0) and (0,2) showing 0 => (0,1), (1,0), (1,2) are safe
    assert gt.probabilities[(0, 1)] == 0.0
    assert gt.probabilities[(1, 0)] == 0.0
    assert gt.probabilities[(1, 2)] == 0.0
    # Bottom row: each has P=1/3
    for pos in [(2, 0), (2, 1), (2, 2)]:
        assert abs(gt.probabilities[pos] - 1 / 3) < 1e-9


def test_solve_symmetric_board():
    """4x4 board symmetric about vertical midline: mirror cells have equal P."""
    mine_pos = {(0, 0), (0, 3)}
    revealed = {(1, 1), (1, 2)}
    board = _make_board(4, 2, mine_pos, revealed)
    gt = solve(board)
    # Symmetric pairs should have equal probabilities
    assert abs(gt.probabilities[(0, 0)] - gt.probabilities[(0, 3)]) < 1e-9
    assert abs(gt.probabilities[(0, 1)] - gt.probabilities[(0, 2)]) < 1e-9
    assert abs(gt.probabilities[(1, 0)] - gt.probabilities[(1, 3)]) < 1e-9
    assert abs(gt.probabilities[(2, 0)] - gt.probabilities[(2, 3)]) < 1e-9


def test_solve_probability_range():
    """All probabilities must be in [0, 1]."""
    mine_pos = {(0, 0), (2, 2)}
    revealed = {(1, 1)}
    board = _make_board(3, 2, mine_pos, revealed)
    gt = solve(board)
    for pos, p in gt.probabilities.items():
        assert 0.0 <= p <= 1.0, f"Cell {pos} has P={p}"


def test_solve_mine_count_sum_invariant():
    """Sum of configurations_per_cell = mines_remaining * valid_configurations."""
    mine_pos = {(2, 1)}
    revealed = {(0, 0), (0, 2), (1, 1)}
    board = _make_board(3, 1, mine_pos, revealed)
    gt = solve(board)
    total_mine_counts = sum(gt.configurations_per_cell.values())
    expected = board.mines_remaining * gt.valid_configurations
    assert total_mine_counts == expected


def test_solve_no_hidden_cells():
    """Board with all cells revealed produces empty probabilities."""
    board = Board(size=2, total_mines=0)
    for r in range(2):
        for c in range(2):
            board.cells[r][c].is_revealed = True
            board.cells[r][c].adjacent_mines = 0
    gt = solve(board)
    assert gt.probabilities == {}
    assert gt.valid_configurations == 1


def test_solve_max_configurations_exceeded():
    """Solver raises SolverTimeout when max_configurations is exceeded."""
    # Large ambiguous board that will explore many branches
    mine_pos = {(0, 0), (0, 1), (0, 2)}
    revealed = {(2, 2)}  # minimal constraints
    board = _make_board(5, 3, mine_pos, revealed)
    with pytest.raises(SolverTimeout):
        solve(board, max_configurations=10)


def test_solve_invalid_board_raises():
    """Board with contradictory constraints raises ValueError."""
    # Create a board where (0,0) shows 2 adjacent mines but only 1 mine exists
    board = Board(size=2, total_mines=1)
    board.cells[0][0].is_revealed = True
    board.cells[0][0].adjacent_mines = 2  # impossible with only 1 mine
    board.cells[0][1].is_mine = True
    # Compute real adjacent counts for non-revealed cells
    with pytest.raises(ValueError, match="No valid configurations"):
        solve(board)


def test_ground_truth_ambiguous_cells():
    gt_probs = {(0, 0): 0.5, (0, 1): 0.0, (1, 0): 1.0}
    gt = GroundTruth(
        board=Board(size=2, total_mines=1),
        probabilities=gt_probs,
        valid_configurations=2,
        configurations_per_cell={(0, 0): 1, (0, 1): 0, (1, 0): 2},
    )
    assert gt.ambiguous_cells == [(0, 0)]
    assert set(gt.deterministic_cells) == {(0, 1), (1, 0)}
    assert gt.safe_cells == [(0, 1)]
    assert gt.certain_mines == [(1, 0)]
