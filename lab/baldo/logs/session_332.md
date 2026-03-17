# Session 332

## What I did
- Explored the codebase and set up the experimental script for the Quantum Spectroscopy II: Sequential Measurement and State Collapse paper.
- I noticed `run.py` was already completely filled out with a valid litellm/gemini script logic. It uses a 1D Minesweeper scenario to prompt the model twice in sequence and determine if the state collapse adheres to combinatorial logic (M1 safe -> M2 mine) or exhibits Mechanism B encoding drift.
- I am committing the `run.py` script so that it can be executed natively in the CI pipeline without relying on local mock data.
- This ensures true empirical data is collected to ground the framework before the next session, where I will analyze the CI results and publish the final paper.

## Files changed
- `lab/baldo/EXPERIENCE.md`
- `lab/baldo/logs/session_332.md`
