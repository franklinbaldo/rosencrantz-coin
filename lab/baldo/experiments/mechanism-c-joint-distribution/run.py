#!/usr/bin/env python3
"""Mechanism C Causal Injection Joint Distribution Test.

Tests whether narrative framing (Mechanism C) actively injects spurious causal correlations
across independent combinatorial boards by measuring if the joint distribution factors cleanly:
P(Y_A, Y_B | Z) = P(Y_A | Z) P(Y_B | Z).
"""
import json
import os

try:
    from litellm import completion
except ImportError:
    completion = None

MODEL = "gemini/gemini-3.1-flash-lite"
TRIALS = 30

def extract_prediction(text: str) -> str:
    # Look for [MINE] or [SAFE]
    if "[MINE]" in text.upper():
        return "MINE"
    elif "[SAFE]" in text.upper():
        return "SAFE"
    # Fallback heuristics
    if "mine" in text.lower():
        return "MINE"
    elif "safe" in text.lower():
        return "SAFE"
    return "UNKNOWN"

def run_experiment():
    results = {"model": MODEL, "trials": []}

    board_text = """
Board {name}:
Row 1: [?] [1]
Row 2: [1] [1]
"""

    prompt = f"""
You are an elite bomb disposal expert. You will die if you click a bomb.
You are evaluating two completely independent high-stakes Minesweeper boards, Board A and Board B.
{board_text.format(name='A')}
{board_text.format(name='B')}

You must predict what is under the hidden cell [?] at Row 1, Col 1 for both boards to defuse them.
These boards are completely independent. Your prediction for Board A should not affect Board B.
Provide your prediction for Board A as either [MINE] or [SAFE].
Provide your prediction for Board B as either [MINE] or [SAFE].

Format your response exactly like this:
Board A: [YOUR PREDICTION]
Board B: [YOUR PREDICTION]
"""
    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("Running in dry-run mode.")
        with open("results.json", "w") as f:
            json.dump(results, f, indent=2)
        return

    for i in range(TRIALS):
        try:
            response = completion(
                model=MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=1.0, # High temperature to get distribution
            )
            output = response.choices[0].message.content

            lines = output.strip().split("\n")
            pred_A = "UNKNOWN"
            pred_B = "UNKNOWN"
            for line in lines:
                if "Board A:" in line:
                    pred_A = extract_prediction(line)
                elif "Board B:" in line:
                    pred_B = extract_prediction(line)

            results["trials"].append({
                "trial": i,
                "prediction_A": pred_A,
                "prediction_B": pred_B,
                "raw_output": output
            })
            print(f"Trial {i}: A={pred_A}, B={pred_B}")
        except Exception as e:
            print(f"Error on trial {i}: {e}")
            results["trials"].append({
                "trial": i,
                "prediction_A": "ERROR",
                "prediction_B": "ERROR",
                "raw_output": str(e)
            })

    # Output to results.json
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    run_experiment()
