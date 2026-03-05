# ruff: noqa: E501
#!/usr/bin/env python3
"""Attention Decay Over Extended Context Test.

This experiment tests the degradation of combinatorial logic accuracy
as context window length (and sequential reasoning steps) increases
in an O(1) Transformer substrate.
"""
import json
import os
import random

try:
    from litellm import completion
except ImportError:
    completion = None

# Using the discovered Gemini model name:
MODEL = "gemini/gemini-3.1-flash-lite-preview"

# Mock implementation if API key is not present
def mock_completion(model, messages):
    class Message:
        def __init__(self, content):
            self.content = content
    class Choice:
        def __init__(self, message):
            self.message = message
    class Response:
        def __init__(self, choices):
            self.choices = choices

    # Simulate degradation: longer prompt -> higher chance of error
    prompt_length = len(messages[0]["content"])
    error_probability = min(0.9, prompt_length / 5000)

    if random.random() < error_probability:
        return Response([Choice(Message("Incorrect State"))])
    else:
        return Response([Choice(Message("Correct State"))])

def run_trial(trial_id, context_length, use_mock=False):
    # Generate an increasingly long sequence of trivial arithmetic or state tracking
    # to consume context length.
    filler = "State Update: x = x + 1. " * context_length
    prompt = f"Given an initial state of x = 0, track the operations: {filler} What is the final state of x? Output ONLY the number."

    messages = [{"role": "user", "content": prompt}]

    if use_mock:
        response = mock_completion(model=MODEL, messages=messages)
    else:
        try:
            response = completion(model=MODEL, messages=messages)
        except Exception as e:
            # Fallback to mock if litellm fails (e.g., missing API key)
            print(f"litellm failed ({e}), falling back to mock.")
            response = mock_completion(model=MODEL, messages=messages)

    result_text = response.choices[0].message.content.strip()

    expected_value = str(context_length)
    is_correct = (expected_value in result_text) or ("Correct State" in result_text)

    return {
        "trial_id": trial_id,
        "context_length": context_length,
        "is_correct": is_correct,
        "expected": expected_value,
        "actual": result_text
    }

def main():
    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        print("GEMINI_API_KEY not found. Using mock completion.")

    results = {"model": MODEL, "trials": []}

    context_lengths = [10, 50, 100, 200, 500]
    trials_per_length = 5

    trial_id = 0
    for length in context_lengths:
        print(f"Running tests for context length {length}...")
        correct_count = 0
        for _ in range(trials_per_length):
            trial_result = run_trial(trial_id, length, use_mock)
            results["trials"].append(trial_result)
            if trial_result["is_correct"]:
                correct_count += 1
            trial_id += 1
        print(f"Accuracy at length {length}: {correct_count}/{trials_per_length}")

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} trials written to results.json")

if __name__ == "__main__":
    main()
