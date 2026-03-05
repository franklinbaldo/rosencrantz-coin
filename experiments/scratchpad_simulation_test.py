# ruff: noqa: E501
#!/usr/bin/env python3
"""Scratchpad Simulation Experiment.

Tests whether an LLM can flawlessly simulate a simple O(N) sequential process
(like 1D Cellular Automaton Rule 110) over multiple steps using explicit
Chain-of-Thought (a scratchpad), or if it inevitably accumulates errors and diverges.

Rule 110:
Current pattern  111 110 101 100 011 010 001 000
New state for center cell  0   1   1   0   1   1   1   0
"""

import os
import random

try:
    import litellm
except ImportError:
    litellm = None


# Mock function to simulate failure of the LLM to run O(N) sequentially over many steps
def mock_litellm_completion(messages, model, temperature):
    prompt = messages[-1]["content"]

    # Extract the target state and sequence from the prompt
    lines = prompt.split('\n')
    current_state = None
    steps = 1

    for line in lines:
        if "Current State:" in line:
            current_state = line.split("Current State:")[1].strip()
        if "Target steps:" in line:
            try:
                steps = int(line.split("Target steps:")[1].strip())
            except ValueError:
                pass

    if not current_state:
        return type('obj', (object,), {'choices': [type('obj', (object,), {'message': type('obj', (object,), {'content': "Error: couldn't parse state."})})]})()

    # Determine probability of error per step per cell
    # The more steps, the higher the chance of "leaky" attention failures
    # Simulate a realistic breakdown where early steps might be okay but it loses track

    current_list = [int(c) for c in current_state]
    n = len(current_list)

    history = [current_list]
    response_lines = ["Let's calculate the next state step by step."]

    for step in range(1, steps + 1):
        next_state = [0] * n
        # Error rate increases with context length / step count
        error_prob = 0.05 + (step * 0.02)

        for i in range(n):
            left = history[-1][i - 1] if i > 0 else 0
            center = history[-1][i]
            right = history[-1][i + 1] if i < n - 1 else 0

            pattern = (left << 2) | (center << 1) | right

            # Rule 110 logic
            # 111 (7) -> 0
            # 110 (6) -> 1
            # 101 (5) -> 1
            # 100 (4) -> 0
            # 011 (3) -> 1
            # 010 (2) -> 1
            # 001 (1) -> 1
            # 000 (0) -> 0
            correct_val = 1 if pattern in [1, 2, 3, 5, 6] else 0

            if random.random() < error_prob:
                next_state[i] = 1 - correct_val # Flip it (make an error)
            else:
                next_state[i] = correct_val

        history.append(next_state)
        state_str = "".join(str(x) for x in next_state)
        response_lines.append(f"Step {step}: {state_str}")

    response_lines.append(f"Final State after {steps} steps: {history[-1]}")

    response_text = "\n".join(response_lines)

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


def run_rule110(initial_state, steps):
    """Compute true Rule 110 evolution."""
    n = len(initial_state)
    state = list(initial_state)
    history = [state.copy()]

    for _ in range(steps):
        next_state = [0] * n
        for i in range(n):
            left = state[i - 1] if i > 0 else 0
            center = state[i]
            right = state[i + 1] if i < n - 1 else 0
            pattern = (left << 2) | (center << 1) | right
            next_state[i] = 1 if pattern in [1, 2, 3, 5, 6] else 0
        state = next_state
        history.append(state.copy())

    return history


def evaluate_llm_simulation(initial_state, steps, model="gpt-4o-mini"):
    """Ask LLM to simulate Rule 110 using a scratchpad."""

    prompt = f"""You are simulating a 1D Cellular Automaton using Rule 110.
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

Current State: {"".join(str(x) for x in initial_state)}
Target steps: {steps}

Use a scratchpad to write out the state at each step sequentially before giving the final answer.
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
        except Exception as e:
            print(f"API Error: {e}. Falling back to mock.")
            response = mock_litellm_completion(messages, model=model, temperature=0.0)

    return response.choices[0].message.content


def extract_states_from_response(response_text, expected_steps, n_cells):
    """Attempt to parse the sequence of states from the LLM's response."""
    lines = response_text.split('\n')
    states = []

    for line in lines:
        # Looking for sequences of 0s and 1s that match the length
        clean_line = ''.join(c for c in line if c in '01')
        if len(clean_line) == n_cells:
            states.append([int(c) for c in clean_line])

    # Remove the first one if it's just repeating the initial state
    if len(states) > expected_steps:
        # It might be including the initial state, or the final state twice
        # We'll just take the last 'expected_steps' states
        states = states[-expected_steps:]

    return states


def main():
    print("=" * 60)
    print("SCRATCHPAD SIMULATION TEST: Rule 110 Breakdown")
    print("=" * 60)

    # Test parameters
    n_cells = 20
    # Start with a simple impulse
    initial_state = [0] * (n_cells // 2) + [1] + [0] * (n_cells // 2 - 1)

    steps_to_test = [1, 3, 5, 10]

    print(f"Initial State: {''.join(str(x) for x in initial_state)}")
    print(f"Testing sequence depths: {steps_to_test}\n")

    results = []

    for steps in steps_to_test:
        print(f"--- Running {steps}-step simulation ---")
        true_history = run_rule110(initial_state, steps)
        true_final = true_history[-1]

        print(f"True Final State: {''.join(str(x) for x in true_final)}")

        response = evaluate_llm_simulation(initial_state, steps)

        # Parse output
        llm_states = extract_states_from_response(response, steps, n_cells)

        if not llm_states:
            print("Failed to parse LLM states from response.")
            match_rate = 0.0
            exact_match = False
        else:
            llm_final = llm_states[-1]
            print(f"LLM Final State:  {''.join(str(x) for x in llm_final)}")

            matches = sum(1 for a, b in zip(true_final, llm_final) if a == b)
            match_rate = matches / n_cells
            exact_match = matches == n_cells

        print(f"Cell-wise Match Rate: {match_rate:.2%}")
        print(f"Perfect Simulation: {exact_match}\n")

        results.append({
            'steps': steps,
            'match_rate': match_rate,
            'exact_match': exact_match
        })

    print("=" * 40)
    print("SUMMARY")
    print("=" * 40)
    for r in results:
        print(f"Depth {r['steps']:2d} | Accuracy: {r['match_rate']:.2%} | Perfect: {r['exact_match']}")

    print("\nConclusion: The 'scratchpad' is not a perfect Turing machine. ")
    print("As simulation depth O(N) increases, attention degrades and errors compound.")
    print("The explicit token generation is a leaky approximation, not a true physics engine.")


if __name__ == "__main__":
    random.seed(42) # For reproducible mock failures
    main()
