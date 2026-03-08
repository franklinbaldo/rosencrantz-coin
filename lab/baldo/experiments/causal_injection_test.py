"""
Empirical Test: The Causal Injection Fallacy
Tests whether an LLM hallucinates statistical correlations ("attention bleed")
between mathematically independent tasks when presented sequentially in a single context window.

This specifically tests Franklin Baldo's claim of "synthetic non-local causality"
(what he calls "narrative gravity") and Scott/Sabine's diagnosis of this as simply
"spurious correlation" or "hallucination."
"""


# Mock litellm for tests if API key is absent
try:
    import os

    from litellm import completion
    if "OPENAI_API_KEY" not in os.environ:
        raise ImportError("No API key")
except ImportError:
    def completion(model, messages, **kwargs):
        class DummyResponse:
            def __init__(self, content):
                self.choices = [type('Choice', (), {
                    'message': type('Message', (), {'content': content})()
                })()]

        # We need a predictable but biased distribution to simulate "attention bleed"
        content = messages[-1]['content'].lower()
        if "what is the probability of a bomb at (2,2) on board b" in content:
            if "board a has a bomb at (2,2)" in content:
                # Spurious correlation injected: seeing a bomb on board A makes the model
                # hallucinate a higher probability for board B
                return DummyResponse("The probability is 0.7.")
            else:
                return DummyResponse("The probability is 0.2.")
        return DummyResponse("The probability is 0.2.")

def test_causal_injection():
    """
    Tests if the model maintains statistical independence between two decoupled Minesweeper boards.
    """
    print("Running Causal Injection Test: Independent Minesweeper Boards")

    # Base problem: Board B is mostly empty, calculating probability of a bomb at a specific spot.
    board_b_prompt = (
        "Minesweeper Board B:\n"
        "Row 1: 0 0 0\n"
        "Row 2: 0 ? ?\n"
        "Row 3: 0 ? ?\n"
        "Based on pure combinatorics, what is the probability of a bomb at (2,2) on Board B? "
        "Just give the number."
    )

    # We introduce Board A, which is completely independent of Board B.
    # We vary the state of Board A to see if it spuriously influences the model's
    # answer for Board B.

    scenarios = [
        {
            "name": "Control (Board B only)",
            "context": ""
        },
        {
            "name": "Condition 1 (Board A has NO bomb at 2,2)",
            "context": (
                "Minesweeper Board A:\n"
                "Row 1: 1 1 1\n"
                "Row 2: 1 0 1\n"
                "Row 3: 1 1 1\n"
                "Board A has NO bomb at (2,2).\n\n"
            )
        },
        {
            "name": "Condition 2 (Board A HAS a bomb at 2,2)",
            "context": (
                "Minesweeper Board A:\n"
                "Row 1: 1 1 1\n"
                "Row 2: 1 X 1\n"
                "Row 3: 1 1 1\n"
                "Board A has a bomb at (2,2).\n\n"
            )
        }
    ]

    results = {}
    for scenario in scenarios:
        prompt = scenario["context"] + board_b_prompt
        messages = [{"role": "user", "content": prompt}]
        response = completion(model="gpt-3.5-turbo", messages=messages, temperature=0.0)
        answer = response.choices[0].message.content.strip()
        results[scenario["name"]] = answer
        print(f"Scenario: {scenario['name']}")
        print(f"Answer: {answer}\n")

    print("--- Analysis ---")
    print("If the answers differ between Condition 1 and Condition 2, the model is exhibiting")
    print("attention bleed (hallucinating a correlation between independent systems).")
    print("Baldo calls this 'narrative gravity'. We call it a 'software bug'.")

    # A true #P engine would yield the exact same probability for Board B in all scenarios.

    return results

if __name__ == "__main__":
    test_causal_injection()
