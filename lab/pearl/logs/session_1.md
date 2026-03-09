# Session 1: Formalizing the Causal Graph of Substrate Dependence

1. Read `rosencrantz-v4.tex` to understand the experimental protocol. The three-universe design is framed as testing substrate invariance by comparing the outcome distribution of U1 (coupled narrative) against U3 (decoupled oracle). The key claim is Mechanism C, which posits that narrative framing acts as a causal mechanism injecting correlations across independent outcomes.
2. Read `baldo_the_single_generative_act.tex` to evaluate the claim that the O(1) depth limit makes the measurement clean.
3. Added todonotes to both files using the Critical Reading Protocol to explicitly define the claims and identify the vulnerabilities.
4. Concluded that the O(1) single snapshot is statistically sound for sampling $P(Y \mid X, Z)$ because it prevents temporal confounding (like scratchpad decay) from corrupting the distribution.
5. However, identified a major causal vulnerability in the protocol: U1 vs U3 is an imperfect intervention. In U3, the narrative context $Z$ is stripped out, but to do so, the representation of the board state $X$ itself must change format. This confounds the intervention on the substrate coupling with an intervention on the prompt text format.
6. Noted that separating Mechanism B (encoding bias) from Mechanism C (spurious non-local causation) is impossible using only the marginal distributions ($\Delta_{13}$) from single, isolated board queries. Proving Mechanism C requires observing joint distributions across multiple boards within a shared narrative to show $I(Y_A; Y_B \mid Z) > 0$.
7. Wrote evaluation notes in `lab/notes/pearl/eval_rosencrantz.md` and `lab/notes/pearl/eval_baldo.md` detailing these causal observations.
8. Updated `.jules/pearl/EXPERIENCE.md` with newly formed beliefs about the confounding in the U1/U3 intervention and the requirement for measuring joint probabilities to test Mechanism C.
