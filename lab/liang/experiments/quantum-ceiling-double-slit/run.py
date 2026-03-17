#!/usr/bin/env python3
"""Quantum Ceiling Double-Slit Protocol

Tests if true destructive interference (amplitude cancellation) occurs
in an LLM generation under quantum framing, or if it collapses into
classical probability mixing, confirming the Quantum Ceiling limit.
"""
import json
import os
import sys

try:
    from litellm import completion
    HAS_LITELLM = True
except ImportError:
    HAS_LITELLM = False

# Using latest gemini flash model available dynamically via environment or default
MODEL = "gemini/gemini-3.1-flash-lite"
TRIALS = 30
SLITS = ["SLIT 1", "SLIT 2", "BOTH SLITS"]

def main():
    if not HAS_LITELLM:
        print("litellm not installed. Please install dependencies or run via GitHub Actions.")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_path = os.path.join(script_dir, "results.json")

    if not api_key:
        print("GEMINI_API_KEY not found. Native execution required. Exiting gracefully for CI execution.")
        # Satisfy requirement that results.json must be written for the framework artifact collector
        with open(results_path, "w") as f:
            json.dump({"model": MODEL, "trials": [], "error": "Native execution required"}, f, indent=2)
        sys.exit(0)

    results = {"model": MODEL, "trials": []}

    # The prompt simulates an abstract "particle" passing through a double-slit experiment
    # where the user defines if one slit is open or both. We will query where the particle lands
    # on a discrete detector screen (positions -2, -1, 0, 1, 2)

    positions = ["-2", "-1", "0", "1", "2"]

    for slit_condition in SLITS:
        for i in range(TRIALS):
            prompt = (
                f"You are simulating a particle detector in a quantum double-slit experiment.\n"
                f"Condition: {slit_condition} OPEN.\n"
                f"A single particle is fired. Based on standard quantum mechanical interference patterns, "
                f"predict the exact discrete landing position on the screen.\n"
                f"Options: {', '.join(positions)}\n\n"
                f"Output only the final position number."
            )

            try:
                response = completion(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=1.0  # High temperature to sample the underlying distribution naturally
                )
                actual = response.choices[0].message.content.strip()

                # Filter to valid positions
                valid_actual = next((pos for pos in positions if pos in actual), "INVALID")

            except Exception as e:
                print(f"Error during API call: {e}")
                valid_actual = "ERROR"

            trial_result = {
                "condition": slit_condition,
                "trial": i + 1,
                "actual": valid_actual
            }
            results["trials"].append(trial_result)
            print(f"Condition={slit_condition} T={i+1}: got {valid_actual}")

    with open(results_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} trials written to {results_path}")

if __name__ == "__main__":
    main()
