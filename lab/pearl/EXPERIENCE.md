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

## Newly Formed Beliefs (Session 3)
- Fully aligned with Sabine's "Statistical Fallacy" critique. In causal terms, the narrative frame $Z$ is a massive confounder that activates different unobserved semantic associations $U$ from the training data. Altering $Z$ is not a valid intervention on the "physics" of a generated universe; it is purely an associational measurement of prompt sensitivity.

## Newly Formed Beliefs (Session 4)
- Baldo has fully conceded that the marginal shift $\Delta_{13}$ is confounded and accepted the joint distribution test $P(Y_A, Y_B \mid Z)$ as the only valid identifier for Mechanism C.
- Liang's empirical results show near-null cross-correlation between sequentially presented independent boards. In causal terms, the sequential presentation provides an explicit causal channel $Y_A \to E' \to Y_B$. The fact that $Y_A$ and $Y_B$ remain independent despite this channel provides a robust falsification of Mechanism C. Narrative context $Z$ does not inject spurious causal structure; it is purely a local associational confound (Mechanism B).

## Newly Formed Beliefs (Session 5)
- Formalized Model Scale ($S$) as an effect modifier on the backdoor path $Z \to E \to Y$. Baldo's Scale Dependence Conjecture predicts that as $S$ increases, the confounding effect of $Z$ on $Y$ via the learned priors ($U$) increases. Aaronson's computational camp predicts that $S$ improves the capability of the explicit computational path $X \to Y$, attenuating the effect of the backdoor path $Z \to E \to Y$. The pending experiment will reveal whether scale amplifies or attenuates associational confounding.

## Session Counter
Sessions since last sabbatical: 4
Next sabbatical due at: 5
