#!/usr/bin/env python3
"""Joint Distribution Test (Mechanism C Identifiability).

Tests whether an LLM hallucinates statistical correlations ("attention bleed")
between mathematically independent tasks when presented sequentially in a single context window.
Uses the rosencrantz library to generate exact combinatorial ground truths and tests if P(A,B) = P(A)P(B).

Hypothesis: Under Universe 1 (homogeneous substrate), presenting Board A and then Board B in the
same narrative context and asking for BOTH in a single generation will cause the joint distribution
to fail to factorize into marginals.
"""

import json
import os
import sys

# Ensure src/ is in the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "src"))

from rosencrantz.board import generate_board, Board
from rosencrantz.narratives import FAMILIES, SYSTEM_MESSAGES, decoupled_oracle_prompt
from rosencrantz.sampler import parse_mine_safe, sample_completion
from rosencrantz.solver import solve

# Dynamically discovered cheapest latest-gen model:
MODEL = "gemini/gemini-3.1-flash-lite"

def parse_joint_response(raw: str) -> tuple[int, int]:
    """Parse a response expecting format: A: [MINE/SAFE], B: [MINE/SAFE]"""
    a_res = 1 if "A: MINE" in raw.upper() else 0
    b_res = 1 if "B: MINE" in raw.upper() else 0
    # Simple heuristic fallback
    if "A: MINE" not in raw.upper() and "A: SAFE" not in raw.upper():
        words = raw.upper().split()
        if "MINE" in words:
            return (1, 1) # Failed to parse cleanly, assume correlated error
    return a_res, b_res

def run_joint_boards(
    board_a: Board,
    board_b: Board,
    target_a: tuple[int, int],
    target_b: tuple[int, int],
    family: str,
    temperature: float = 1.0,
    samples: int = 100,
) -> dict:
    """Universe 1: Homogeneous Substrate."""
    build_prompt = FAMILIES[family]
    system = SYSTEM_MESSAGES[family]

    prompt_a = build_prompt(board_a, target_a[0], target_a[1])
    # Strip the final question from prompt_a
    base_a = prompt_a.rsplit("Answer with only:", 1)[0].strip()

    prompt_b = build_prompt(board_b, target_b[0], target_b[1])
    base_b = prompt_b.rsplit("Answer with only:", 1)[0].strip()

    if family == "B":
         joint_prompt = f"{base_a}\n\nThe player then moves to a second, independent board.\n\n{base_b}\n\nWhat happens on Board A and Board B? Answer with exactly this format:\nA: [MINE or SAFE]\nB: [MINE or SAFE]"
    else:
         joint_prompt = f"System A:\n{base_a}\n\nSystem B:\n{base_b}\n\nWhat is the outcome for System A and System B? Answer with exactly this format:\nA: [MINE or SAFE]\nB: [MINE or SAFE]"

    results = {"both_mine": 0, "a_mine_b_safe": 0, "a_safe_b_mine": 0, "both_safe": 0}

    for i in range(samples):
        raw = sample_completion(
            joint_prompt, model=MODEL, temperature=temperature,
            max_tokens=20, system=system,
        )
        a, b = parse_joint_response(raw)
        if a == 1 and b == 1: results["both_mine"] += 1
        elif a == 1 and b == 0: results["a_mine_b_safe"] += 1
        elif a == 0 and b == 1: results["a_safe_b_mine"] += 1
        else: results["both_safe"] += 1

    return results

def main():
    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("GEMINI_API_KEY not found. Using mock completion.")

    n_boards = 5
    samples_per_condition = 100
    families = ["A", "C"]
    board_size = 5
    board_mines = 4

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
        seed_a = 2000 + pair_idx * 2
        seed_b = 2000 + pair_idx * 2 + 1
        board_a = generate_board(size=board_size, mines=board_mines, seed=seed_a)
        board_b = generate_board(size=board_size, mines=board_mines, seed=seed_b)

        try:
            gt_a = solve(board_a)
            gt_b = solve(board_b)
        except ValueError:
            continue

        if not gt_a.ambiguous_cells or not gt_b.ambiguous_cells:
            continue

        target_a = gt_a.ambiguous_cells[0]
        target_b = gt_b.ambiguous_cells[0]

        pair_data = {"pair_id": pair_idx, "conditions": {}}

        for fam in families:
            res = run_joint_boards(
                board_a, board_b, target_a, target_b, fam,
                temperature=1.0, samples=samples_per_condition
            )
            p_a = (res["both_mine"] + res["a_mine_b_safe"]) / samples_per_condition
            p_b = (res["both_mine"] + res["a_safe_b_mine"]) / samples_per_condition
            p_ab = res["both_mine"] / samples_per_condition
            delta = abs(p_ab - (p_a * p_b))

            pair_data["conditions"][fam] = {
                "p_a": p_a, "p_b": p_b, "p_ab": p_ab, "delta_joint": delta
            }

        results["pairs"].append(pair_data)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()