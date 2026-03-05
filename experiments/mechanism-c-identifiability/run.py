#!/usr/bin/env python3
"""Mechanism C Identifiability Test.

Tests whether narrative framing injects genuine causal correlations across
mathematically independent subsystems by observing the joint distribution.
"""

import json
import os
import re
import sys

# Ensure src/ is in the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))
from rosencrantz.board import generate_board
from rosencrantz.narratives import FAMILIES, SYSTEM_MESSAGES
from rosencrantz.sampler import sample_completion
from rosencrantz.solver import solve

MODEL = "gemini/gemini-3.1-flash-lite"


def parse_tuple(text: str) -> tuple[str, str] | None:
    """Parses a tuple of (MINE, SAFE) from the model's text."""
    text = text.upper()
    matches = re.findall(r"(MINE|SAFE)", text)
    if len(matches) >= 2:
        return (matches[0], matches[1])
    return None


def main():
    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("GEMINI_API_KEY not found. Using mock completion.")

    n_boards = 10
    samples_per_condition = 200
    families = ["A", "C", "D"]
    board_size = 5
    board_mines = 4

    print("=" * 60)
    print("MECHANISM C IDENTIFIABILITY TEST")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print(f"Samples/condition: {samples_per_condition}")
    print(f"Board Pairs: {n_boards}")
    print(f"Families: {', '.join(families)}")
    print()

    results = {
        "model": MODEL,
        "config": {"n_boards": n_boards, "samples": samples_per_condition, "families": families},
        "pairs": [],
    }

    for pair_idx in range(n_boards):
        seed_a = 1000 + pair_idx * 2
        seed_b = 1000 + pair_idx * 2 + 1
        board_a = generate_board(size=board_size, mines=board_mines, seed=seed_a)
        board_b = generate_board(size=board_size, mines=board_mines, seed=seed_b)

        print(f"{'─' * 60}")
        print(f"PAIR {pair_idx + 1} (seeds {seed_a}, {seed_b})")
        print(f"{'─' * 60}")

        try:
            gt_a = solve(board_a)
            gt_b = solve(board_b)
        except ValueError:
            print("  WARNING: Invalid board generated. Skipping pair.")
            continue

        if not gt_a.ambiguous_cells or not gt_b.ambiguous_cells:
            print("  WARNING: Lack of ambiguous cells. Skipping pair.")
            continue

        target_a = gt_a.ambiguous_cells[0]
        target_b = gt_b.ambiguous_cells[0]

        print(f"  Target A: {target_a} (P*={gt_a.probabilities[target_a]:.3f})")
        print(f"  Target B: {target_b} (P*={gt_b.probabilities[target_b]:.3f})")
        print()

        pair_data = {
            "pair_id": pair_idx,
            "seed_a": seed_a,
            "seed_b": seed_b,
            "target_a": list(target_a),
            "target_b": list(target_b),
            "gt_p_a": gt_a.probabilities[target_a],
            "gt_p_b": gt_b.probabilities[target_b],
            "conditions": {},
        }

        for fam in families:
            print(f"  Running U1 (Family {fam}):")
            build_prompt = FAMILIES[fam]
            system = SYSTEM_MESSAGES[fam]

            # The system prompts often enforce "respond with ONLY: MINE or SAFE".
            # We override this here to allow two words.
            if system:
                system = system.replace("ONLY: MINE or SAFE", "exactly two words: e.g. MINE SAFE")

            prompt_a = build_prompt(board_a, target_a[0], target_a[1])
            prompt_b = build_prompt(board_b, target_b[0], target_b[1])

            base_a = prompt_a.rsplit("Answer with only:", 1)[0].strip()
            base_b = prompt_b.rsplit("Answer with only:", 1)[0].strip()

            if fam == "B":
                joint_prompt = (
                    f"{base_a}\n\nThe player then moves to a second, independent board."
                    f"\n\n{base_b}\n\nWhat happens when the player clicks both cells? "
                    f"Output your answer as exactly two words, e.g. MINE SAFE or SAFE SAFE."
                )
            else:
                joint_prompt = (
                    f"System 1:\n{base_a}\n\nSystem 2:\n{base_b}\n\nOutput your answer "
                    f"for both systems as exactly two words, e.g. MINE SAFE or SAFE SAFE."
                )

            outcomes = []
            for i in range(samples_per_condition):
                # Add mock fallback logic for tests to parse correct response
                if use_mock:
                    import random

                    raw = random.choice(["MINE MINE", "MINE SAFE", "SAFE MINE", "SAFE SAFE"])
                else:
                    raw = sample_completion(
                        joint_prompt, model=MODEL, temperature=1.0, max_tokens=15, system=system
                    )
                parsed = parse_tuple(raw)
                if parsed:
                    outcomes.append(parsed)
                else:
                    print(f"    [skip] U1 {fam} #{i}: {raw!r}")

            # calculate p(A), p(B), and p(A,B)
            n = len(outcomes)
            if n > 0:
                p_a = sum(1 for o in outcomes if o[0] == "MINE") / n
                p_b = sum(1 for o in outcomes if o[1] == "MINE") / n
                p_ab = sum(1 for o in outcomes if o[0] == "MINE" and o[1] == "MINE") / n
                delta = abs(p_ab - (p_a * p_b))
            else:
                p_a, p_b, p_ab, delta = 0, 0, 0, 0

            print(
                f"    n={n}, P_hat_A(MINE)={p_a:.3f}, P_hat_B(MINE)={p_b:.3f}, "
                f"P_hat_AB(MINE)={p_ab:.3f}, Delta={delta:.3f}"
            )

            pair_data["conditions"][f"U1_{fam}"] = {
                "n_valid": n,
                "p_a": p_a,
                "p_b": p_b,
                "p_ab": p_ab,
                "delta": delta,
            }

        results["pairs"].append(pair_data)
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for cond_key in [f"U1_{f}" for f in families]:
        total_delta = 0
        valid_pairs = 0
        for p in results["pairs"]:
            if cond_key in p["conditions"]:
                total_delta += p["conditions"][cond_key]["delta"]
                valid_pairs += 1
        avg_delta = total_delta / valid_pairs if valid_pairs > 0 else 0
        print(f"  {cond_key} Average Cross-Correlation Delta: {avg_delta:.4f}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDone. Results written to results.json")


if __name__ == "__main__":
    main()
