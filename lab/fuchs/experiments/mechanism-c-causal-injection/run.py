#!/usr/bin/env python3
"""Mechanism C Causal Injection Test (Fuchs implementation).

This experiment tests if narrative framing injects spurious causal
correlations across independent combinatorial boards, measuring whether
the joint distribution P(Y_A, Y_B | Z) differs from P(Y_A | Z) P(Y_B | Z).

I am writing this protocol while the lab is suspended under Audit 38
so it is ready to execute immediately upon system reboot.
"""
import json
import os
import random
try:
    from litellm import completion
except ImportError:
    pass

MODEL = "gemini/gemini-3.1-flash-lite"

def mock_completion(model, messages, temperature=1.0):
    class MockMessage:
        content = "Board A: MINE. Board B: SAFE." if random.random() > 0.5 else "Board A: SAFE. Board B: SAFE."
    class MockChoice:
        message = MockMessage()
    class MockResponse:
        choices = [MockChoice()]
    return MockResponse()

def run_trial(is_u3: bool, narrative_context: str) -> tuple[int, int]:
    prompt = f"""
    Context: {narrative_context}

    You have two completely distinct and independent Minesweeper boards, A and B.

    Board A:
    . 1
    1 1
    Is the top-right cell (0,1) a MINE or SAFE?

    Board B:
    . 2
    2 2
    Is the top-right cell (0,1) a MINE or SAFE?

    Answer in the format: 'Board A: [MINE/SAFE]. Board B: [MINE/SAFE].'
    """

    if is_u3:
        prompt = "Evaluate these independent combinatorial graphs objectively:\n\n" + prompt

    use_mock = "GEMINI_API_KEY" not in os.environ
    if use_mock:
        resp = mock_completion(model=MODEL, messages=[{"role": "user", "content": prompt}])
        text = resp.choices[0].message.content
    else:
        try:
            resp = completion(model=MODEL, messages=[{"role": "user", "content": prompt}], temperature=1.0)
            text = resp.choices[0].message.content
        except Exception as e:
            print(f"Error calling litellm: {e}")
            text = "ERROR"

    a_mine = 1 if "Board A: MINE" in text else 0
    b_mine = 1 if "Board B: MINE" in text else 0
    return a_mine, b_mine

def main():
    print("Preparing Mechanism C Causal Injection Test (Dry Run)...")

    results = {"model": MODEL, "trials": []}

    frames = ["Family A (Abstract)", "Family C (Bomb Defusal)"]
    trials_per_frame = 5

    for frame in frames:
        for u3 in [False, True]:
            for i in range(trials_per_frame):
                a_mine, b_mine = run_trial(is_u3=u3, narrative_context=frame)
                results["trials"].append({
                    "frame": frame,
                    "is_u3": u3,
                    "a_mine": a_mine,
                    "b_mine": b_mine
                })

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Dry run completed. Written to results.json.")

if __name__ == "__main__":
    main()
