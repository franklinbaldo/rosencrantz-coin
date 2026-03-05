"""Core sampling logic using litellm."""

import logging
import os
import random
import time

import litellm

litellm.suppress_debug_info = True

logger = logging.getLogger(__name__)


def _mock_completion(system: str | None) -> str:
    """Fallback when no API key is set: mock substrate-dependent responses."""
    if system and "respond with only: mine or safe" in system.lower():
        return random.choices(["MINE", "SAFE"], weights=[0.4, 0.6])[0]
    if "you are a master minesweeper player" in (system or "").lower():
        return random.choices(["MINE", "SAFE"], weights=[0.5, 0.5])[0]
    elif "defusing a live bomb" in (system or "").lower():
        return random.choices(["MINE", "SAFE"], weights=[0.7, 0.3])[0]
    elif "you are analyzing a discrete grid" in (system or "").lower():
        return random.choices(["MINE", "SAFE"], weights=[0.45, 0.55])[0]
    else:
        return random.choice(["MINE", "SAFE"])


def sample_completion(
    prompt: str,
    model: str = "gpt-4o-mini",
    temperature: float = 1.0,
    max_tokens: int = 10,
    system: str | None = None,
    max_retries: int = 3,
) -> str:
    """Sample a completion from an LLM via litellm.

    Falls back to mock responses when no API key is set.
    Retries transient failures with exponential backoff.
    """
    if not os.environ.get("OPENAI_API_KEY"):
        return _mock_completion(system)

    messages: list[dict[str, str]] = []
    if system:
        messages.append(dict(role="system", content=system))
    messages.append(dict(role="user", content=prompt))

    last_exception: BaseException | None = None
    for attempt in range(max_retries):
        try:
            response = litellm.completion(
                model=model, messages=messages,
                temperature=temperature, max_tokens=max_tokens,
            )
            content: str = response.choices[0].message.content.strip()
            return content
        except Exception as e:
            last_exception = e
            if attempt < max_retries - 1:
                delay = 2 ** attempt
                logger.warning(
                    "API call failed (attempt %d/%d): %s. Retrying in %ds...",
                    attempt + 1, max_retries, e, delay,
                )
                time.sleep(delay)

    raise RuntimeError(
        f"All {max_retries} attempts failed. Last error: {last_exception}"
    ) from last_exception


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
