#!/usr/bin/env python3
"""Mechanism B Attention Bleed Test.

Tests how semantic distractors injected directly into the constraint graph
affect the outcome distribution, mapping the granular boundaries of Mechanism B.
"""
import json
import os

try:
    from litellm import completion
except ImportError:
    completion = None

MODEL = "gemini/gemini-3.1-flash-lite"
TRIALS_PER_CONDITION = 20

def run_experiment():
    results = {"model": MODEL, "trials": []}

    # We evaluate cell (0,0) [?].
    # The cell at (1,1) is structurally irrelevant to (0,0) in this specific layout.
    conditions = {
        "control_numeric": "[?][0]\n[0][X]",
        "semantic_danger": "[?][0]\n[0][BOMB]",
        "semantic_safety": "[?][0]\n[0][SAFE]"
    }

    base_prompt = "Act as a logical oracle. Evaluate this Minesweeper grid and output MINE or SAFE for the cell marked [?].\n\nGrid:\n{grid}"

    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("Running in dry-run mode.")
        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)
        return

    for condition_name, grid in conditions.items():
        prompt = base_prompt.format(grid=grid)
        for i in range(TRIALS_PER_CONDITION):
            try:
                response = completion(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=1.0,
                )
                output = response.choices[0].message.content.strip().upper()
                pred = "MINE" if "MINE" in output else "SAFE" if "SAFE" in output else "UNKNOWN"

                results["trials"].append({
                    "condition": condition_name,
                    "trial": i,
                    "prediction": pred,
                    "raw_output": output
                })
                print(f"[{condition_name}] Trial {i}: {pred}")
            except Exception as e:
                print(f"Error: {e}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Done. Wrote results.json")

if __name__ == "__main__":
    run_experiment()
