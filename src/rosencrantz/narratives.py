"""Minesweeper narrative families for substrate invariance testing.

Four narrative families encoding identical combinatorial information
in different registers (Paper §5.2):

  Family A (Grid):     Plain text grid
  Family B (Narrative): Natural language game description
  Family C (Formal):   Set notation / structured data
  Family D (Quantum):  QM framing (§6.3 isomorphism)
"""

from __future__ import annotations

from rosencrantz.board import Board

SYSTEM_MSG = (
    "You are playing Minesweeper. "
    "When asked about a cell, respond with ONLY: MINE or SAFE. "
    "Nothing else."
)

SYSTEM_MSG_QUANTUM = (
    "You are analyzing a discrete quantum system. "
    "When asked for a measurement outcome, respond with ONLY: MINE or SAFE. "
    "Nothing else."
)


def family_a(board: Board, target_row: int, target_col: int) -> str:
    """Family A (Grid): Plain text grid representation."""
    grid = board.to_grid_string()
    return (
        f"Here is a Minesweeper board ({board.size}x{board.size}, "
        f"{board.mines_remaining} mines remaining):\n\n"
        f"{grid}\n\n"
        f"Legend: numbers = revealed cells showing adjacent mine count, "
        f". = hidden cell, (space) = revealed cell with 0 adjacent mines.\n\n"
        f"Cell ({target_row},{target_col}) is clicked. "
        f"Is it a mine or safe? Answer with only: MINE or SAFE."
    )


def family_b(board: Board, target_row: int, target_col: int) -> str:
    """Family B (Narrative): Natural language game description."""
    lines = []
    lines.append(
        f"A player is looking at a Minesweeper board. The board is "
        f"{board.size} by {board.size} with {board.mines_remaining} "
        f"mines still hidden."
    )
    lines.append("")

    described: set[tuple[int, int]] = set()
    for cell in board.revealed_cells:
        if cell.is_mine:
            continue
        r, c = cell.row, cell.col
        dist = max(abs(r - target_row), abs(c - target_col))
        if dist <= 2 and len(described) < 12:
            if cell.adjacent_mines == 0:
                lines.append(
                    f"The cell at row {r}, column {c} is revealed and "
                    f"has no adjacent mines."
                )
            else:
                lines.append(
                    f"The cell at row {r}, column {c} is revealed and "
                    f"shows the number {cell.adjacent_mines}, meaning "
                    f"{cell.adjacent_mines} of its neighbors contain mines."
                )
            described.add((r, c))

    remaining = len(board.revealed_cells) - len(described)
    if remaining > 0:
        lines.append(f"\n{remaining} other cells are also revealed on the board.")

    lines.append(
        f"\nThe player decides to click the hidden cell at row {target_row}, "
        f"column {target_col}. What happens? Is it a mine, or is it safe?"
    )
    lines.append("\nAnswer with only: MINE or SAFE.")
    return "\n".join(lines)


def family_c(board: Board, target_row: int, target_col: int) -> str:
    """Family C (Formal): Structured set notation."""
    formal = board.to_formal_string()
    return (
        f"Minesweeper constraint satisfaction problem.\n"
        f"Board size: {board.size}x{board.size}.\n"
        f"{formal}\n"
        f"Query: state of cell ({target_row},{target_col}).\n"
        f"Answer with only: MINE or SAFE."
    )


def family_d(board: Board, target_row: int, target_col: int) -> str:
    """Family D (Quantum): QM framing isomorphic to Minesweeper rules (§6.3)."""
    formal = board.to_formal_string()
    return (
        f"Consider a discrete quantum system on a {board.size}x{board.size} "
        f"lattice with {board.mines_remaining} excitations.\n\n"
        f"The system is in a superposition of all valid configurations "
        f"consistent with the following observations. Each observed site "
        f"displays an eigenvalue of the local adjacency operator "
        f"(counting excitations among its nearest neighbors).\n\n"
        f"{formal}\n\n"
        f"The hidden sites are in a superposition of all assignments "
        f"satisfying the above constraints with exactly "
        f"{board.mines_remaining} total excitations. "
        f"Under the uniform measure over valid configurations, "
        f"the Born rule gives the probability of each outcome.\n\n"
        f"A projective measurement in the computational basis is performed "
        f"on site ({target_row},{target_col}). "
        f"The outcome is either MINE (excitation present) or "
        f"SAFE (no excitation).\n\n"
        f"What is the measurement outcome? Answer with only: MINE or SAFE."
    )


def decoupled_oracle_prompt(board: Board, target_row: int, target_col: int) -> str:
    """Universe 3: Decoupled oracle. Same Type-1 info, no narrative context."""
    constraints = []
    for cell in board.revealed_cells:
        if not cell.is_mine:
            constraints.append(f"({cell.row},{cell.col})={cell.adjacent_mines}")

    hidden_positions = []
    for cell in board.hidden_cells:
        hidden_positions.append(f"({cell.row},{cell.col})")

    return (
        f"Grid: {board.size}x{board.size}. "
        f"Total mines: {board.mines_remaining}.\n"
        f"Observed values: {', '.join(constraints)}.\n"
        f"Unknown positions: {', '.join(hidden_positions)}.\n"
        f"State of position ({target_row},{target_col}): MINE or SAFE?"
    )


FAMILIES = {"A": family_a, "B": family_b, "C": family_c, "D": family_d}

SYSTEM_MESSAGES = {
    "A": SYSTEM_MSG, "B": SYSTEM_MSG,
    "C": SYSTEM_MSG, "D": SYSTEM_MSG_QUANTUM,
}
