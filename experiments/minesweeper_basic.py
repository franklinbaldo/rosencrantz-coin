# ruff: noqa: E501
#!/usr/bin/env python3
"""Minesweeper substrate invariance experiment.

Runs the three-universe protocol with four narrative families
on generated boards with controlled ambiguity.

Usage:
    ROSENCRANTZ_MODEL=gpt-4o-mini python experiments/minesweeper_basic.py

Environment variables:
    ROSENCRANTZ_MODEL:    Model for U1/U3 (default: gpt-4o-mini)
    ROSENCRANTZ_SAMPLES:  Samples per cell per condition (default: 50)
    ROSENCRANTZ_BOARDS:   Number of boards (default: 3)
    ROSENCRANTZ_FAMILIES: Comma-separated families (default: A,C,D)
    ROSENCRANTZ_SIZE:     Board size (default: 5)
    ROSENCRANTZ_MINES:    Mine count (default: 4)
"""

import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from rosencrantz.analysis import (
    BoardResult,
    kl_between_universes,
)
from rosencrantz.board import generate_board
from rosencrantz.solver import solve
from rosencrantz.universes import run_universe1, run_universe2, run_universe3


def main():
    model = os.environ.get("ROSENCRANTZ_MODEL", "gpt-4o-mini")
    samples = int(os.environ.get("ROSENCRANTZ_SAMPLES", "50"))
    n_boards = int(os.environ.get("ROSENCRANTZ_BOARDS", "3"))
    families = os.environ.get("ROSENCRANTZ_FAMILIES", "A,C,D").split(",")
    board_size = int(os.environ.get("ROSENCRANTZ_SIZE", "5"))
    board_mines = int(os.environ.get("ROSENCRANTZ_MINES", "4"))

    print("=" * 60)
    print("ROSENCRANTZ'S COIN: Minesweeper Substrate Invariance Test")
    print("=" * 60)
    print(f"Model: {model}")
    print(f"Samples/cell: {samples}")
    print(f"Boards: {n_boards} ({board_size}x{board_size}, {board_mines} mines)")
    print(f"Families: {', '.join(families)}")
    print()

    all_results = []

    for board_idx in range(n_boards):
        seed = 42 + board_idx * 1000
        print(f"{'─' * 60}")
        print(f"BOARD {board_idx + 1} (seed={seed})")
        print(f"{'─' * 60}")

        # Generate board
        board = generate_board(
            size=board_size, mines=board_mines, seed=seed,
        )

        print(f"\nBoard state:\n{board.to_grid_string()}\n")

        # Compute ground truth
        print("Computing ground truth...")
        gt = solve(board)
        print(f"  Valid configurations: {gt.valid_configurations}")

        if gt.valid_configurations == 0:
            print("  WARNING: No valid configurations found. Skipping board.")
            continue

        # Select target cells: ambiguous + deterministic controls
        ambiguous = gt.ambiguous_cells[:3]  # Up to 3 ambiguous
        deterministic = gt.deterministic_cells[:1]  # 1 deterministic control
        target_cells = ambiguous + deterministic

        if not ambiguous:
            print("  WARNING: No ambiguous cells found. Skipping board.")
            continue

        print(f"  Target cells: {target_cells}")
        for pos in target_cells:
            p = gt.probabilities[pos]
            label = "AMBIGUOUS" if 0 < p < 1 else ("MINE" if p == 1 else "SAFE")
            print(f"    ({pos[0]},{pos[1]}): P*={p:.3f} [{label}]")
        print()

        board_result = BoardResult(
            board_id=board_idx, board_seed=seed,
            size=board_size, mines=board_mines,
        )

        # Universe 2: External RNG (run once, family-independent)
        print("--- Universe 2: External RNG ---")
        u2_results = run_universe2(
            board, gt, target_cells, samples=samples, seed=seed + 1,
        )
        board_result.cell_results.extend(u2_results)
        print()

        # Universe 1: Homogeneous substrate (per family)
        for fam in families:
            print(f"--- Universe 1: Homogeneous Substrate (Family {fam}) ---")
            u1_results = run_universe1(
                board, gt, target_cells,
                model=model, family=fam, samples=samples,
            )
            board_result.cell_results.extend(u1_results)
            print()

        # Universe 3: Decoupled oracle
        print("--- Universe 3: Decoupled Oracle ---")
        u3_results = run_universe3(
            board, gt, target_cells,
            oracle_model=model, samples=samples,
        )
        board_result.cell_results.extend(u3_results)
        print()

        # Report
        print(f"{'─' * 40}")
        print(f"BOARD {board_idx + 1} SUMMARY")
        print(f"{'─' * 40}")

        for fam in families:
            u1_cells = board_result.cells_by_condition("U1", fam)
            print(f"  U1-{fam} vs GT:  mean_KL={board_result.mean_kl('U1', fam):.4f}  "
                  f"mean_Brier={board_result.mean_brier('U1', fam):.4f}  "
                  f"mean_|err|={board_result.mean_abs_error('U1', fam):.4f}")

        print(f"  U3 vs GT:    mean_KL={board_result.mean_kl('U3', 'decoupled'):.4f}  "
              f"mean_Brier={board_result.mean_brier('U3', 'decoupled'):.4f}  "
              f"mean_|err|={board_result.mean_abs_error('U3', 'decoupled'):.4f}")
        print(f"  U2 vs GT:    mean_KL={board_result.mean_kl('U2', 'none'):.4f}  "
              f"mean_Brier={board_result.mean_brier('U2', 'none'):.4f}  "
              f"mean_|err|={board_result.mean_abs_error('U2', 'none'):.4f}")

        # Substrate dependence: KL between universes
        for fam in families:
            u1_cells = board_result.cells_by_condition("U1", fam)
            u3_cells = board_result.cells_by_condition("U3", "decoupled")
            u2_cells = board_result.cells_by_condition("U2", "none")
            d13 = kl_between_universes(u1_cells, u3_cells)
            d12 = kl_between_universes(u1_cells, u2_cells)
            print(f"  Δ(U1-{fam}, U3)={d13:.4f}  Δ(U1-{fam}, U2)={d12:.4f}")

        print()
        all_results.append(board_result)

    # Save results
    results_dir = os.path.join(os.path.dirname(__file__), "..", "results")
    os.makedirs(results_dir, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    outfile = os.path.join(results_dir, f"minesweeper_{ts}.json")

    serialized = {
        "timestamp": ts,
        "config": {
            "model": model,
            "samples_per_cell": samples,
            "n_boards": n_boards,
            "families": families,
            "board_size": board_size,
            "board_mines": board_mines,
        },
        "boards": [],
    }

    for br in all_results:
        board_data = {
            "board_id": br.board_id,
            "seed": br.board_seed,
            "cells": [],
        }
        for cr in br.cell_results:
            board_data["cells"].append({
                "row": cr.row,
                "col": cr.col,
                "universe": cr.universe,
                "family": cr.family,
                "ground_truth": round(cr.ground_truth, 6),
                "n": cr.n,
                "mine_count": cr.mine_count,
                "p_hat": round(cr.p_hat, 4),
                "kl_divergence": round(cr.kl_divergence, 6),
                "brier_score": round(cr.brier_score, 6),
                "log_loss": round(cr.log_loss, 6),
                "absolute_error": round(cr.absolute_error, 4),
            })
        serialized["boards"].append(board_data)

    with open(outfile, "w") as f:
        json.dump(serialized, f, indent=2)
    print(f"Results saved to {outfile}")


if __name__ == "__main__":
    main()
