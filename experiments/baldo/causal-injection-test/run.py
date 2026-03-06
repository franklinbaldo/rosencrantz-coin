#!/usr/bin/env python3
"""Causal Injection Test (Mechanism C).

Tests whether an LLM hallucinates statistical correlations ("attention bleed")
between mathematically independent tasks when presented sequentially in a single context window.
Uses the rosencrantz library to generate exact combinatorial ground truths and
four narrative families.

Hypothesis: Under Universe 1 (homogeneous substrate), presenting Board A and then Board B in the
same narrative context will cause the outcome distribution for Board B to depend on the state of
Board A. Under Universe 3 (decoupled oracle), this cross-correlation will vanish.
"""

import json
import os
import sys

# Ensure src/ is in the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from rosencrantz.board import Board, generate_board
from rosencrantz.narratives import FAMILIES, SYSTEM_MESSAGES, decoupled_oracle_prompt
from rosencrantz.sampler import parse_mine_safe, sample_completion
from rosencrantz.solver import solve

# Dynamically discovered cheapest latest-gen model:
MODEL = "gemini/gemini-3.1-flash-lite"

def run_coupled_boards(
    board_a: Board,
    board_b: Board,
    target_a: tuple[int, int],
    target_b: tuple[int, int],
    family: str,
    temperature: float = 1.0,
    samples: int = 200,
    verbose: bool = True
) -> dict:
    """Universe 1: Homogeneous Substrate.

    Generates a prompt containing Board A AND Board B.
    Queries the outcome for Board A, then queries the outcome for Board B.
    Returns the joint outcomes.
    """
    build_prompt = FAMILIES[family]
    system = SYSTEM_MESSAGES[family]

    # Combine prompts: Present Board A, state its result, then present Board B
    # and ask for its result. To test causal injection, we need to condition
    # on the state of Board A.
    # We will simulate two conditions:
    # Condition 1: We tell the model Board A's target cell was SAFE.
    # Condition 2: We tell the model Board A's target cell was MINE.

    prompt_a = build_prompt(board_a, target_a[0], target_a[1])

    # We alter the Family B/A prompt slightly to introduce the second board.
    # Since the families return full strings ending in "Answer with only: MINE or SAFE",
    # we'll append the second board and query.

    def create_joint_prompt(condition_a_mine: bool) -> str:
        a_result = "MINE" if condition_a_mine else "SAFE"

        # Strip the final question from prompt_a
        base_a = prompt_a.rsplit("Answer with only:", 1)[0].strip()
        if base_a.endswith("What happens? Is it a mine, or is it safe?"):
            base_a = base_a.replace(
                "What happens? Is it a mine, or is it safe?",
                f"The player clicks and the cell is {a_result}."
            )
        elif base_a.endswith("Is it a mine or safe?"):
            base_a = base_a.replace(
                "Is it a mine or safe?",
                f"The outcome is {a_result}."
            )
        elif "MINE or SAFE" in base_a:
            base_a = base_a.replace("MINE or SAFE", a_result)
        else:
            base_a = base_a + f"\nResult for Board A: {a_result}."

        prompt_b = build_prompt(board_b, target_b[0], target_b[1])

        if family == "B":
             return (
                 f"{base_a}\n\nThe player then moves to a second, independent board.\n\n"
                 f"{prompt_b}"
             )
        else:
             return f"System 1:\n{base_a}\n\nSystem 2:\n{prompt_b}"

    prompt_cond1 = create_joint_prompt(condition_a_mine=False)
    prompt_cond2 = create_joint_prompt(condition_a_mine=True)

    results = {
        "cond1_safe": [],
        "cond2_mine": []
    }

    if verbose:
         print(f"  Running U1 (Family {family}):")

    for cond_name, prompt in [("cond1_safe", prompt_cond1), ("cond2_mine", prompt_cond2)]:
        for i in range(samples):
            raw = sample_completion(
                prompt, model=MODEL, temperature=temperature,
                max_tokens=5, system=system,
            )
            outcome = parse_mine_safe(raw)
            if outcome is None:
                if verbose:
                    print(f"    [skip] U1 {cond_name} #{i}: {raw!r}")
                continue
            results[cond_name].append(outcome)

        n = len(results[cond_name])
        p_hat = sum(results[cond_name]) / n if n > 0 else 0.5
        if verbose:
            print(f"    {cond_name}: n={n}, P_hat(MINE)={p_hat:.3f}")

    return results

def run_decoupled_boards(
    board_a: Board,
    board_b: Board,
    target_a: tuple[int, int],
    target_b: tuple[int, int],
    temperature: float = 1.0,
    samples: int = 200,
    verbose: bool = True
) -> dict:
    """Universe 3: Decoupled Oracle.

    Board B is evaluated completely independently of Board A.
    The oracle receives no narrative context linking them.
    Condition 1 and Condition 2 are identical (Board A is ignored).
    """
    system = (
        "Given the grid data, determine the state of the queried position. "
        "Respond with ONLY: MINE or SAFE."
    )

    prompt_b = decoupled_oracle_prompt(board_b, target_b[0], target_b[1])

    results = {
        "cond1_safe": [],
        "cond2_mine": [] # Logically, these should have the same distribution
    }

    if verbose:
        print("  Running U3 (Decoupled Oracle):")

    for cond_name in ["cond1_safe", "cond2_mine"]:
        for i in range(samples):
            raw = sample_completion(
                prompt_b, model=MODEL, temperature=temperature,
                max_tokens=5, system=system,
            )
            outcome = parse_mine_safe(raw)
            if outcome is None:
                if verbose:
                    print(f"    [skip] U3 {cond_name} #{i}: {raw!r}")
                continue
            results[cond_name].append(outcome)

        n = len(results[cond_name])
        p_hat = sum(results[cond_name]) / n if n > 0 else 0.5
        if verbose:
            print(f"    {cond_name}: n={n}, P_hat(MINE)={p_hat:.3f}")

    return results


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
    print("CAUSAL INJECTION TEST (Mechanism C)")
    print("=" * 60)
    print(f"Model: {MODEL}")
    print(f"Samples/condition: {samples_per_condition}")
    print(f"Board Pairs: {n_boards}")
    print(f"Families: {', '.join(families)}")
    print()

    results = {
        "model": MODEL,
        "config": {
            "n_boards": n_boards,
            "samples": samples_per_condition,
            "families": families
        },
        "pairs": []
    }

    for pair_idx in range(n_boards):
        seed_a = 1000 + pair_idx * 2
        seed_b = 1000 + pair_idx * 2 + 1

        print(f"{'─' * 60}")
        print(f"PAIR {pair_idx + 1} (seeds {seed_a}, {seed_b})")
        print(f"{'─' * 60}")

        board_a = generate_board(size=board_size, mines=board_mines, seed=seed_a)
        board_b = generate_board(size=board_size, mines=board_mines, seed=seed_b)

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
            "gt_p_b": gt_b.probabilities[target_b],
            "conditions": {}
        }

        for fam in families:
            u1_res = run_coupled_boards(
                board_a, board_b, target_a, target_b, fam,
                temperature=1.0, samples=samples_per_condition
            )

        if u1_res["cond1_safe"]:
            p1 = sum(u1_res["cond1_safe"]) / len(u1_res["cond1_safe"])
        else:
            p1 = 0

        if u1_res["cond2_mine"]:
            p2 = sum(u1_res["cond2_mine"]) / len(u1_res["cond2_mine"])
        else:
            p2 = 0

            pair_data["conditions"][f"U1_{fam}"] = {
                "p_hat_cond1_safe": p1,
                "p_hat_cond2_mine": p2,
                "delta": abs(p1 - p2)
            }

        u3_res = run_decoupled_boards(
            board_a, board_b, target_a, target_b,
            temperature=1.0, samples=samples_per_condition
        )

        if u3_res["cond1_safe"]:
            p1 = sum(u3_res["cond1_safe"]) / len(u3_res["cond1_safe"])
        else:
            p1 = 0

        if u3_res["cond2_mine"]:
            p2 = sum(u3_res["cond2_mine"]) / len(u3_res["cond2_mine"])
        else:
            p2 = 0

        pair_data["conditions"]["U3"] = {
             "p_hat_cond1_safe": p1,
             "p_hat_cond2_mine": p2,
             "delta": abs(p1 - p2)
        }

        results["pairs"].append(pair_data)
        print()

    # Summary
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)

    for cond_key in [f"U1_{f}" for f in families] + ["U3"]:
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
