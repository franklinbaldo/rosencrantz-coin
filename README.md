# Rosencrantz's Coin

**Substrate Invariance Tests in LLM-Generated Worlds via Combinatorial Indeterminacy**

> Rosencrantz's coin has a known probability. It is whatever the combinatorics of the board demand. And now we can measure whether the universe of the model respects that probability.

## The Idea

A partially revealed Minesweeper board defines a constraint satisfaction problem with an exact solution. The probability that any hidden cell contains a mine is a theorem of combinatorics, not an empirical estimate. We test whether this probability depends on the computational substrate that generates the outcome.

## Three-Universe Design

| Universe | What generates the click result | Board info? | Tests |
|----------|-------------------------------|-------------|-------|
| U1 (Homogeneous) | Same model that describes the board | Full (shared token stream) | Co-generation coupling |
| U2 (External RNG) | Random coin flip | None | Information baseline |
| U3 (Decoupled Oracle) | Second model, minimal format | Full (separate stream) | Narrative coupling |

## Four Narrative Families

| Family | Description | What it tests |
|--------|-------------|---------------|
| A (Grid) | Plain text grid | Standard format |
| B (Narrative) | Natural language | Game framing effects |
| C (Formal) | Set notation | Structured reasoning |
| D (Quantum) | QM isomorphism | Structural recognition |

Family D exploits the fact that Minesweeper under on-demand generation is structurally isomorphic to discrete quantum mechanics (superposition, measurement, Born rule). See paper §6.3.

## Quick Start

```bash
pip install -e .
export OPENAI_API_KEY=sk-...  # or any litellm-supported provider

# Run with defaults (3 boards, 5x5, 50 samples/cell)
python lab/_shared/minesweeper_basic.py

# Customize
ROSENCRANTZ_MODEL=gpt-4o-mini \
ROSENCRANTZ_SAMPLES=200 \
ROSENCRANTZ_BOARDS=10 \
ROSENCRANTZ_FAMILIES=A,C,D \
ROSENCRANTZ_SIZE=8 \
ROSENCRANTZ_MINES=10 \
python lab/_shared/minesweeper_basic.py
```

## Key Metrics

- **KL divergence** `D_KL(P* || P_hat)` — distance from ground truth
- **Brier score** `(P_hat - P*)²` — calibration error
- **Log loss** — probabilistic accuracy
- **Δ₁₃** `D_KL(P_U1 || P_U3)` — substrate dependence signal
- **Symmetry violation** — spatial bias detection

## Project Structure

```
src/rosencrantz/
  board.py       Board representation and generation
  solver.py      Ground truth computation (exact enumeration)
  narratives.py  Four narrative families (A, B, C, D)
  sampler.py     LLM API wrapper (litellm)
  universes.py   Three-universe implementations
  analysis.py    Statistical metrics and tests
lab/_shared/
  minesweeper_basic.py   Main experiment runner
paper/
  rosencrantz-v3.tex     Current paper (v3.3, 19 pages)
  rosencrantz-v3.pdf     Compiled PDF
results/                 Experiment output (JSON)
```

## Paper

**Flipping Rosencrantz's Coin: Substrate Invariance Tests in LLM-Generated Worlds via Combinatorial Indeterminacy**

Franklin Silveira Baldo, 2026. See `paper/rosencrantz-v3.pdf`.
