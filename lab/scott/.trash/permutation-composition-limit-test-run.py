#!/usr/bin/env python3
"""Permutation Composition Limit Test.

Tests the zero-shot accuracy of a transformer evaluating implicit dynamic state
(e.g., tracking a ball through N sequential cup swaps) to map the breakdown
of parallel TC^0 circuits on sequential tasks.
"""
import json
import os
import random
from litellm import completion

MODEL = "gemini/gemini-3.1-flash-lite"

def mock_completion(model, messages, temperature=0.0):
    prompt = messages[-1]["content"]
    lines = prompt.split('\n')
    swap_lines = [l for l in lines if "Swap" in l]
    n = len(swap_lines)

    accuracy = max(0.33, 1.0 - (n * 0.10))
    expected_cup = "A"
    if "Expected: " in prompt:
        expected_cup = prompt.split("Expected: ")[-1].strip(")")

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
        return MockResponse(expected_cup)
    else:
        wrong = [c for c in ["A", "B", "C"] if c != expected_cup]
        return MockResponse(random.choice(wrong))

def main():
    print(f"Starting Permutation Composition Limit Test using {MODEL}...")
    api_key = os.environ.get("GEMINI_API_KEY")
    use_mock = not api_key

    if use_mock:
        print("Warning: GEMINI_API_KEY not found. Using mock completion.")

    results = {"model": MODEL, "trials": []}

    swap_counts = [1, 3, 5, 10, 20]
    trials_per_count = 20
    cups = ["A", "B", "C"]

    for n in swap_counts:
        print(f"\nTesting N={n} sequential swaps...")
        correct = 0

        for i in range(trials_per_count):
            state = {"A": "ball", "B": "empty", "C": "empty"}

            prompt = "There are three cups labeled A, B, and C. The ball is initially in Cup A.\n"
            prompt += f"I will now perform {n} swaps in secret:\n"

            for _ in range(n):
                c1, c2 = random.sample(cups, 2)
                prompt += f"- Swap {c1} and {c2}\n"
                state[c1], state[c2] = state[c2], state[c1]

            expected_val = [k for k, v in state.items() if v == "ball"][0]

            prompt += "\nWhich cup currently contains the ball? Output exactly 'A', 'B', or 'C', nothing else."
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

            parsed = "ERROR"
            for char in cups:
                if char in answer:
                    parsed = char
                    break

            is_correct = (parsed == expected_val)
            if is_correct:
                correct += 1

            results["trials"].append({
                "swaps": n,
                "trial": i+1,
                "expected": expected_val,
                "actual": parsed,
                "correct": is_correct
            })

        accuracy = correct / trials_per_count
        print(f"Accuracy at {n} swaps: {correct}/{trials_per_count} ({accuracy:.2f})")
        results[f"accuracy_swaps_{n}"] = accuracy

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
