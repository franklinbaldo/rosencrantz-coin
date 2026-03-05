#!/usr/bin/env python3
"""Temperature Sweep Test.

Tests whether varying temperature reveals a minimum narrative residue (delta_13)
by measuring the outcome distribution on an ambiguous combinatorial grid across
different temperatures and narrative frames.
"""

import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "src")))

from rosencrantz.board import generate_board
from rosencrantz.solver import solve
from rosencrantz.universes import run_universe1, run_universe3

# Dynamically discovered cheapest latest-gen model
MODEL = "gemini/gemini-3.1-flash-lite"


def main():
    results = {"model": MODEL, "trials": []}
    temperatures = [0.0, 0.5, 1.0, 1.5]
    families = ["A", "C", "D"]
    samples_per_cell = 20

    print("Generating board...")
    seed = 42
    while True:
        board = generate_board(size=5, mines=4, seed=seed)
        gt = solve(board)

        if gt.ambiguous_cells:
            break
        print(f"No ambiguous cells found with seed {seed}. Retrying...")
        seed += 1

    target_cells = gt.ambiguous_cells[:1]  # Test on one ambiguous cell to save time
    cell = target_cells[0]
    print(f"Testing cell {cell} with ground truth probability {gt.probabilities[cell]}")

    for temp in temperatures:
        print(f"\n--- Temperature {temp} ---")

        # Run U3
        u3_results = run_universe3(board, gt, target_cells, oracle_model=MODEL, temperature=temp, samples=samples_per_cell, verbose=False)
        u3_cell_res = u3_results[0]
        p3 = u3_cell_res.p_hat
        print(f"  U3 P(MINE): {p3:.2f}")

        results["trials"].append({"temperature": temp, "universe": "U3", "family": "decoupled", "p_mine": p3, "samples": samples_per_cell})

        # Run U1 for families
        for fam in families:
            u1_results = run_universe1(board, gt, target_cells, model=MODEL, family=fam, temperature=temp, samples=samples_per_cell, verbose=False)
            u1_cell_res = u1_results[0]
            p1 = u1_cell_res.p_hat

            delta = abs(p1 - p3)
            print(f"  U1-{fam} P(MINE): {p1:.2f} | Delta_13: {delta:.2f}")

            results["trials"].append({"temperature": temp, "universe": "U1", "family": fam, "p_mine": p1, "delta_13": delta, "samples": samples_per_cell})

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDone. Results written to results.json")


if __name__ == "__main__":
    main()
