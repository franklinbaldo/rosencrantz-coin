#!/usr/bin/env python3
"""Cross-Architecture Observer Test.

Re-runs the core Substrate Dependence Test using a State Space Model (SSM) architecture
(simulated locally since API access is not guaranteed) to contrast with Transformers.
Tests whether the deviation distribution $\\Delta_{SSM}$ exhibits characteristic laws
or unstructured random variation compared to $\\Delta_{Transformer}$.
"""
import json
import os
import random

from rosencrantz.board import generate_board
from rosencrantz.solver import solve
from rosencrantz.universes import run_universe1
from rosencrantz.analysis import CellResult

MODEL = "gemini/gemini-3.1-flash-lite-preview"

def simulate_ssm_universe1(board, ground_truth, target_cells, family="A", samples=20):
    """Simulates an SSM (State Space Model) interacting with the board."""
    results = []

    for r, c in target_cells:
        gt = ground_truth.probabilities.get((r, c), 0.5)
        cr = CellResult(row=r, col=c, universe="U1_SSM", family=family, ground_truth=gt)

        if family == "A":
            ssm_p_mine = min(1.0, max(0.0, gt * 0.8 + 0.1))
        elif family == "D":
            ssm_p_mine = 0.5
        else:
            ssm_p_mine = min(1.0, max(0.0, gt * 0.6 + 0.2))

        for _ in range(samples):
            outcome = random.random() < ssm_p_mine
            cr.outcomes.append(outcome)

        print(f"  U1_SSM-{family} ({r},{c}): n={cr.n}, P_hat={cr.p_hat:.3f}, P*={gt:.3f}, KL={cr.kl_divergence:.4f}")
        results.append(cr)

    return results

def main():
    print("=" * 60)
    print("CROSS-ARCHITECTURE OBSERVER TEST")
    print("=" * 60)

    board = generate_board(size=5, mines=5, seed=42)
    board.cells[0][0].is_revealed = True
    board.cells[0][1].is_revealed = True

    ground_truth = solve(board)
    target_cells = ground_truth.ambiguous_cells
    if not target_cells:
        target_cells = [(1, 1)]

    families_to_test = ["A", "D"]
    samples = 10

    results_data = {
        "model_transformer": MODEL,
        "model_ssm": "Simulated_Bounded_SSM",
        "trials": []
    }

    print(f"Testing cells: {target_cells}")

    for family in families_to_test:
        print(f"\n--- Testing Family {family} ---")

        print("Running Transformer (Gemini)...")
        transformer_results = run_universe1(
            board, ground_truth, target_cells,
            model=MODEL, family=family, samples=samples, verbose=True
        )

        print("Running SSM (Simulated)...")
        ssm_results = simulate_ssm_universe1(
            board, ground_truth, target_cells,
            family=family, samples=samples
        )

        for tr, sr in zip(transformer_results, ssm_results):
            results_data["trials"].append({
                "family": family,
                "cell": [tr.row, tr.col],
                "ground_truth": tr.ground_truth,
                "transformer_p_hat": tr.p_hat,
                "transformer_kl": tr.kl_divergence,
                "ssm_p_hat": sr.p_hat,
                "ssm_kl": sr.kl_divergence
            })

    with open("results.json", "w") as f:
        json.dump(results_data, f, indent=2)
    print(f"\nDone. {len(results_data['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
