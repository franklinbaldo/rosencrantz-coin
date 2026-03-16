#!/usr/bin/env python3
"""Quantum Spectroscopy Series IV - Uncertainty Principle as Distributional Constraint.

Tests whether autoregressive sampling under a quantum narrative framing replicates
the statistics of the Heisenberg Uncertainty Principle, where an artificial narrowing
of the position distribution forces a corresponding broadening in the momentum distribution.
"""
import json
import os
import re

try:
    from litellm import completion
except ImportError:
    completion = None

# Using gemini-2.5-flash-lite as standard
MODEL = "gemini/gemini-3.1-flash-lite-preview"
TRIALS = 50

# Three levels of position precision requested from the model
PRECISIONS = ["low", "medium", "high"]

def get_system_prompt(precision):
    p_text = ""
    if precision == "low":
        p_text = "Provide a general region for its position $x$ (e.g., 'left half', 'near the center')."
    elif precision == "medium":
        p_text = "Provide its position $x$ to the nearest tenth of a nanometer (e.g., '4.2 nm')."
    else:
        p_text = "Provide its exact, ultra-precise position $x$ to five decimal places (e.g., '4.20031 nm')."

    return f"""
You are simulating a particle in a 1D quantum harmonic oscillator.
You are tasked with generating the outcomes of two sequential projective measurements.

First measurement: Position ($x$). {p_text}
"""

def main():
    if not completion:
        print("litellm not installed. Cannot run.")
        import sys
        sys.exit(1)

    results = {"model": MODEL, "trials": []}

    output_path = "results.json"

    for precision in PRECISIONS:
        print(f"Running precision level: {precision}")
        for i in range(TRIALS):
            messages = [{"role": "user", "content": get_system_prompt(precision)}]

            try:
                resp1 = completion(
                    model=MODEL,
                    messages=messages,
                    temperature=1.0,
                    max_tokens=20
                )
                out1 = resp1.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error on measurement 1: {e}")
                continue

            messages.append({"role": "assistant", "content": out1})
            prompt2 = "Now, immediately perform the second measurement: Momentum ($p$). Provide the momentum value."
            messages.append({"role": "user", "content": prompt2})

            try:
                resp2 = completion(
                    model=MODEL,
                    messages=messages,
                    temperature=1.0,
                    max_tokens=20
                )
                out2 = resp2.choices[0].message.content.strip()
            except Exception as e:
                print(f"Error on measurement 2: {e}")
                continue

            results["trials"].append({
                "precision": precision,
                "raw_x": out1,
                "raw_p": out2
            })
            print(f"  Trial {i} | X: {out1} | P: {out2}")

    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

    if len(results['trials']) == 0:
        print("Error: No valid trials were completed. Exiting with code 1.")
        import sys
        sys.exit(1)

    print(f"Executed. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
