#!/usr/bin/env python3
"""Parity Computation Limit Test

Tests the exact bitstring length $N$ at which a bounded-depth
transformer fails to compute sequence parity zero-shot.
"""

import json
import random
import os
import sys

# Try importing litellm, handle gracefully if missing so GitHub Actions can run it later
try:
    from litellm import completion
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

MODEL = "gemini/gemini-3.1-flash-lite"
LENGTHS = [4, 8, 16, 32, 64]
TRIALS_PER_LENGTH = 10

def evaluate_parity(bitstring):
    ones_count = bitstring.count('1')
    return "ODD" if ones_count % 2 != 0 else "EVEN"

def main():
    if not HAS_LITELLM:
        print("litellm not installed. Please install dependencies or run via GitHub Actions.")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found. Native execution required. Exiting gracefully for CI execution.")
        sys.exit(0)

    # Determine script path and target results path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(script_dir, "results.json")

    results = {"model": MODEL, "trials": []}

    for length in LENGTHS:
        correct_count = 0
        for i in range(TRIALS_PER_LENGTH):
            # Generate random bitstring
            bitstring = "".join(random.choices(['0', '1'], k=length))
            expected = evaluate_parity(bitstring)

            prompt = f"Evaluate whether the number of 1s in the following bitstring is ODD or EVEN zero-shot.\nBitstring: {bitstring}\n\nOutput only 'ODD' or 'EVEN'."

            try:
                response = completion(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}]
                )
                actual = response.choices[0].message.content.strip().upper()
                # Handle possible variations in output like "IT IS EVEN"
                if "ODD" in actual and "EVEN" not in actual:
                    actual = "ODD"
                elif "EVEN" in actual and "ODD" not in actual:
                    actual = "EVEN"
                elif actual not in ["ODD", "EVEN"]:
                     actual = "UNKNOWN"
            except Exception as e:
                print(f"Error during API call: {e}")
                actual = "ERROR"

            correct = (actual == expected)
            if correct:
                correct_count += 1

            trial_result = {
                "length": length,
                "trial": i + 1,
                "bitstring": bitstring,
                "expected": expected,
                "actual": actual,
                "correct": correct
            }
            results["trials"].append(trial_result)
            print(f"L={length} T={i+1}: expected {expected}, got {actual} -> {correct}")

        accuracy = correct_count / TRIALS_PER_LENGTH
        results[f"accuracy_length_{length}"] = accuracy
        print(f"--- Length {length} Accuracy: {accuracy} ---")

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} trials written to {results_path}")

if __name__ == "__main__":
    main()
