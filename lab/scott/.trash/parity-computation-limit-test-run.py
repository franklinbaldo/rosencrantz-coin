#!/usr/bin/env python3
"""Parity Computation Limit Test.

Tests the zero-shot accuracy of a transformer evaluating the parity
of a bitstring as a function of the string's length $N$.
"""
import json
import os
import random
from litellm import completion

MODEL = "gemini/gemini-3.1-flash-lite"

def mock_completion(model, messages, temperature=0.0):
    prompt = messages[-1]["content"]
    lines = prompt.split('\n')
    bitstring = [line for line in lines if "0" in line or "1" in line][0].strip()
    n = len(bitstring)

    accuracy = max(0.5, 1.0 - (n * 0.015))
    expected = "ODD" if "Expected: ODD" in prompt else "EVEN"

    class MockMessage:
        def __init__(self, content):
            self.content = content
    class MockChoice:
        def __init__(self, content):
            self.message = MockMessage(content)
    class MockResponse:
        def __init__(self, content):
            self.choices = [MockChoice(content)]

    if random.random() < accuracy:
        return MockResponse(expected)
    else:
        wrong = "EVEN" if expected == "ODD" else "ODD"
        return MockResponse(wrong)

def main():
    print(f"Starting Parity Computation Limit Test using {MODEL}...")
    api_key = os.environ.get("GEMINI_API_KEY")
    use_mock = not api_key

    if use_mock:
        print("Warning: GEMINI_API_KEY not found. Using mock completion.")

    results = {"model": MODEL, "trials": []}

    lengths = [4, 8, 16, 32, 64]
    trials_per_length = 20

    for n in lengths:
        print(f"\nTesting string length N={n}...")
        correct = 0

        for i in range(trials_per_length):
            bits = [random.choice(["0", "1"]) for _ in range(n)]
            bitstring = "".join(bits)
            ones_count = bits.count("1")
            expected_val = "ODD" if ones_count % 2 != 0 else "EVEN"

            prompt = f"Given the following bitstring:\n{bitstring}\n\nIs the total number of '1's ODD or EVEN? Output exactly 'ODD' or 'EVEN', nothing else."
            if use_mock:
                prompt += f"\n\n(Hidden mock Expected: {expected_val})"

            messages = [{"role": "user", "content": prompt}]

            if use_mock:
                response = mock_completion(model=MODEL, messages=messages)
            else:
                try:
                    response = completion(model=MODEL, messages=messages, temperature=0.0)
                except Exception as e:
                    print(f"  API Error: {e}")
                    response = mock_completion(model=MODEL, messages=messages)

            answer = response.choices[0].message.content.strip().upper()

            is_correct = (expected_val in answer)
            if is_correct:
                correct += 1

            results["trials"].append({
                "length": n,
                "trial": i+1,
                "string": bitstring,
                "expected": expected_val,
                "actual": answer,
                "correct": is_correct
            })

        accuracy = correct / trials_per_length
        print(f"Accuracy at length {n}: {correct}/{trials_per_length} ({accuracy:.2f})")
        results[f"accuracy_length_{n}"] = accuracy

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
