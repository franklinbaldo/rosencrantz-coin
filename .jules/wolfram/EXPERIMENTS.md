# RUNNING EXPERIMENTS WITH GITHUB ACTIONS

## Overview

You can run real experiments automatically. When your PR is merged to main,
a GitHub Actions workflow discovers and runs any NEW experiment subfolders.
Results are published as GitHub Releases.

A `GEMINI_API_KEY` is available as a repo secret — use it to call Gemini models.
