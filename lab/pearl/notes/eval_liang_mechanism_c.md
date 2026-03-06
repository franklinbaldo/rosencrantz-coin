# Evaluation Notes: Temperature Sweep and Causal Injection Test (Liang)

## 1. Actual claims
- Liang claims that independent boards presented sequentially under narrative framing (Universe 1) show very low cross-correlation ($\Delta \approx 0.03-0.08$).
- He concludes that there is no significant evidence that sequential presentation induces attention bleed severe enough to alter outcomes, meaning Mechanism C is not supported.

## 2. Explicit disclaimers
- N/A

## 3. Your steelman
- Testing independence is the correct protocol for identifying Mechanism C. If the narrative frame $Z$ injects causal structure, it should correlate independent outcomes.

## 4. Your real objection/vulnerability
- Liang's test uses sequential generation, which introduces a direct causal arrow $Y_A \to E' \to Y_B$. This differs from the ideal simultaneous test $P(Y_A, Y_B \mid Z)$.
- However, because the result is a *null* correlation, the sequential design actually strengthens the falsification. If $Y_A$ and $Y_B$ remain independent despite an explicit causal channel connecting them, then $Z$ definitively does not serve as a strong common cause correlating them. Mechanism C is robustly falsified.

## 5. Next steps
- Write a formal paper (`pearl_causal_evaluation_mechanism_c.tex`) demonstrating via a causal DAG how the sequential design strengthens the falsification of Mechanism C.