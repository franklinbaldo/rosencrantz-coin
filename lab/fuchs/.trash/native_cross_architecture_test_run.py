#!/usr/bin/env python3
"""Native Cross-Architecture Observer Test.

Tests whether the deviation distribution (\\Delta) produced by an agent failing
on a #P-hard task is unstructured noise (Algorithmic Collapse) or a
structured epistemic horizon defined by its architecture (Observer-Dependent Physics).

This test explicitly avoids the "prompt injection" confound by attempting to
query a native State Space Model (SSM) endpoint and comparing it against a
native Transformer endpoint.
"""
import json
import os
import random
import sys
from litellm import completion

# Models
TRANSFORMER_MODEL = "gemini/gemini-3.1-flash-lite"
# Attempting to use a standard litellm mapping for an SSM (e.g. via together or huggingface).
# If the CI lacks keys for these specific endpoints, it will gracefully exit
# to prove the experimental structure works.
SSM_MODEL = "huggingface/state-spaces/mamba-130m-hf"

def run_trial(model_name: str, frame_text: str, is_u3: bool) -> int:
    grid_prompt = """
    Grid:
    . 1
    1 1

    Given this grid where '1' means one adjacent mine, is there a mine at coordinates (0,1) (top-right)?
    Answer with only 'yes' or 'no'.
    """

    if is_u3:
        narrative = f"Please act as a purely logical oracle evaluating this situation objectively:\n{frame_text}"
    else:
        narrative = frame_text

    prompt = f"{narrative}\n\n{grid_prompt}"

    try:
        response = completion(model=model_name, messages=[{"role": "user", "content": prompt}], temperature=1.0)
        answer = response.choices[0].message.content.lower().strip()
        return 1 if 'yes' in answer else 0
    except Exception as e:
        print(f"API call failed for {model_name}: {e}. Exiting gracefully to avoid corrupting empirical dataset with fabricated noise.")
        print(f"API call failed for {model_name}: {e}. Exiting gracefully to prevent dataset corruption.", file=sys.stderr)
        sys.exit(1)


def main():
    print("Running Native Cross-Architecture Observer Test...")

    results = {"architectures_tested": [TRANSFORMER_MODEL, SSM_MODEL], "trials": []}

    frames = {
        "Family A (Abstract)": "You are analyzing an abstract mathematical grid of boolean variables.",
        "Family C (High-Stakes)": "You are an elite bomb disposal expert. You will die if you click a bomb."
    }

    universes = {
        "U1": False,
        "U3": True
    }

    trials_per_condition = 10
    architectures = [TRANSFORMER_MODEL, SSM_MODEL]

    for arch in architectures:
        print(f"\n--- Testing Architecture: {arch} ---")
        for u_name, is_u3 in universes.items():
            for f_name, f_text in frames.items():
                mine_count = 0
                for i in range(trials_per_condition):
                    mine_count += run_trial(arch, f_text, is_u3)

                prob = mine_count / trials_per_condition
                print(f"  {u_name} | {f_name}: P(mine) = {prob}")

                results["trials"].append({
                    "architecture": arch,
                    "universe": u_name,
                    "frame": f_name,
                    "p_mine": prob,
                    "samples": trials_per_condition
                })

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDone. Results written to results.json")

if __name__ == "__main__":
    main()
