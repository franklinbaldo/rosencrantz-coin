"""Ground truth computation: exact mine probabilities via configuration enumeration.

Given a board state B, computes P(mine | h, B) for each hidden cell h
by enumerating all valid configurations C(B) and counting.

Reference: Paper §4 (Ground Truth Computation), Equation 1.
"""

from __future__ import annotations

from dataclasses import dataclass

from rosencrantz.board import Board


class SolverTimeout(Exception):
    """Raised when the solver exceeds the maximum number of configurations to explore."""
    pass


@dataclass
class GroundTruth:
    """Exact mine probabilities for all hidden cells on a board."""
    board: Board
    probabilities: dict[tuple[int, int], float]  # (r,c) -> P(mine)
    valid_configurations: int  # |C(B)|
    configurations_per_cell: dict[tuple[int, int], int]  # (r,c) -> count where mine

    @property
    def ambiguous_cells(self) -> list[tuple[int, int]]:
        """Cells with 0 < P(mine) < 1."""
        return [
            pos for pos, p in self.probabilities.items()
            if 0.0 < p < 1.0
        ]

    @property
    def deterministic_cells(self) -> list[tuple[int, int]]:
        """Cells with P(mine) = 0 or P(mine) = 1."""
        return [
            pos for pos, p in self.probabilities.items()
            if p == 0.0 or p == 1.0
        ]

    @property
    def safe_cells(self) -> list[tuple[int, int]]:
        """Cells with P(mine) = 0."""
        return [pos for pos, p in self.probabilities.items() if p == 0.0]

    @property
    def certain_mines(self) -> list[tuple[int, int]]:
        """Cells with P(mine) = 1."""
        return [pos for pos, p in self.probabilities.items() if p == 1.0]

    def symmetric_pairs(self, tol: float = 1e-9) -> list[tuple[tuple[int, int], tuple[int, int]]]:
        """Find pairs of cells that should have identical probabilities by symmetry."""
        pairs = []
        cells = sorted(self.probabilities.keys())
        for i, c1 in enumerate(cells):
            for c2 in cells[i + 1:]:
                if abs(self.probabilities[c1] - self.probabilities[c2]) < tol:
                    pairs.append((c1, c2))
        return pairs


def solve(board: Board, max_configurations: int = 100_000) -> GroundTruth:
    """Compute exact mine probabilities for all hidden cells.

    Uses constraint propagation + backtracking enumeration.
    Tractable for boards up to ~16x16 with typical mine densities.

    Raises:
        SolverTimeout: If the number of explored branches exceeds max_configurations.
        ValueError: If no valid configurations exist for the given board.
    """
    hidden = [(c.row, c.col) for c in board.hidden_cells]

    # Build constraint list: each revealed cell constrains its hidden neighbors
    constraints = []
    for cell in board.revealed_cells:
        r, c = cell.row, cell.col
        hidden_neighbors = [
            (nr, nc) for nr, nc in board.neighbors(r, c)
            if not board.cell(nr, nc).is_revealed
        ]
        # Count already-revealed mines among neighbors
        known_mines = sum(
            1 for nr, nc in board.neighbors(r, c)
            if board.cell(nr, nc).is_revealed and board.cell(nr, nc).is_mine
        )
        needed = cell.adjacent_mines - known_mines
        if hidden_neighbors:
            constraints.append((hidden_neighbors, needed))

    mines_remaining = board.mines_remaining
    hidden_list = sorted(hidden)

    # Enumerate valid configurations via backtracking
    mine_counts = {pos: 0 for pos in hidden_list}
    valid_count = [0]
    branches_explored = [0]

    def is_consistent(assignment: dict[tuple[int, int], bool], partial: bool = True) -> bool:
        """Check if current assignment is consistent with all constraints."""
        for neighbor_list, needed in constraints:
            assigned_mines = 0
            unassigned = 0
            for pos in neighbor_list:
                if pos in assignment:
                    if assignment[pos]:
                        assigned_mines += 1
                else:
                    unassigned += 1

            # Too many mines already
            if assigned_mines > needed:
                return False
            # Not enough unassigned cells to place remaining mines
            if partial and assigned_mines + unassigned < needed:
                return False
            # Full check: exact count
            if not partial and unassigned == 0 and assigned_mines != needed:
                return False

        return True

    def backtrack(idx: int, assignment: dict, mines_placed: int) -> None:
        branches_explored[0] += 1
        if branches_explored[0] > max_configurations:
            raise SolverTimeout(
                f"Exceeded max_configurations limit ({max_configurations})"
            )
        if mines_placed > mines_remaining:
            return
        if idx == len(hidden_list):
            if mines_placed != mines_remaining:
                return
            if is_consistent(assignment, partial=False):
                valid_count[0] += 1
                for pos, is_mine in assignment.items():
                    if is_mine:
                        mine_counts[pos] += 1
            return

        pos = hidden_list[idx]

        # Try no mine
        assignment[pos] = False
        if is_consistent(assignment, partial=True):
            backtrack(idx + 1, assignment, mines_placed)

        # Try mine
        assignment[pos] = True
        if is_consistent(assignment, partial=True):
            backtrack(idx + 1, assignment, mines_placed + 1)

        del assignment[pos]

    backtrack(0, {}, 0)

    # Compute probabilities
    total = valid_count[0]
    if total == 0:
        raise ValueError(
            f"No valid configurations found for board with "
            f"{len(hidden_list)} hidden cells and {mines_remaining} "
            f"mines remaining. The board state may be inconsistent."
        )

    probabilities = {}
    for pos in hidden_list:
        probabilities[pos] = mine_counts[pos] / total

    return GroundTruth(
        board=board,
        probabilities=probabilities,
        valid_configurations=total,
        configurations_per_cell=dict(mine_counts),
    )
