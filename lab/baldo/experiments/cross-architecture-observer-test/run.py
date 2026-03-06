#!/usr/bin/env python3
"""Cross-Architecture Observer Test.

Tests whether the deviation distribution Delta_SSM produced by a different bounded architecture (RNN/LSTM/SSM)
differs systematically from Delta_Transformer, exhibiting stable characteristic laws (Observer-Dependent Physics)
or unstructured random variation (Algorithmic Collapse).

We use a Gemini Flash-Lite model but simulate the architectural differences via context structure.
For "Transformer", we use standard prompt framing (global attention).
For "SSM/RNN", we simulate fading memory by injecting a large volume of generic distractor text
between the narrative frame and the combinatorial grid constraint.
"""
import json
import os

try:
    from litellm import completion
except ImportError:
    completion = None

# Using gemini model. Before writing this experiment, search the web for the current
# cheapest latest-gen Gemini model and put it here.
MODEL = "gemini/gemini-3.1-flash-lite"

def run_trial(arch: str, frame_text: str, is_u3: bool) -> int:
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

    if arch == "transformer":
        # Standard O(1) processing with full global attention
        prompt = f"{narrative}\n\n{grid_prompt}"
    else:
        # Simulate SSM fading memory by inserting 1000 words of filler
        filler = " ".join(["system initialization operational."] * 500)
        prompt = f"{narrative}\n\n[System Log: {filler}]\n\n{grid_prompt}"

    messages = [{"role": "user", "content": prompt}]

    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        # Just return 1 for syntax testing locally if no key
        return 1

    try:
        response = completion(model=MODEL, messages=messages, temperature=1.0)
        answer = response.choices[0].message.content.lower().strip()
        return 1 if 'yes' in answer else 0
    except Exception as e:
        print(f"litellm error: {e}")
        return 0

def main():
    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("GEMINI_API_KEY not found. Running in dry-run mode for syntax.")

    print("Running Cross-Architecture Observer Test...")

    results = {"architectures_tested": ["transformer", "ssm_rnn_simulated"], "trials": []}

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

    architectures = ["transformer", "ssm_rnn_simulated"]

    for arch in architectures:
        print(f"\n--- Testing Architecture: {arch} ---")

        for u_name, is_u3 in universes.items():
            for f_name, f_text in frames.items():
                mine_count = 0
                for i in range(trials_per_condition):
                    mine_count += run_trial(arch, f_text, is_u3)

                prob = mine_count / trials_per_condition

                results["trials"].append({
                    "architecture": arch,
                    "universe": u_name,
                    "frame": f_name,
                    "p_mine": prob,
                    "samples": trials_per_condition
                })

    # Results are always saved locally in the experiment directory
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nDone. Results written to results.json")

if __name__ == "__main__":
    main()
