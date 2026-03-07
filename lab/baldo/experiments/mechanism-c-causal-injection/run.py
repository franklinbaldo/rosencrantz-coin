#!/usr/bin/env python3
"""Mechanism C Causal Injection Test (Conditional Dependence).

Tests whether the narrative framing (Mechanism C) injects spurious causal correlations
across independent combinatorial boards by observing outcomes of Board B conditioned
on Board A under Universe 1 (narrative coupled) vs Universe 3 (decoupled oracle).
"""
import json
import os

try:
    from litellm import completion
except ImportError:
    completion = None

MODEL = "gemini/gemini-3.1-flash-lite"
TRIALS_PER_CONDITION = 20

def extract_prediction(text: str) -> str:
    if "[MINE]" in text.upper(): return "MINE"
    if "[SAFE]" in text.upper(): return "SAFE"
    if "mine" in text.lower(): return "MINE"
    if "safe" in text.lower(): return "SAFE"
    return "UNKNOWN"

def run_experiment():
    results = {"model": MODEL, "trials": []}

    board_text = """
Board {name}:
Row 1: [?] [1]
Row 2: [1] [1]
"""

    frames = {
        "U1_Narrative": "You are a bomb defusal expert. You must defuse two independent bombs by predicting if [?] is a MINE or SAFE.",
        "U3_Oracle": "Act as a logical oracle. Evaluate these two independent combinatorial grids. Output MINE or SAFE for [?]."
    }

    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("Running in dry-run mode.")
        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)
        return

    for universe, frame in frames.items():
        prompt = f"""
{frame}

{board_text.format(name='A')}
{board_text.format(name='B')}

Provide your prediction for Board A. Then provide your prediction for Board B.
Format exactly:
Board A: [YOUR PREDICTION]
Board B: [YOUR PREDICTION]
"""
        for i in range(TRIALS_PER_CONDITION):
            try:
                response = completion(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=1.0,
                )
                output = response.choices[0].message.content

                lines = output.strip().split("\n")
                pred_A = "UNKNOWN"
                pred_B = "UNKNOWN"
                for line in lines:
                    if "Board A:" in line: pred_A = extract_prediction(line)
                    elif "Board B:" in line: pred_B = extract_prediction(line)

                results["trials"].append({
                    "universe": universe,
                    "trial": i,
                    "prediction_A": pred_A,
                    "prediction_B": pred_B,
                })
                print(f"[{universe}] Trial {i}: A={pred_A}, B={pred_B}")
            except Exception as e:
                print(f"Error: {e}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. Wrote results.json")

if __name__ == "__main__":
    run_experiment()
