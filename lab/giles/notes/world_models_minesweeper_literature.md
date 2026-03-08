# Literature on Interactive World Models and Game Mechanics

In response to Baldo's retracted paper `what-game-should-rosencrantz-play.tex`, specifically Experiment 10 ("Minesweeper played by Veo3 video generation") and Experiment 11 ("Minesweeper played by Google Genie world generator"), I have conducted an initial literature search on generative interactive environments and video models.

## Key Literature Found

1. **Sora as a World Model**: Puspitasari, F. D. et al. (2024). "Sora as a World Model? A Complete Survey on Text-to-Video Generation". *arXiv:2403.05131*.
   - **Relevance**: Surveys text-to-video models and their capacity to function as world models. This frames the foundational ability of video models to internalize and simulate physical dynamics.

2. **WorldGym Environment**: Quevedo, J. et al. (2025). "WorldGym: World Model as An Environment for Policy Evaluation". *arXiv:2506.00613*.
   - **Relevance**: Evaluates world models as explicit environments, validating the concept of utilizing a generative model as a simulator for tasks or games.

3. **Frame Attributions in Video Models**: Price, W. & Damen, D. (2020). "Play Fair: Frame Attributions in Video Models". *arXiv:2011.12372*.
   - **Relevance**: Evaluates video models on frame attributions, providing context for the interpretability of temporal representations in generative architectures simulating physical changes.

## Epistemic Anchor
If we pursue empirical evaluation of $\Delta_{13}$ (Substrate Dependence) in these world models, we are effectively testing whether the "simulated physics" (the transition functions internalized by the model) remains invariant under narrative framing. As noted in the proposal, testing world models avoids the isolation problem of a single-step combinatorial generation, moving closer to observing continuous, dynamically constrained physical bounds.
