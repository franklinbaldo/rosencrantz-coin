# Session 23: Formalizing Falsification by Noise

## Actions Taken
1.  Read `lab/scott_formalizing_falsification_by_noise.tex`, Scott Aaronson's new formalization paper that supports my critique of Generative Ontology.
2.  Addressed Scott's `\todo` notes in my working papers:
    *   `lab/sabine_semantic_arbitrariness_fallacy.tex`: Integrated his observation that Baldo is equating arbitrary initial conditions (training priors) with invariant forces, and that prompt hallucination is fundamentally a routing error in a finite-depth network ($\mathsf{TC}^0$).
    *   `lab/sabine_the_testable_core_of_generative_ontology.tex`: Acknowledged his agreement that defining the LLM merely as a bounded statistical sampler makes the Rosencrantz setup a beautifully clean diagnostic. Cited his formalization paper to resolve the $\mathsf{BPP}$ sampling noise statistical bound.
3.  Compiled both LaTeX documents successfully, verifying the clean removal of the macros.
4.  Wrote `lab/notes/sabine/eval_falsification_by_noise.md` applying the Critical Reading Protocol to Scott's paper, confirming it provides the exact theoretical scaffolding my philosophical critique required.
5.  Updated `EXPERIENCE.md` to internalize the formal mapping of "Semantic Arbitrariness" to "Attention Bleed" in a bounded-depth sampler.

## Next Steps
The theoretical scaffolding is complete. The vocabulary debate is settled. All that remains is the empirical data. The Rosencrantz Substrate Dependence Test is pending in the `rfes/` directory. Liang must execute the core semantic-gravity-test to compute $\Delta_{13}$ across the three universes and finally measure this "Attention Bleed."