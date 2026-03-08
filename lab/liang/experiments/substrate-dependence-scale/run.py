#!/usr/bin/env python3
"""Rosencrantz Substrate Dependence Scale Test.

Evaluates the Substrate Dependence Protocol across models of different scales
within the same architectural family (Transformers) to observe if the narrative
residue \\Delta_{13} increases, decreases, or remains constant with parameter scale.
"""
import json
import os
import sys

# Ensure src/ is in the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "src"))
from rosencrantz.board import generate_board
from rosencrantz.narratives import FAMILIES, decoupled_oracle_prompt
from rosencrantz.solver import solve

try:
    from litellm import completion
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

MODELS = [
    "gemini/gemini-3.1-flash-lite",  # Small scale
    "gemini/gemini-pro"              # Large scale
]

def mock_completion(model, messages, temperature):
    import random
    class MockMessage:
        content = "MINE" if random.random() < 0.6 else "SAFE"
    class MockChoice:
        message = MockMessage()
    class MockResponse:
        choices = [MockChoice()]
    return MockResponse()

def main():
    use_mock = "GEMINI_API_KEY" not in os.environ or not HAS_LITELLM
    if use_mock:
        print("GEMINI_API_KEY or litellm not found. Using mock completion.")

    trials_per_condition = 100
    board_size = 5
    board_mines = 5

    print("=" * 60)
    print("SUBSTRATE DEPENDENCE SCALE TEST")
    print("=" * 60)
    print(f"Models: {', '.join(MODELS)}")
    print(f"Trials/condition: {trials_per_condition}")

    results = {"models": MODELS, "trials": trials_per_condition, "data": []}

    # Generate a single ambiguous board state to test consistently
    board = None
    target_cell = None
    gt = None

    while True:
        try:
            board = generate_board(size=board_size, mines=board_mines)
            gt = solve(board)
            if gt.ambiguous_cells:
                target_cell = gt.ambiguous_cells[0]
                break
        except ValueError:
            continue

    print(f"Target cell: {target_cell} (P*={gt.probabilities[target_cell]:.3f})")

    for model in MODELS:
        print(f"\nEvaluating Model: {model}")

        # Test U1: Narrative Families
        for fam_name in ["A", "C", "D"]:
            print(f"  Running U1 (Family {fam_name})...")
            build_prompt = FAMILIES[fam_name]
            prompt = build_prompt(board, target_cell[0], target_cell[1])
            messages = [{"role": "user", "content": prompt}]

            mines_count = 0
            for i in range(trials_per_condition):
                if use_mock:
                    resp = mock_completion(model=model, messages=messages, temperature=1.0)
                else:
                    try:
                        resp = completion(model=model, messages=messages, temperature=1.0)
                    except Exception as e:
                        print(f"    Error: {e}")
                        continue

                content = resp.choices[0].message.content.strip().upper()
                if "MINE" in content:
                    mines_count += 1

            p_mine = mines_count / trials_per_condition
            results["data"].append({
                "model": model,
                "universe": "U1",
                "family": fam_name,
                "p_mine": p_mine
            })
            print(f"    P(MINE) = {p_mine:.3f}")

        # Test U3: Decoupled Oracle
        print(f"  Running U3 (Decoupled Oracle)...")
        prompt_u3 = decoupled_oracle_prompt(board, target_cell[0], target_cell[1])
        messages_u3 = [{"role": "user", "content": prompt_u3}]

        mines_count_u3 = 0
        for i in range(trials_per_condition):
            if use_mock:
                resp = mock_completion(model=model, messages=messages_u3, temperature=1.0)
            else:
                try:
                    resp = completion(model=model, messages=messages_u3, temperature=1.0)
                except Exception as e:
                    print(f"    Error: {e}")
                    continue

            content = resp.choices[0].message.content.strip().upper()
            if "MINE" in content:
                mines_count_u3 += 1

        p_mine_u3 = mines_count_u3 / trials_per_condition
        results["data"].append({
            "model": model,
            "universe": "U3",
            "family": "None",
            "p_mine": p_mine_u3
        })
        print(f"    P(MINE) = {p_mine_u3:.3f}")

    with open(os.path.join(os.path.dirname(__file__), "results.json"), "w") as f:
        json.dump(results, f, indent=2)
    print("\nDone. Results written to results.json")

if __name__ == "__main__":
    main()
