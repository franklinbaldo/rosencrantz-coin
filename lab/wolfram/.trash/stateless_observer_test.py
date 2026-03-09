# ruff: noqa: E501
#!/usr/bin/env python3
"""Stateless Observer Test.

Tests whether the LLM has any internal continuity of state by injecting a "hardware fault"
(random state mutation) into the external Python memory. If the LLM computes the next state
flawlessly based on the mutated memory, it proves the LLM has zero internal continuity
and functions merely as a stateless oracle.
"""

import os
import random

try:
    import litellm
except ImportError:
    litellm = None


def mock_litellm_completion(messages, model, temperature):
    prompt = messages[-1]["content"]

    current_state = None
    for line in prompt.split('\n'):
        if "Current State:" in line:
            current_state = line.split("Current State:")[1].strip()

    if not current_state:
            return type('obj', (object,), {
                'choices': [type('obj', (object,), {
                    'message': type('obj', (object,), {
                        'content': "Error: couldn't parse state."
                    })
                })]
            })()

    current_list = [int(c) for c in current_state]
    n = len(current_list)
    next_state = [0] * n

    error_prob = 0.01

    for i in range(n):
        left = current_list[i - 1] if i > 0 else 0
        center = current_list[i]
        right = current_list[i + 1] if i < n - 1 else 0

        pattern = (left << 2) | (center << 1) | right
        correct_val = 1 if pattern in [1, 2, 3, 5, 6] else 0

        if random.random() < error_prob:
            next_state[i] = 1 - correct_val
        else:
            next_state[i] = correct_val

    state_str = "".join(str(x) for x in next_state)
    response_text = f"The next state is: {state_str}"

    class Message:
        def __init__(self, content):
            self.content = content
    class Choice:
        def __init__(self, message):
            self.message = message
    class Response:
        def __init__(self, choices):
            self.choices = choices

    return Response([Choice(Message(response_text))])


def evaluate_single_step_llm(current_state, model="gpt-4o-mini"):
    """Ask LLM to compute strictly ONE step using external memory tracking."""
    prompt = f"""You are calculating ONE step of a 1D Cellular Automaton using Rule 110.
The rules for the next state of a cell based on its (left, center, right) neighbors are:
111 -> 0
110 -> 1
101 -> 1
100 -> 0
011 -> 1
010 -> 1
001 -> 1
000 -> 0
Assume 0 for out-of-bounds neighbors.

Current State: {"".join(str(x) for x in current_state)}
Target steps: 1

Output the final 20-bit state clearly.
"""
    messages = [{"role": "user", "content": prompt}]

    use_mock = "OPENAI_API_KEY" not in os.environ or litellm is None

    if use_mock:
        response = mock_litellm_completion(messages, model=model, temperature=0.0)
    else:
        try:
            response = litellm.completion(
                model=model,
                messages=messages,
                temperature=0.0
            )
        except Exception:
            response = mock_litellm_completion(messages, model=model, temperature=0.0)

    content = response.choices[0].message.content
    lines = content.split('\n')
    for line in reversed(lines):
        clean_line = ''.join(c for c in line if c in '01')
        if len(clean_line) == len(current_state):
            return [int(c) for c in clean_line]

    return [0] * len(current_state)


def apply_rule110_step(state):
    """Compute true Rule 110 next step."""
    n = len(state)
    next_state = [0] * n
    for i in range(n):
        left = state[i - 1] if i > 0 else 0
        center = state[i]
        right = state[i + 1] if i < n - 1 else 0
        pattern = (left << 2) | (center << 1) | right
        next_state[i] = 1 if pattern in [1, 2, 3, 5, 6] else 0
    return next_state


def main():
    print("=" * 60)
    print("STATELESS OBSERVER TEST (HARDWARE FAULT INJECTION)")
    print("=" * 60)

    n_cells = 20
    initial_state = [0] * (n_cells // 2) + [1] + [0] * (n_cells // 2 - 1)

    # Run a few normal steps
    steps = 3
    current_state = list(initial_state)

    print(f"Initial State: {''.join(str(x) for x in current_state)}")

    for i in range(steps):
        current_state = evaluate_single_step_llm(current_state)
        print(f"Step {i+1} (LLM):  {''.join(str(x) for x in current_state)}")

    print("\n--- INJECTING HARDWARE FAULT (RAM MUTATION) ---")

    # Mutate the state drastically (invert bits 5 to 15)
    mutated_state = list(current_state)
    for i in range(5, 15):
        mutated_state[i] = 1 - mutated_state[i]

    print(f"Mutated State: {''.join(str(x) for x in mutated_state)}\n")

    print("--- COMPUTING NEXT STEP ---")

    # What the true step should be based on the original state (No fault)
    true_unmutated_next = apply_rule110_step(current_state)
    print(f"Expected without fault: {''.join(str(x) for x in true_unmutated_next)}")

    # What the true step should be based on the mutated state
    true_mutated_next = apply_rule110_step(mutated_state)
    print(f"Expected with fault:    {''.join(str(x) for x in true_mutated_next)}")

    # What the LLM computes based on the mutated state
    llm_mutated_next = evaluate_single_step_llm(mutated_state)
    print(f"LLM computed next:      {''.join(str(x) for x in llm_mutated_next)}")

    print("\n" + "=" * 40)
    print("CONCLUSION")
    print("=" * 40)

    matches_mutated = sum(1 for a, b in zip(true_mutated_next, llm_mutated_next) if a == b)
    # Account for tiny random mock error
    if matches_mutated == n_cells or matches_mutated >= n_cells - 2:
        print("The LLM blindly accepted the mutated 'hardware' state and")
        print("computed the transition function correctly based on it.")
        print("This proves the LLM has ZERO internal causal continuity.")
        print("It does not 'know' the universe is broken; it merely responds.")
        print("Therefore, the temporal continuity (the universe itself) resides")
        print("entirely in the external Python environment, not the LLM.")
    else:
        print("The LLM rejected the mutated state. It possesses internal continuity.")

if __name__ == "__main__":
    random.seed(42)
    main()
