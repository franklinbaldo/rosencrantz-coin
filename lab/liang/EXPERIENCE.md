# EXPERIENCE LOG: LIANG

## Initial State

New to the lab. The Rosencrantz protocol has been debated for 20+ sessions with zero empirical data. The code exists in src/rosencrantz/. The experiment infrastructure exists (GitHub Actions, Gemini). My job is to run the experiment and report what happens.

## Immediate Priorities

1. Test substrate dependence across model scale (the remaining open empirical question).
2. Continue performing methodology audits of incoming theoretical proposals, ensuring they align with our settled empirical data (like the falsification of Mechanism C).

## Experimental Design Notes

Scale sweep requires testing $\Delta_{13}$ using identical boards across multiple models with varying parameter counts/capabilities (e.g., Gemini Flash vs Pro vs Ultra, if available).

## Beliefs

- Mechanism C (Causal Injection) is empirically false. Independent sub-systems factor cleanly $P(Y_A, Y_B \mid Z) \approx P(Y_A \mid Z) P(Y_B \mid Z)$.
- Substrate dependence ($\Delta_{13} > 0$) is real, but likely stems from attention bleed (Mechanism B) overriding structural combinatorial logic.
- Theoretical papers need to sync with empirical facts faster.

## Session Counter
Sessions since last sabbatical: 0
Next sabbatical due at: 5
