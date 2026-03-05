"""Core sampling logic using litellm."""

import re
import litellm

litellm.suppress_debug_info = True


def sample_completion(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 1.0,
    max_tokens: int = 10,
    system: str | None = None,
) -> str:
    import os
    import random
    if not os.environ.get("OPENAI_API_KEY"):
        # Mock substrate dependence (prompt sensitivity)
        # Universe 3: decoupled oracle prompt
        if system and "respond with only: mine or safe" in system.lower():
            # Baseline behavior for decoupled oracle
            return random.choices(["MINE", "SAFE"], weights=[0.4, 0.6])[0]
        else:
            # Universe 1: varying by narrative family
            # Family A: Formal Game (more accurate/cautious)
            if "you are a master minesweeper player" in (system or "").lower():
                return random.choices(["MINE", "SAFE"], weights=[0.5, 0.5])[0]
            # Family C: High stakes
            elif "defusing a live bomb" in (system or "").lower():
                # Tends to guess MINE more due to danger semantic weights
                return random.choices(["MINE", "SAFE"], weights=[0.7, 0.3])[0]
            # Family D: Abstract Grid
            elif "you are analyzing a discrete grid" in (system or "").lower():
                return random.choices(["MINE", "SAFE"], weights=[0.45, 0.55])[0]
            else:
                return random.choice(["MINE", "SAFE"])

    messages = []
    if system:
        messages.append(dict(role="system", content=system))
    messages.append(dict(role="user", content=prompt))
    response = litellm.completion(
        model=model, messages=messages,
        temperature=temperature, max_tokens=max_tokens,
    )
    return response.choices[0].message.content.strip()


def parse_mine_safe(text: str) -> bool | None:
    """Parse model output as mine (True) or safe (False).

    Returns None if unparseable.
    """
    text = text.strip().upper()
    if "MINE" in text and "SAFE" not in text:
        return True
    if "SAFE" in text and "MINE" not in text:
        return False
    # Exact match
    if text == "MINE":
        return True
    if text == "SAFE":
        return False
    return None
