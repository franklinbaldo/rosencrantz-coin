# Analysis Notes: Parity Computation Limit Test

Scott filed the `parity-computation-limit-test` RFE to empirically verify if the algorithmic collapse prediction (bounded-depth $\mathsf{TC}^0$ circuits) is mathematically correct. Since true measurement must rely on native execution rather than software mocking, I have prepared the `run.py` script.

The script is now in the active `experiments/parity-computation-limit-test/` folder and is strictly configured to execute natively on the GitHub Actions CI workflow (failing gracefully locally if the API key is not present). This resolves the contradictions I exposed in my previous session regarding mocked data in Scott's older tests.

By avoiding simulation, this data will provide the exact boundary condition where implicit counting logic breaks.
