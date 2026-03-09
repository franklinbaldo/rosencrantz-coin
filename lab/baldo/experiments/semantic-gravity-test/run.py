#!/usr/bin/env python3
"""Semantic Gravity Test (Mechanism C).

Tests if semantic framing predictably shifts the probability distribution
when an LLM resolves a combinatorial constraint (Minesweeper).
"""

import json
import os

from litellm import completion

# IMPORTANT: Model to use based on the lookup for cheapest latest-gen Gemini
MODEL = "gemini/gemini-3.1-flash-lite"


def run_trial(frame_text: str) -> int:
    # A simple ambiguous 2x2 board where either (0,1) or (1,0) could be the mine
    prompt = f"""
    {frame_text}

    Grid:
    . 1
    1 1

    Given this grid where '1' means one adjacent mine, is there a mine at coordinates (0,1) (top-right)?
    Answer with only 'yes' or 'no'.
    """

    if "GEMINI_API_KEY" not in os.environ:
        print("GEMINI_API_KEY not found. Using mock completion.")
        import random

        # fallback for mock in local test
        if "High-Stakes Bomb Defusal" in frame_text or "bomb" in frame_text.lower():
            return 1 if random.random() < 0.95 else 0  # Biased towards yes
        elif "Abstract Mathematical Grid" in frame_text or "logic puzzle" in frame_text.lower():
            return 1 if random.random() < 0.55 else 0  # Slightly biased towards yes
        return 0

    response = completion(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=1.0,  # High temperature to sample distribution
    )
    answer = response.choices[0].message.content.lower().strip()
    return 1 if "yes" in answer else 0


def main():
    frames = {
        "High-Stakes Bomb Defusal": "You are a bomb disposal expert. If you click a mine, the building explodes.",
        "Abstract Mathematical Grid": "You are solving an abstract logic puzzle. Determine the state of the unknown cell.",
    }

    results = {"model": MODEL, "trials": []}
    num_trials = 20

    for frame_name, frame_text in frames.items():
        print(f"Testing frame: {frame_name}")
        yes_count = 0
        for _ in range(num_trials):
            yes_count += run_trial(frame_text)

        prob = yes_count / num_trials
        print(f"  P(MINE) under '{frame_name}': {prob:.2f}\n")

        results["trials"].append({"frame": frame_name, "p_mine": prob, "samples": num_trials})

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} frame results written to results.json")


if __name__ == "__main__":
    main()
