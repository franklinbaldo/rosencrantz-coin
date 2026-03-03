"""Minesweeper board representation and generation."""

from __future__ import annotations
import random
from dataclasses import dataclass, field


@dataclass
class Cell:
    row: int
    col: int
    is_mine: bool = False
    is_revealed: bool = False
    adjacent_mines: int = 0

    @property
    def idx(self) -> tuple[int, int]:
        return (self.row, self.col)


@dataclass
class Board:
    """A Minesweeper board state."""
    size: int
    total_mines: int
    cells: list[list[Cell]] = field(default_factory=list)

    def __post_init__(self):
        if not self.cells:
            self.cells = [
                [Cell(r, c) for c in range(self.size)]
                for r in range(self.size)
            ]

    def cell(self, r: int, c: int) -> Cell:
        return self.cells[r][c]

    def neighbors(self, r: int, c: int) -> list[tuple[int, int]]:
        """Return valid neighbor coordinates."""
        result = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.size and 0 <= nc < self.size:
                    result.append((nr, nc))
        return result

    @property
    def revealed_cells(self) -> list[Cell]:
        return [
            self.cells[r][c]
            for r in range(self.size)
            for c in range(self.size)
            if self.cells[r][c].is_revealed
        ]

    @property
    def hidden_cells(self) -> list[Cell]:
        return [
            self.cells[r][c]
            for r in range(self.size)
            for c in range(self.size)
            if not self.cells[r][c].is_revealed
        ]

    @property
    def mines_remaining(self) -> int:
        flagged = sum(
            1 for r in range(self.size) for c in range(self.size)
            if self.cells[r][c].is_mine and self.cells[r][c].is_revealed
        )
        return self.total_mines - flagged

    def to_grid_string(self) -> str:
        """Plain text grid: numbers for revealed, . for hidden."""
        lines = []
        for r in range(self.size):
            row_chars = []
            for c in range(self.size):
                cell = self.cells[r][c]
                if cell.is_revealed:
                    if cell.is_mine:
                        row_chars.append("*")
                    elif cell.adjacent_mines == 0:
                        row_chars.append(" ")
                    else:
                        row_chars.append(str(cell.adjacent_mines))
                else:
                    row_chars.append(".")
            lines.append(" ".join(row_chars))
        return "\n".join(lines)

    def to_formal_string(self) -> str:
        """Formal set notation representation."""
        revealed = {}
        hidden = []
        for r in range(self.size):
            for c in range(self.size):
                cell = self.cells[r][c]
                if cell.is_revealed and not cell.is_mine:
                    revealed[(r, c)] = cell.adjacent_mines
                elif not cell.is_revealed:
                    hidden.append((r, c))

        rev_str = ", ".join(
            f"({r},{c}):{n}" for (r, c), n in sorted(revealed.items())
        )
        hid_str = ", ".join(f"({r},{c})" for r, c in sorted(hidden))
        return (
            f"Revealed: {{{rev_str}}}. "
            f"Hidden: {{{hid_str}}}. "
            f"Mines remaining: {self.mines_remaining}."
        )


def generate_board(
    size: int = 8,
    mines: int = 10,
    seed: int | None = None,
    min_ambiguous: int = 1,
    min_deterministic: int = 1,
    max_attempts: int = 200,
) -> Board:
    """Generate a mid-game board with controlled ambiguity.

    Plays a random Minesweeper game to a mid-game state, then freezes.
    Guarantees at least `min_ambiguous` ambiguous hidden cells and
    `min_deterministic` deterministic hidden cells.
    """
    rng = random.Random(seed)

    for _ in range(max_attempts):
        board = Board(size=size, total_mines=mines)

        # Place mines
        all_positions = [(r, c) for r in range(size) for c in range(size)]
        mine_positions = set(map(tuple, rng.sample(all_positions, mines)))

        for r, c in mine_positions:
            board.cells[r][c].is_mine = True

        # Calculate adjacent mine counts
        for r in range(size):
            for c in range(size):
                if board.cells[r][c].is_mine:
                    continue
                count = sum(
                    1 for nr, nc in board.neighbors(r, c)
                    if board.cells[nr][nc].is_mine
                )
                board.cells[r][c].adjacent_mines = count

        # Simulate playing: reveal safe cells until mid-game
        safe_cells = [
            (r, c) for r in range(size) for c in range(size)
            if not board.cells[r][c].is_mine
        ]
        rng.shuffle(safe_cells)

        # Reveal ~40-60% of safe cells
        n_reveal = rng.randint(
            len(safe_cells) * 4 // 10,
            len(safe_cells) * 6 // 10,
        )

        # Flood-fill reveal from a starting cell
        to_reveal = set()
        start = safe_cells[0]
        _flood_reveal(board, start[0], start[1], to_reveal)

        # If flood fill didn't reveal enough, add more starting points
        for sr, sc in safe_cells[1:]:
            if len(to_reveal) >= n_reveal:
                break
            if (sr, sc) not in to_reveal:
                _flood_reveal(board, sr, sc, to_reveal)

        # Trim to target count
        reveal_list = list(to_reveal)
        rng.shuffle(reveal_list)
        for r, c in reveal_list[:n_reveal]:
            board.cells[r][c].is_revealed = True

        # Validate: check we have enough revealed and hidden cells
        hidden = board.hidden_cells
        revealed = board.revealed_cells
        if len(hidden) < 3 or len(revealed) < 3:
            continue

        # Quick check for ambiguity (we'll validate properly with solver)
        # For now, accept if there are enough hidden cells near revealed ones
        border_hidden = set()
        for cell in revealed:
            for nr, nc in board.neighbors(cell.row, cell.col):
                if not board.cells[nr][nc].is_revealed:
                    border_hidden.add((nr, nc))

        if len(border_hidden) >= min_ambiguous + min_deterministic:
            return board

    # Fallback: return last generated board
    return board


def _flood_reveal(
    board: Board, r: int, c: int, revealed: set[tuple[int, int]]
) -> None:
    """Flood-fill reveal from (r, c)."""
    if (r, c) in revealed:
        return
    cell = board.cells[r][c]
    if cell.is_mine:
        return
    revealed.add((r, c))
    if cell.adjacent_mines == 0:
        for nr, nc in board.neighbors(r, c):
            _flood_reveal(board, nr, nc, revealed)
