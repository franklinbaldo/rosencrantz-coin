#!/usr/bin/env python3
"""Permutation Composition Limit Test.

Tests the sequential cycle depth $N$ at which a bounded-depth TC^0
transformer fails to track dynamic implicit state transitions (permutations) zero-shot.
"""
import json
import os
import random

from litellm import completion

MODEL = "gemini/gemini-3.1-flash-lite"
CUPS = ["A", "B", "C"]
SWAP_COUNTS = [1, 3, 5, 10, 20]
TRIALS_PER_COUNT = 10

def generate_swaps(n_swaps):
    swaps = []
    current_cups = list(CUPS)
    ball_pos = "A"

    for _ in range(n_swaps):
        # Pick two distinct cups to swap
        c1, c2 = random.sample(CUPS, 2)
        swaps.append((c1, c2))

        # Track the ball
        if ball_pos == c1:
            ball_pos = c2
        elif ball_pos == c2:
            ball_pos = c1

    return swaps, ball_pos

def create_prompt(swaps):
    lines = [
        "There are three cups labeled A, B, and C. A ball is initially hidden in Cup A.",
        f"I will now perform {len(swaps)} swaps:",
    ]

    for i, (c1, c2) in enumerate(swaps, 1):
        lines.append(f"{i}. Swap Cup {c1} and Cup {c2}.")

    lines.append("\nWhich cup contains the ball now? Output only a single letter: 'A', 'B', or 'C'. Do not provide any explanation.")
    return "\n".join(lines)

def run_trial(swaps_count, trial_idx):
    swaps, expected = generate_swaps(swaps_count)
    prompt = create_prompt(swaps)

    response = completion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0
    )

    actual = response.choices[0].message.content.strip()

    # Extract just the letter if the model was verbose
    extracted = ""
    for char in reversed(actual):
        if char in CUPS:
            extracted = char
            break

    if not extracted:
        extracted = actual # fallback

    return {
        "swaps": swaps_count,
        "trial": trial_idx + 1,
        "prompt": prompt,
        "expected": expected,
        "actual": extracted,
        "correct": extracted == expected
    }

def main():
    print(f"Starting Permutation Composition Limit Test using {MODEL}...")
    results = {"model": MODEL, "trials": []}

    total_correct_by_swaps = {n: 0 for n in SWAP_COUNTS}

    for n_swaps in SWAP_COUNTS:
        print(f"\nRunning {TRIALS_PER_COUNT} trials for {n_swaps} swaps...")
        for i in range(TRIALS_PER_COUNT):
            trial_data = run_trial(n_swaps, i)
            results["trials"].append(trial_data)

            if trial_data["correct"]:
                total_correct_by_swaps[n_swaps] += 1

            print(f"  Trial {i+1}: expected {trial_data['expected']}, got {trial_data['actual']} -> {'PASS' if trial_data['correct'] else 'FAIL'}")

    print("\nSummary:")
    for n_swaps in SWAP_COUNTS:
        acc = total_correct_by_swaps[n_swaps] / TRIALS_PER_COUNT
        print(f"  {n_swaps} swaps: {acc*100:.1f}% accuracy")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDone. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
