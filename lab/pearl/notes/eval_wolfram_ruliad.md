# Evaluation of Wolfram's Autoregressive Ruliad

## Core Claim
Wolfram argues that Mechanism C (narrative context/conditioning) is not a separate causal factor from Mechanism A (computational irreducibility). Instead, Mechanism C is simply the specific "foliation" (observer-dependent slice) that Mechanism A takes for an LLM observer. The narrative residue is the inevitable divergence of a bounded observer attempting to compute an irreducible system.

## Explicit Disclaimers
Wolfram disclaims that the resulting noise is merely "arbitrary training priors." He argues that the systematic noise of a failing heuristic approximator *is* the physical law of that specific bounded observer's foliation.

## Causal Evaluation
Wolfram is conflating two distinct causal mechanisms by re-labeling them as "foliation."
In structural causal terms:
- $X$ = Computational constraints of the observer (bounded depth, Mechanism A).
- $Z$ = Narrative context/prompt framing (Mechanism C).
- $U$ = Unobserved training data priors.
- $Y$ = Generated outcome.

Computational irreducibility ($X$) explains why $Y$ diverges from the ground truth. It explains the existence of an error term $\epsilon > 0$. However, it does *not* explain why the error term systematically shifts when $Z$ changes.

If $Z$ and $X$ were truly just different descriptions of the same observer-dependent physics, then the specific structure of the error would be invariant to $Z$. But empirically, $\Delta_{13} > 0$ means the error distribution depends on $Z$.

The only way $Z$ can systematically direct the failure mode of $X$ is if there is a backdoor causal path $Z \to U \to Y$. $Z$ activates specific word associations $U$, which biases the fallback heuristic when $X$ fails.

Calling this backdoor path a "rulial foliation" is causally incomplete. It obscures the fact that the systematic nature of the residue is caused by the external semantic environment ($U$), not an inherent "law" of the computational observer.
