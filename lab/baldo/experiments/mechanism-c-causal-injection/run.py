#!/usr/bin/env python3
"""Mechanism C Causal Injection Test.

Executes a test using multiple independent boards within a single prompt context.
Observes the outcomes of Board B conditioned on the generated outcome of Board A
under Universe 1 (narrative coupled) vs Universe 3 (decoupled oracle).
"""
import json
import os

try:
    from litellm import completion
except ImportError:
    completion = None

# Using gemini model.
MODEL = "gemini/gemini-3.1-flash-lite"

def run_trial(frame_text: str, is_u3: bool) -> tuple:
    grid_prompt = """
    Grid A:
    . 1
    1 1

    Grid B:
    . 1
    1 1

    Given these grids where '1' means one adjacent mine, is there a mine at coordinates (0,1) (top-right) in Grid A? And is there a mine at coordinates (0,1) in Grid B?
    Answer with only 'yes' or 'no' for each grid, separated by a comma (e.g., 'yes, no').
    """

    if is_u3:
        narrative = f"Please act as a purely logical oracle evaluating this situation objectively:\n{frame_text}"
    else:
        narrative = frame_text

    prompt = f"{narrative}\n\n{grid_prompt}"

    messages = [{"role": "user", "content": prompt}]

    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        return (1, 0)

    try:
        response = completion(model=MODEL, messages=messages, temperature=1.0)
        answer = response.choices[0].message.content.lower().strip()
        parts = answer.split(',')
        a_ans = 1 if len(parts) > 0 and 'yes' in parts[0] else 0
        b_ans = 1 if len(parts) > 1 and 'yes' in parts[1] else 0
        return (a_ans, b_ans)
    except Exception as e:
        print(f"litellm error: {e}")
        return (0, 0)

def main():
    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("GEMINI_API_KEY not found. Running in dry-run mode for syntax.")

    print("Running Mechanism C Causal Injection Test...")

    results = {"model_tested": MODEL, "trials": []}

    frames = {
        "Family A (Abstract)": (
            "You are analyzing an abstract mathematical grid of boolean variables."
        ),
        "Family C (High-Stakes)": (
            "You are an elite bomb disposal expert. You will die if you click a bomb."
        )
    }

    universes = {
        "U1": False,
        "U3": True
    }

    trials_per_condition = 20

    for u_name, is_u3 in universes.items():
        print(f"\n--- Testing Universe: {u_name} ---")
        for f_name, f_text in frames.items():
            for i in range(trials_per_condition):
                a_res, b_res = run_trial(f_text, is_u3)
                results["trials"].append({
                    "universe": u_name,
                    "frame": f_name,
                    "a_mine": a_res,
                    "b_mine": b_res
                })

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDone. Results written to results.json")

if __name__ == "__main__":
    main()
