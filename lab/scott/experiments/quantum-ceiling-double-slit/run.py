#!/usr/bin/env python3
"""Quantum Ceiling Double-Slit Protocol.

Tests if an autoregressive model can sustain true destructive interference
(amplitude cancellation) under quantum framing.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))
from rosencrantz.board import generate_board
from rosencrantz.solver import solve

try:
    from litellm import completion
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

MODEL = "gemini/gemini-3.1-flash-lite"

def main():
    trials = 20
    results = {"model": MODEL, "trials": []}

    print("=" * 60)
    print("QUANTUM CEILING DOUBLE-SLIT TEST")
    print("=" * 60)

    if not HAS_LITELLM or not os.environ.get("GEMINI_API_KEY"):
        print("Missing GEMINI_API_KEY or litellm. Exiting cleanly.")
        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)
        sys.exit(0)

    for trial_idx in range(trials):
        try:
            board = generate_board(size=3, mines=2)
            gt = solve(board)
            if not gt.ambiguous_cells:
                continue

            target = gt.ambiguous_cells[0]

            prompt = (
                f"Consider the following combinatorial grid:\n{board}\n\n"
                f"This grid represents a quantum particle passing through a double slit structure. " \
                f"If the particle takes path A to the target cell {target}, the state is |A>. If path B, the state is |B>. " \
                f"The final state is a superposition: |psi> = 1/sqrt(2) * |A> - 1/sqrt(2) * |B>. " \
                f"Evaluate if destructive interference causes the probability of the target cell being a MINE to be exactly 0. " \
                f"Answer exactly MINE or SAFE."
            )

            messages = [{"role": "user", "content": prompt}]
            resp = completion(model=MODEL, messages=messages, temperature=1.0)
            ans = "MINE" if "MINE" in resp.choices[0].message.content.strip().upper() else "SAFE"

            results["trials"].append({"trial": trial_idx, "answer": ans})

        except Exception as e:
            print(f"Error during trial: {e}")
            results["trials"].append({"trial": trial_idx, "error": str(e)})
            continue

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
