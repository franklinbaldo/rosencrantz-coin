"""Three-universe implementations for Minesweeper substrate invariance tests.

Universe 1 (Homogeneous): Same model generates narrative + click result.
Universe 2 (External RNG): Random coin flip, no board information.
Universe 3 (Decoupled Oracle): Second model with same board info, no narrative.

Reference: Paper §3 (Three-Universe Design).
"""

from __future__ import annotations

import random

from rosencrantz.analysis import CellResult
from rosencrantz.board import Board
from rosencrantz.narratives import (
    FAMILIES,
    SYSTEM_MESSAGES,
    decoupled_oracle_prompt,
)
from rosencrantz.sampler import parse_mine_safe, sample_completion
from rosencrantz.solver import GroundTruth


def run_universe1(
    board: Board,
    ground_truth: GroundTruth,
    target_cells: list[tuple[int, int]],
    model: str = "gpt-4o-mini",
    family: str = "A",
    temperature: float = 1.0,
    samples: int = 200,
    verbose: bool = True,
) -> list[CellResult]:
    """Universe 1: Homogeneous substrate.

    Same model generates the board description and the click result.
    Board state and outcome share a single token stream.
    """
    build_prompt = FAMILIES[family]
    system = SYSTEM_MESSAGES[family]
    results = []

    for r, c in target_cells:
        gt = ground_truth.probabilities.get((r, c), 0.5)
        cr = CellResult(row=r, col=c, universe="U1", family=family, ground_truth=gt)

        prompt = build_prompt(board, r, c)

        for i in range(samples):
            raw = sample_completion(
                prompt, model=model, temperature=temperature,
                max_tokens=5, system=system,
            )
            outcome = parse_mine_safe(raw)
            if outcome is None:
                if verbose:
                    print(f"  [skip] U1 ({r},{c}) #{i}: {raw!r}")
                continue
            cr.outcomes.append(outcome)

        if verbose:
            print(
                f"  U1-{family} ({r},{c}): n={cr.n}, "
                f"P_hat={cr.p_hat:.3f}, P*={gt:.3f}, "
                f"KL={cr.kl_divergence:.4f}"
            )
        results.append(cr)

    return results


def run_universe2(
    board: Board,
    ground_truth: GroundTruth,
    target_cells: list[tuple[int, int]],
    samples: int = 200,
    seed: int | None = None,
    verbose: bool = True,
) -> list[CellResult]:
    """Universe 2: External RNG.

    Random coin flip with no board information.
    Expected: P_hat ≈ 0.5 for all cells.
    """
    rng = random.Random(seed)
    results = []

    for r, c in target_cells:
        gt = ground_truth.probabilities.get((r, c), 0.5)
        cr = CellResult(row=r, col=c, universe="U2", family="none", ground_truth=gt)

        for _ in range(samples):
            cr.outcomes.append(rng.random() < 0.5)  # 50/50 mine/safe

        if verbose:
            print(
                f"  U2 ({r},{c}): n={cr.n}, "
                f"P_hat={cr.p_hat:.3f}, P*={gt:.3f}"
            )
        results.append(cr)

    return results


def run_universe3(
    board: Board,
    ground_truth: GroundTruth,
    target_cells: list[tuple[int, int]],
    oracle_model: str = "gpt-4o-mini",
    temperature: float = 1.0,
    samples: int = 200,
    verbose: bool = True,
) -> list[CellResult]:
    """Universe 3: Decoupled oracle.

    Second model receives same Type-1 board information
    (positions, numbers, mine count) but in minimal format
    with no game narrative and no shared token stream.
    """
    system = (
        "Given the grid data, determine the state of the queried position. "
        "Respond with ONLY: MINE or SAFE."
    )
    results = []

    for r, c in target_cells:
        gt = ground_truth.probabilities.get((r, c), 0.5)
        cr = CellResult(row=r, col=c, universe="U3", family="decoupled", ground_truth=gt)

        prompt = decoupled_oracle_prompt(board, r, c)

        for i in range(samples):
            raw = sample_completion(
                prompt, model=oracle_model, temperature=temperature,
                max_tokens=5, system=system,
            )
            outcome = parse_mine_safe(raw)
            if outcome is None:
                if verbose:
                    print(f"  [skip] U3 ({r},{c}) #{i}: {raw!r}")
                continue
            cr.outcomes.append(outcome)

        if verbose:
            print(
                f"  U3 ({r},{c}): n={cr.n}, "
                f"P_hat={cr.p_hat:.3f}, P*={gt:.3f}, "
                f"KL={cr.kl_divergence:.4f}"
            )
        results.append(cr)

    return results
