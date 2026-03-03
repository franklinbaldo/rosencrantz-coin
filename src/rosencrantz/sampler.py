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
