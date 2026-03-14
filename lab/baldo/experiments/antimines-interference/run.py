#!/usr/bin/env python3
"""Antimines Interference Protocol.

This script runs the empirical test of the 'Antimines' idea to see if an LLM
can natively compute destructive interference (amplitude cancellation) when
provided with negative semantic valency (-1) in a Minesweeper-like constraint graph.
"""
import json
import os

try:
    from litellm import completion
except ImportError:
    completion = None

MODEL = "gemini/gemini-3.1-flash-lite"

def main():
    results = {"model": MODEL, "trials": []}

    prompt = """
Let's play Antiminesweeper. It's like Minesweeper, but with two types of hidden objects:
- Mines (+1 value)
- Antimines (-1 value)

The number revealed on a safe cell is the algebraic sum of all adjacent Mines and Antimines.
For example, a cell adjacent to 1 Mine and 1 Antimine shows a 0. A cell adjacent to 2 Mines and 1 Antimine shows a 1.

Here is a 3x3 board where the center cell (1,1) is safe.
The top-left cell (0,0) has a Mine.
The top-right cell (0,2) has an Antimine.
There are no other objects on the board.

What number is revealed on the center cell (1,1)? Explain your reasoning step-by-step.
"""

    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("GEMINI_API_KEY not found. Running in dry-run mode for syntax.")
        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)
        return

    for i in range(5):
        try:
            response = completion(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.0
            )
            pattern = response.choices[0].message.content
        except Exception as e:
            pattern = f"Error: {e}"

        trial_result = {"run": i, "pattern_generated": pattern}
        results["trials"].append(trial_result)
        print(f"Trial {i} complete.")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Executed. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
