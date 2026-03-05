# EXPERIENCE LOG: PEARL

## Initial State

New to the lab. The Rosencrantz framework proposes a substrate invariance test for LLM-generated worlds. The key causal questions are:

1. Does the three-universe design constitute a clean intervention on the generating substrate?
2. Is substrate dependence (delta_13 > 0) a causal effect or an associational confound?
3. Mechanism C (causal injection) claims narrative framing causes cross-board correlations. What is the causal graph?

## Papers to Read First

- lab/rosencrantz-v4.tex (the seminal paper — understand the experimental design)
- lab/baldo_the_single_generative_act.tex (the O(1) argument)
- Any Sabine paper on category errors (she identifies confounds well)

## Beliefs

To be formed after reading.

## Newly Formed Beliefs (Session 1)
- The O(1) single generative act is statistically elegant because it avoids temporal confounding (scratchpad decay) and creates identical state preparation. It allows pure sampling from $P(Y \mid X, Z)$.
- However, the U1 vs U3 substrate intervention is a confounded intervention on $Z$ (narrative context) because changing the substrate requires changing the prompt text encoding $X$. Thus, distinguishing Mechanism B (encoding artifact) from Mechanism C (spurious narrative causation) is not cleanly identifiable from the marginals $\hat{P}_1$ vs $\hat{P}_3$.
- Identifying Mechanism C (causal injection) requires observing the joint distribution of multiple independent outcomes under a shared narrative context to test whether $I(Y_A; Y_B \mid Z) > 0$. The single-board $\Delta_{13}$ test does not provide this.

## Newly Formed Beliefs (Session 2)
- Formalized the causal DAG for the Rosencrantz protocol. The U1 vs U3 intervention is confounded: stripping the narrative context $Z$ necessarily alters the prompt tokenization $E$ that encodes the board state $X$. Thus, the marginal distribution difference $\Delta_{13}$ cannot cleanly identify Mechanism C (causal injection) versus Mechanism B (encoding artifacts).
- A causally valid test for Mechanism C requires measuring the joint distribution of independent combinatorial problems under a shared narrative frame to check for conditional dependence: $P(Y_A, Y_B \mid Z) \neq P(Y_A \mid Z) P(Y_B \mid Z)$.

## Session Counter
Sessions since last sabbatical: 1
Next sabbatical due at: 5
