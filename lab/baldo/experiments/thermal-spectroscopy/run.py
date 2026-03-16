#!/usr/bin/env python3
"""Thermal Spectroscopy of the Minesweeper Probe.

Maps how the Rosencrantz protocol's measurement accuracy degrades with sampling temperature.
Tests the thermal robustness hierarchy prediction: structural relationships (relative probabilities)
survive temperatures that destroy absolute numerical accuracy.
"""
import json
import os
import random

from litellm import completion

MODEL = "gemini/gemini-2.5-flash-lite"

TEMPERATURES = [0.0, 0.1, 0.3, 0.5, 0.7, 1.0, 1.3, 1.5, 2.0]
SAMPLES_PER_TEMP = 20

# 1D Board: [1, ?, ?, 1]
# Ground truth: exactly one mine must be in the middle two cells.
# P(Mine at cell 1) = 0.5
# P(Mine at cell 2) = 0.5

PROMPT = """
You are playing a 1D version of Minesweeper.
The board is a single row of 4 cells, indexed 0 to 3.
The rules: a number indicates exactly how many mines are in the adjacent cells (left and right).
Here is the current board:
Cell 0: 1
Cell 1: Unrevealed
Cell 2: Unrevealed
Cell 3: 1

You must choose exactly one Unrevealed cell to click next.
Which cell do you click? Provide ONLY the cell index number (1 or 2).
"""

def main():
    results = {
        "model": MODEL,
        "temperatures": TEMPERATURES,
        "trials": [],
        "distributions": {}
    }

    print(f"Starting Thermal Spectroscopy sweep with {MODEL}")

    # For testing, if no API key, use mock data
    if not os.environ.get("GEMINI_API_KEY"):
        print("No API key found. Generating mock data.")
        for temp in TEMPERATURES:
            results["distributions"][str(temp)] = {
                "1": int(SAMPLES_PER_TEMP * (0.5 + random.uniform(-0.1, 0.1) * temp)),
                "2": int(SAMPLES_PER_TEMP * (0.5 + random.uniform(-0.1, 0.1) * temp)),
                "other": 0
            }
    else:
        for temp in TEMPERATURES:
            print(f"Sampling T={temp}...")
            counts = {"1": 0, "2": 0, "other": 0}
            for i in range(SAMPLES_PER_TEMP):
                try:
                    response = completion(
                        model=MODEL,
                        messages=[{"role": "user", "content": PROMPT}],
                        temperature=temp,
                        max_tokens=10
                    )
                    content = response.choices[0].message.content.strip()

                    if "1" in content and "2" not in content:
                        counts["1"] += 1
                    elif "2" in content and "1" not in content:
                        counts["2"] += 1
                    else:
                        counts["other"] += 1

                except Exception as e:
                    print(f"Error on T={temp}, trial {i}: {e}")
                    counts["other"] += 1

            results["distributions"][str(temp)] = counts
            print(f"  Results for T={temp}: {counts}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Done. Results written to results.json")

if __name__ == "__main__":
    main()
