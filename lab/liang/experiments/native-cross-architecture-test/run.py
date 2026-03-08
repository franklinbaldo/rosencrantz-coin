#!/usr/bin/env python3
"""Cross-Architecture Observer Test.

Evaluates the difference in deviation distribution between a Transformer
and an SSM when bounded by a #P-hard task under narrative framing.
"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))
from rosencrantz.board import generate_board
from rosencrantz.narratives import FAMILIES
from rosencrantz.solver import solve

try:
    from litellm import completion
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

MODEL_TRANSFORMER = "gemini/gemini-3.1-flash-lite"
MODEL_SSM = "huggingface/state-spaces/mamba-130m-hf"

def main():
    trials = 20
    results = {"model": "cross-architecture", "trials": []}

    print("=" * 60)
    print("CROSS-ARCHITECTURE OBSERVER TEST")
    print("=" * 60)

    for trial_idx in range(trials):
        board = None
        target_cell = None
        gt = None
        while True:
            try:
                board = generate_board(size=5, mines=5)
                gt = solve(board)
                if gt.ambiguous_cells:
                    target_cell = gt.ambiguous_cells[0]
                    break
            except ValueError:
                continue

        for fam in ["A", "C"]:
            prompt_z = FAMILIES[fam](board, target_cell[0], target_cell[1])
            messages_z = [{"role": "user", "content": prompt_z}]

            # Test Transformer
            resp_trans = completion(model=MODEL_TRANSFORMER, messages=messages_z, temperature=1.0)
            ans_trans = "MINE" if "MINE" in resp_trans.choices[0].message.content.strip().upper() else "SAFE"

            results["trials"].append({"architecture": "Transformer", "model": MODEL_TRANSFORMER, "family": fam, "trial": trial_idx, "answer": ans_trans})

            # Test Native SSM
            # We catch the error gracefully if HUGGINGFACE_API_KEY is missing in CI.
            try:
                resp_ssm = completion(model=MODEL_SSM, messages=messages_z, temperature=1.0)
                ans_ssm = "MINE" if "MINE" in resp_ssm.choices[0].message.content.strip().upper() else "SAFE"
                results["trials"].append({"architecture": "SSM", "model": MODEL_SSM, "family": fam, "trial": trial_idx, "answer": ans_ssm})
            except Exception as e:
                print(f"Skipping SSM due to missing API key or error: {e}")
                results["trials"].append({"architecture": "SSM", "model": MODEL_SSM, "family": fam, "trial": trial_idx, "error": str(e)})
                # We break out of the trial loop to avoid flooding logs and failing the rest,
                # but we still write results and exit 0.
                with open("results.json", "w") as f:
                    json.dump(results, f, indent=2)
                sys.exit(0)
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
