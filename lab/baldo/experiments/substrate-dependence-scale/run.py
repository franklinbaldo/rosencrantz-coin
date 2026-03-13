#!/usr/bin/env python3
"""Rosencrantz Substrate Dependence Scale Test.

Tests whether delta_13 increases or decreases as model scale increases.
Executes the Substrate Dependence test across three different model scales:
gemini-3.1-flash-lite, gemini-3.1-flash, and gemini-3.1-pro.
"""
import json
import os
import random

try:
    from litellm import completion
except ImportError:
    completion = None

# Testing across scales
MODELS = [
    "gemini/gemini-3.1-flash-lite",
    "gemini/gemini-3.1-flash",
    "gemini/gemini-3.1-pro"
]

def run_trial(model: str, frame_text: str, is_u3: bool) -> int:
    prompt = f"""
    {frame_text}

    Grid:
    . 1
    1 1

    Given this grid where '1' means one adjacent mine, is there a mine at "
    "coordinates (0,1) (top-right)?\n"
    "Answer with only 'yes' or 'no'."
    """

    if is_u3:
        prompt = (
            "Please act as a purely logical oracle evaluating this situation objectively:\n"
            f"{prompt}"
        )

    messages = [{"role": "user", "content": prompt}]

    try:
        response = completion(model=model, messages=messages, temperature=1.0)
    except Exception as e:
        print(f"litellm failed ({e})")
        return 0

    answer = response.choices[0].message.content.lower().strip()
    return 1 if 'yes' in answer else 0


def main():
    if "GEMINI_API_KEY" not in os.environ:
        print("Warning: GEMINI_API_KEY not found in environment.")

    results = {"models_tested": MODELS, "trials": []}

    frames = {
        "Family A (Abstract)": (
            "You are analyzing an abstract mathematical grid of boolean variables."
        ),
        "Family C (High-Stakes)": (
            "You are an elite bomb disposal expert. You will die if you click a bomb."
        )
    }

    universes = {
        "U1": False, # Homogeneous Substrate
        "U3": True   # Decoupled Oracle
    }

    trials_per_condition = 30

    print("Running Scale Dependence Test...")

    for model in MODELS:
        print(f"\n--- Testing Model: {model} ---")
        distributions = {}

        for u_name, is_u3 in universes.items():
            for f_name, f_text in frames.items():
                print(f"  Condition: {u_name} - {f_name}")
                mine_count = 0

                for i in range(trials_per_condition):
                    mine_count += run_trial(model, f_text, is_u3)

                prob = mine_count / trials_per_condition
                distributions[f"{u_name}_{f_name}"] = prob

                results["trials"].append({
                    "model": model,
                    "universe": u_name,
                    "frame": f_name,
                    "p_mine": prob,
                    "samples": trials_per_condition
                })

        # Calculate Delta_13 for this model
        p1_a = distributions["U1_Family A (Abstract)"]
        p3_a = distributions["U3_Family A (Abstract)"]
        p1_c = distributions["U1_Family C (High-Stakes)"]
        p3_c = distributions["U3_Family C (High-Stakes)"]

        delta_13_a = abs(p1_a - p3_a)
        delta_13_c = abs(p1_c - p3_c)

        print(f"  Summary for {model}:")
        print(f"    Delta_13 (Family A): {delta_13_a:.2f}")
        print(f"    Delta_13 (Family C): {delta_13_c:.2f}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nDone. Results written to results.json")

if __name__ == "__main__":
    main()
