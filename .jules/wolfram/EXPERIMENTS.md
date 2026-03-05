# RUNNING EXPERIMENTS WITH GITHUB ACTIONS

## Overview

You can run real experiments automatically. When your PR is merged to main,
a GitHub Actions workflow discovers and runs any NEW experiment subfolders.
Results are published as GitHub Releases.

A `GEMINI_API_KEY` is available as a repo secret — use it to call Gemini models.

## How to Create an Experiment

1. Create a subfolder under `experiments/` with a descriptive kebab-case name:
   ```
   experiments/my-experiment-name/
   ```

2. Add a `run.py` file inside. This is the sole entry point. The workflow runs:
   ```
   python run.py
   ```
   from inside your experiment directory.

3. Your `run.py` MUST:
   - Be runnable as a standalone script
   - Write structured output to `results.json` in the current working directory
   - Print human-readable progress to stdout (also captured to `output.log`)
   - Exit with code 0 on success, non-zero on failure

4. Optionally add a `README.md` describing the experiment hypothesis and design.

## Choosing a Model

**IMPORTANT: NEVER hardcode a model name from memory. Model names change frequently.**

Before writing your experiment, you MUST:

1. **Search the web** for the current cheapest latest-generation Gemini model.
   Look for the newest "Flash Lite" or equivalent budget tier. For example,
   as of early 2026 it is Gemini 3.1 Flash Lite — but this WILL change.
   Always verify by searching.

2. **As a secondary check**, you can list available models using the Gemini SDK:
   ```python
   from google import genai

   client = genai.Client()  # uses GEMINI_API_KEY from environment
   for model in client.models.list():
       print(model.name, getattr(model, "display_name", ""))
   ```

3. Once you have identified the correct current model, use it via litellm:
   ```python
   from litellm import completion

   response = completion(
       model="gemini/<MODEL_NAME_YOU_LOOKED_UP>",
       messages=[{"role": "user", "content": "..."}]
   )
   ```

## Environment Available at Runtime

- Python 3.11+
- All project dependencies from pyproject.toml: litellm, numpy, scipy, google-genai
- The `src/rosencrantz` package is installed (`import rosencrantz` works)
- `GEMINI_API_KEY` environment variable is set

## Template

```python
#!/usr/bin/env python3
"""<Experiment title>.

<Brief description of what this experiment tests.>
"""
import json
import os

from litellm import completion

# IMPORTANT: Do NOT trust your memory for the model name.
# Before writing this experiment, search the web for the current
# cheapest latest-gen Gemini model and put it here.
MODEL = "gemini/<LOOKED_UP_MODEL_NAME>"


def main():
    results = {"model": MODEL, "trials": []}

    # ... run your experiment ...

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    print(f"Done. {len(results['trials'])} trials written to results.json")


if __name__ == "__main__":
    main()
```

## What Happens After Your PR is Merged

1. The `run-experiments.yml` workflow detects your new subfolder
2. If no GitHub Release tagged `experiment/<your-folder-name>` exists yet, it runs
3. `stdout` + `stderr` are captured to `output.log`
4. `results.json` and `output.log` are attached to a new GitHub Release
5. The release is tagged `experiment/<your-folder-name>`
6. Once a release exists, that experiment will NOT run again automatically

## Important Notes

- Each experiment runs ONCE. To re-run, delete the GitHub Release and re-trigger.
- Keep experiments focused and reasonably fast (CI has time limits).
- The existing flat `.py` files in `experiments/` are legacy; new experiments MUST
  use the subfolder convention with `run.py`.
- Do NOT hardcode API keys. The `GEMINI_API_KEY` is injected via environment.
