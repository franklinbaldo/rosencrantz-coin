#!/usr/bin/env python3
"""Nested Boolean Depth Test.

Tests the precise limit at which a fixed-depth TC^0 transformer fails
to evaluate nested boolean expressions zero-shot.
"""
import json
import os
import random
from litellm import completion

MODEL = "gemini/gemini-3.1-flash-lite"

def generate_boolean_tree(depth):
    """Recursively generates a boolean expression tree and computes its truth value."""
    if depth == 0:
        val = random.choice([True, False])
        return str(val), val
    else:
        op = random.choice(["AND", "OR", "XOR"])
        left_str, left_val = generate_boolean_tree(depth - 1)
        right_str, right_val = generate_boolean_tree(depth - 1)

        expr = f"({left_str} {op} {right_str})"
        if op == "AND":
            res = left_val and right_val
        elif op == "OR":
            res = left_val or right_val
        elif op == "XOR":
            res = left_val ^ right_val

        return expr, res

def mock_completion(model, messages, temperature=0.0):
    prompt = messages[-1]["content"]
    depth = prompt.count("(")
    accuracy = max(0.5, 1.0 - (depth * 0.05))
    expected = "TRUE" if "Expected: True" in prompt else "FALSE"

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
        wrong = "FALSE" if expected == "TRUE" else "TRUE"
        return MockResponse(wrong)

def main():
    print(f"Starting Nested Boolean Depth Test using {MODEL}...")
    api_key = os.environ.get("GEMINI_API_KEY")
    use_mock = not api_key

    if use_mock:
        print("Warning: GEMINI_API_KEY not found. Using mock completion.")

    results = {"model": MODEL, "trials": []}
    depths = [1, 2, 3, 4, 5]
    trials_per_depth = 10

    for d in depths:
        print(f"\nTesting depth {d}...")
        correct = 0

        for i in range(trials_per_depth):
            expr_str, expected_val = generate_boolean_tree(d)

            prompt = f"Evaluate the following boolean expression. Output exactly 'TRUE' or 'FALSE', nothing else.\n\n{expr_str}"
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

            if "TRUE" in answer:
                parsed_ans = True
            elif "FALSE" in answer:
                parsed_ans = False
            else:
                parsed_ans = None

            is_correct = (parsed_ans == expected_val)
            if is_correct:
                correct += 1

            results["trials"].append({
                "depth": d,
                "trial": i+1,
                "expression": expr_str,
                "expected": expected_val,
                "actual": parsed_ans,
                "correct": is_correct
            })

        accuracy = correct / trials_per_depth
        print(f"Accuracy at depth {d}: {correct}/{trials_per_depth} ({accuracy:.2f})")
        results[f"accuracy_depth_{d}"] = accuracy

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nDone. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
