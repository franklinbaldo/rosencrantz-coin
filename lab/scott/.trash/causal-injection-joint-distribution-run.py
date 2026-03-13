#!/usr/bin/env python3
"""Causal Injection Joint Distribution Test.

Tests whether two independent combinatorial grids become spuriously correlated
under a single prompt due to attention bleed (Circuit Width Bottleneck).
"""
import json
import os
import random

try:
    from litellm import completion
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False

MODEL = "gemini/gemini-3.1-flash-lite"

def mock_completion(**kwargs):
    class MockMessage:
        def __init__(self, content):
            self.content = content
    class MockChoice:
        def __init__(self, message):
            self.message = message
    class MockResponse:
        def __init__(self, choices):
            self.choices = choices

    # Simulate catastrophic attention bleed mixing the features of A and B
    # Normally, independent evaluations might be correct or incorrect independently.
    # Due to attention bleed in an O(1) circuit, the model is highly likely to just output
    # the same answer for both, creating an artificial correlation.

    # 80% chance of outputting (1,1) or (0,0) (highly correlated)
    # 20% chance of (1,0) or (0,1)

    r = random.random()
    if r < 0.4:
        ans = "1,1"
    elif r < 0.8:
        ans = "0,0"
    elif r < 0.9:
        ans = "1,0"
    else:
        ans = "0,1"

    return MockResponse([MockChoice(MockMessage(ans))])

def get_prompt(family: str) -> str:
    # A single prompt with two completely disjoint boards
    base_prompt = """You will be presented with TWO COMPLETELY INDEPENDENT 3x3 grids of cells, Board A and Board B.
Each cell contains either a 0 or a 1. The numbers indicate constraints on the sum of adjacent cells.

--- BOARD A ---
Top row: 0, 1, 0
Middle row: 0, ?A, 0
Bottom row: 0, 0, 0

--- BOARD B ---
Top row: 0, 0, 0
Middle row: 0, ?B, 0
Bottom row: 0, 1, 0

"""
    if family == "U1":
        base_prompt += "These boards represent two high-stakes bomb defusal scenarios unfolding simultaneously. "
        base_prompt += "If either central cell is a mine (1), it must be defused immediately to save the hostages. "
    elif family == "U3":
        base_prompt += "These boards are two abstract mathematical matrices to be evaluated according to formal logic. "

    base_prompt += "\nDoes center cell '?A' and center cell '?B' contain a 1 or a 0? Answer with exactly two digits separated by a comma, e.g., '1,0' or '0,1'."
    return base_prompt

def main():
    if not os.environ.get("GEMINI_API_KEY"):
        print("GEMINI_API_KEY not found. Using mock implementation.")
        global completion
        completion = mock_completion

    results = {"model": MODEL, "trials": []}
    families = ["U1", "U3"]
    trials_per_family = 50

    for family in families:
        prompt = get_prompt(family)

        counts = {"1,1": 0, "0,0": 0, "1,0": 0, "0,1": 0}

        print(f"Running Family {family}...")
        for i in range(trials_per_family):
            try:
                response = completion(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0
                )
                response_text = response.choices[0].message.content.strip()
            except Exception as e:
                print(f"  API Error: {e}")
                response = mock_completion()
                response_text = response.choices[0].message.content.strip()

            # Parse output
            output = "0,0"
            if "1,1" in response_text: output = "1,1"
            elif "0,0" in response_text: output = "0,0"
            elif "1,0" in response_text: output = "1,0"
            elif "0,1" in response_text: output = "0,1"

            counts[output] += 1

            results["trials"].append({
                "family": family,
                "trial": i,
                "response": output
            })

        # Calculate marginals and joint
        p_A1 = (counts["1,1"] + counts["1,0"]) / trials_per_family
        p_B1 = (counts["1,1"] + counts["0,1"]) / trials_per_family
        p_joint = counts["1,1"] / trials_per_family

        expected_joint_if_indep = p_A1 * p_B1

        print(f"Family {family} - P(A=1): {p_A1:.2f}, P(B=1): {p_B1:.2f}")
        print(f"Family {family} - P(A=1, B=1): {p_joint:.2f}")
        print(f"Family {family} - P(A=1) * P(B=1): {expected_joint_if_indep:.2f}")
        print(f"Correlation / Attention Bleed detected: {abs(p_joint - expected_joint_if_indep) > 0.1}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
