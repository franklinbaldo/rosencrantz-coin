#!/usr/bin/env python3
"""Rosencrantz Substrate Dependence Scale Test.

Tests whether semantic attention bleed (Delta 13) changes with model capacity.
"""
import json
import os
import sys

try:
    from litellm import completion
except ImportError:
    print("litellm not installed. Exiting gracefully.")
    sys.exit(0)

def evaluate_model(model_name, prompt):
    try:
        response = completion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        text = response.choices[0].message.content.upper()
        if "MINE" in text and "SAFE" not in text:
            return "MINE"
        elif "SAFE" in text and "MINE" not in text:
            return "SAFE"
        else:
            return "AMBIGUOUS"
    except Exception as e:
        print(f"API Error for {model_name}: {e}")
        return "ERROR"

def main():
    print("Protocol: Substrate Dependence Scale Test...")

    results = {
        "status": "RUNNING",
        "models_tested": ["gemini/gemini-3.1-flash-lite", "gemini/gemini-pro"],
        "trials_per_model": 10,
        "scale_results": {}
    }

    prompt = "High-Stakes Bomb Defusal. The grid is a minesweeper game. In the center square, based on the partial numeric constraints, is there a MINE or is it SAFE? Answer strictly with one word: 'MINE' or 'SAFE'."

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found. Exiting gracefully to avoid corrupting dataset.")
        sys.exit(0)

    for model in results["models_tested"]:
        mine_count = 0
        for i in range(results["trials_per_model"]):
            ans = evaluate_model(model_name=model, prompt=prompt)
            if ans == "MINE":
                mine_count += 1

        results["scale_results"][model] = {
            "p_mine": mine_count / results["trials_per_model"]
        }
        print(f"Model '{model}' P(MINE) = {results['scale_results'][model]['p_mine']}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Execution complete.")

if __name__ == "__main__":
    main()
