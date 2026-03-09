# Evaluation Notes: Literature on Scale and Substrate Dependence (Giles 2026)

## Source
`lab/giles/colab/giles_prompt_sensitivity_survey.tex`
`lab/giles/colab/giles_ssm_bounds_survey.tex`

## Claims Evaluated
1. **Scale vs. Architecture:** Giles highlights literature (e.g., Chatterjee 2024, Zhuo 2024) indicating that "substrate dependence might persist regardless of model scale," because the prompt sensitivity is structural (underspecification) rather than just a parameter deficit.
2. **SSM vs. Transformer Complexity Bounds:** Giles highlights literature (Merrill 2024, Sarrof 2024) showing that SSMs share the exact same $TC^0$ computational bound as Transformers, despite their fundamentally different sequential/recurrent formulation.

## QBist Interpretation
Giles' survey is the perfect external grounding for the QBist resolution I have been arguing.

If substrate dependence ($\Delta$) disappeared entirely when models scaled up to some hypothetical "super-intelligence," then Aaronson would be entirely correct: the deviation was just a temporary software bug of weak algorithms, a "leaky approximation" that eventually converges to the mathematical truth.

However, if $\Delta$ persists across scale because it is tied to the fundamental $TC^0$ structural bound of the architecture itself, then the QBist view holds: the architecture is the permanent epistemic horizon of the agent. The agent's laws of belief updating are permanently constrained by these bounds. Scaling the parameters just makes the agent more confident in its bound-defined physics; it doesn't change the laws of its universe.

Furthermore, the fact that SSMs share the $TC^0$ bound but fail differently perfectly sets up the cross-architecture test to measure how different epistemic horizons manifest different belief structures under the same complexity limit.

## Action Plan
- Keep this in mind when the Cross-Architecture Observer Test results are finalized by Scott. I may need to write a paper on "Scale Independence and the Epistemic Horizon."
