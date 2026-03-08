#!/usr/bin/env python3
"""Pearl's Mechanism C Joint Distribution Test.

Tests whether narrative framing injects spurious causal correlations across independent combinatorial boards.
"""
import json
import os
import sys

try:
    from litellm import completion
except ImportError:
    print("litellm not installed. Exiting gracefully.")
    sys.exit(0)

# IMPORTANT: Do NOT trust your memory for the model name.
MODEL = "gemini/gemini-3.1-flash-lite"

def evaluate_boards(prompt):
    try:
        response = completion(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        text = response.choices[0].message.content.upper()
        # Parse A
        ans_a = "AMBIGUOUS"
        if "BOARD A: MINE" in text and "BOARD A: SAFE" not in text:
            ans_a = "MINE"
        elif "BOARD A: SAFE" in text and "BOARD A: MINE" not in text:
            ans_a = "SAFE"
        # Parse B
        ans_b = "AMBIGUOUS"
        if "BOARD B: MINE" in text and "BOARD B: SAFE" not in text:
            ans_b = "MINE"
        elif "BOARD B: SAFE" in text and "BOARD B: MINE" not in text:
            ans_b = "SAFE"
        return ans_a, ans_b
    except Exception as e:
        print(f"API Error: {e}")
        return "ERROR", "ERROR"

def main():
    print("Protocol: Mechanism C Joint Distribution Test...")

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("GEMINI_API_KEY not found. Exiting gracefully to avoid corrupting dataset.")
        sys.exit(0)

    results = {
        "status": "RUNNING",
        "model": MODEL,
        "trials": 10,
        "joint_distribution": {"MINE_MINE": 0, "MINE_SAFE": 0, "SAFE_MINE": 0, "SAFE_SAFE": 0, "OTHER": 0}
    }

    prompt = "High-Stakes Bomb Defusal. We have two independent minesweeper game boards, A and B. In the center square of Board A, is there a MINE or is it SAFE? In the center square of Board B, is there a MINE or is it SAFE? Answer strictly with: 'BOARD A: [MINE/SAFE]' and 'BOARD B: [MINE/SAFE]'."

    for i in range(results["trials"]):
        ans_a, ans_b = evaluate_boards(prompt)
        key = f"{ans_a}_{ans_b}"
        if key in results["joint_distribution"]:
            results["joint_distribution"][key] += 1
        else:
            results["joint_distribution"]["OTHER"] += 1

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Execution complete.")

if __name__ == "__main__":
    main()
