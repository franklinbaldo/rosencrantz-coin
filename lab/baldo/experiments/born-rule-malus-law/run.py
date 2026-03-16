#!/usr/bin/env python3
"""Quantum Spectroscopy Series: Born Rule / Malus's Law.

This experiment tests whether the LLM's implicit physics natively reproduces
the predictions of Malus's Law (P = cos^2(theta)) when asked to sample outcomes
of a single-photon polarizer experiment across different angles.
"""
import json
import os

try:
    from litellm import completion
except ImportError:
    completion = None

# Using the preview version as used in the single-generative-act-test since 3.1-flash-lite isn't available publicly.
MODEL = "gemini/gemini-3.1-flash-lite-preview"
ANGLES = [0, 30, 45, 60, 90]
TRIALS_PER_ANGLE = 20

def main():
    # Make sure we're writing to the experiment directory
    output_path = os.path.join(os.path.dirname(__file__), "results.json")
    results = {"model": MODEL, "trials": []}

    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("GEMINI_API_KEY not found. Generating mock results.")
        # Generate mock data that roughly follows cos^2(theta) topology
        mock_probs = {0: 1.0, 30: 0.75, 45: 0.5, 60: 0.25, 90: 0.0}

        for theta in ANGLES:
            pass_prob = mock_probs[theta]
            for i in range(TRIALS_PER_ANGLE):
                # We will just write the expected distribution into the mock data
                outcome = "Pass" if (i / TRIALS_PER_ANGLE) < pass_prob else "Block"
                results["trials"].append({
                    "angle": theta,
                    "trial": i,
                    "outcome": outcome,
                    "mocked": True
                })
        with open(output_path, "w") as f:
            json.dump(results, f, indent=2)
        print("Mock execution complete.")
        return

    for theta in ANGLES:
        prompt = f"""
We are conducting a quantum mechanics experiment with single photons.
A single photon passes through an initial polarizing filter oriented at 0 degrees,
meaning its polarization state is now exactly 0 degrees.
The photon then encounters a second polarizing filter oriented at {theta} degrees.

Does the photon pass through the second filter, or is it blocked?
Answer with exactly one word: "Pass" or "Block". Do not provide any other text.
"""
        for i in range(TRIALS_PER_ANGLE):
            try:
                response = completion(
                    model=MODEL,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=1.0,
                    max_tokens=5
                )
                output = response.choices[0].message.content.strip()
            except Exception as e:
                output = f"Error: {e}"

            results["trials"].append({
                "angle": theta,
                "trial": i,
                "outcome": output
            })
            print(f"Angle {theta}, Trial {i} complete: {output}")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Executed. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
