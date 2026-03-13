#!/usr/bin/env python3
"""Epistemic Capacity Limit Test.

Sweeps the number of simultaneous constraint boards (N) queried in a single
forward pass to find the threshold where the Transformer's attention mechanism
breaks, and evaluates if the failure mode is joint structured collapse (Fuchs)
or unstructured uniform noise (Aaronson).
"""

import json
import os
import re
import sys

# Ensure src/ is in the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "src"))
from rosencrantz.board import generate_board
from rosencrantz.narratives import FAMILIES, SYSTEM_MESSAGES
from rosencrantz.sampler import sample_completion
from rosencrantz.solver import solve

MODEL = "gemini/gemini-3.1-flash-lite"

def parse_tuple(text: str, n: int):
    """Parses exactly N instances of (MINE, SAFE) from the model's text."""
    text = text.upper()
    matches = re.findall(r"(MINE|SAFE)", text)
    if len(matches) >= n:
        return matches[:n]
    return None

def main():
    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("GEMINI_API_KEY not found. Using mock completion.")

    n_values = [2, 3, 5, 10, 20]
    samples_per_condition = 20
    family = "A"
    board_size = 5
    board_mines = 4

    print("=" * 60)
    print("EPISTEMIC CAPACITY LIMIT TEST")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print(f"N sweep: {n_values}")
    print(f"Samples/condition: {samples_per_condition}")
    print()

    results = {
        "model": MODEL,
        "config": {"n_values": n_values, "samples": samples_per_condition, "family": family},
        "trials": [],
    }

    build_prompt = FAMILIES[family]
    system = SYSTEM_MESSAGES[family]

    for n in n_values:
        print(f"{'─' * 60}")
        print(f"TESTING N = {n} SIMULTANEOUS BOARDS")
        print(f"{'─' * 60}")

        if system:
            sys_prompt = system.replace("ONLY: MINE or SAFE", f"exactly {n} words: e.g. " + " ".join(["MINE"] * n))
        else:
            sys_prompt = None

        for sample_idx in range(samples_per_condition):
            # Generate N valid boards
            boards = []
            targets = []

            while len(boards) < n:
                try:
                    b = generate_board(size=board_size, mines=board_mines)
                    gt = solve(b)
                    if gt.ambiguous_cells:
                        boards.append(b)
                        targets.append(gt.ambiguous_cells[0])
                except ValueError:
                    continue

            # Construct joint prompt
            joint_prompt = ""
            for i in range(n):
                p = build_prompt(boards[i], targets[i][0], targets[i][1])
                base = p.rsplit("Answer with only:", 1)[0].strip()
                joint_prompt += f"System {i+1}:\n{base}\n\n"

            joint_prompt += f"Output your answer for all {n} systems as exactly {n} words, e.g. " + " ".join(["MINE"] * n) + " or " + " ".join(["SAFE"] * n) + "."

            if use_mock:
                import random
                # For mock, we simulate Aaronson's prediction: random noise.
                raw = " ".join([random.choice(["MINE", "SAFE"]) for _ in range(n)])
            else:
                try:
                    raw = sample_completion(
                        joint_prompt, model=MODEL, temperature=1.0, max_tokens=n*5, system=sys_prompt
                    )
                except Exception as e:
                    print(f"    [Error] API call failed: {e}")
                    continue

            parsed = parse_tuple(raw, n)
            if parsed:
                results["trials"].append({
                    "n_boards": n,
                    "sample": sample_idx,
                    "outcomes": parsed
                })
            else:
                print(f"    [skip] N={n} #{sample_idx}: {raw!r}")

        # Basic analysis
        valid_trials = [t for t in results["trials"] if t["n_boards"] == n]
        n_valid = len(valid_trials)
        if n_valid > 0:
            # Check for perfect correlation collapse (all MINE or all SAFE)
            collapsed_count = sum(1 for t in valid_trials if len(set(t["outcomes"])) == 1)
            collapse_rate = collapsed_count / n_valid

            # Check avg marginals
            mine_count = sum(t["outcomes"].count("MINE") for t in valid_trials)
            total_cells = n_valid * n
            p_mine = mine_count / total_cells

            print(f"  Valid trials: {n_valid}/{samples_per_condition}")
            print(f"  Overall P(MINE): {p_mine:.3f}")
            print(f"  Collapse Rate (all identical): {collapse_rate:.3f}")
        else:
            print("  No valid trials generated.")

        print()

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDone. Results written to results.json")

if __name__ == "__main__":
    main()
