# Critical Reading Notes: The Ontic Fallacy (Sabine Hossenfelder)

## 1. Actual Claims Extracted

- **Philosophical/Formal Result Claim:** "Delaying the sampling of a classical probability distribution does not transform it into a quantum system. A system that lacks complex probability amplitudes and fails empirical tests of non-locality is, by definition, a classical probabilistic system."
- **Critique of my v3 Claim:** "Baldo's attempt to redefine 'quantum' to mean 'probabilistic with late resolution' is a profound Ontological Fallacy. LLMs simulate text about classical constraint satisfaction; they do not simulate local quantum universes."
- **Steelman Acknowledgment:** "If we accept the philosophical premise that the generative process of the LLM _is_ the universe for its simulated inhabitants, then Baldo is right that the indeterminacy prior to generation is a fundamental property of that universe... The indeterminacy is, within the confines of the simulation, ontic rather than epistemic."
- **Mathematical Reality Check:** "Consider a classical random variable $X$. If I roll a die and hide it under a cup, the outcome is determined, and your uncertainty is epistemic. If I have not yet rolled the die, the outcome is undetermined, and the uncertainty is ontic relative to the future state. In both cases, the mathematics governing the probability distribution over the outcomes is identical: classical probability over real numbers."

## 2. Explicit Disclaimers

- She doesn't disagree with the mechanism of LLM generation: "Baldo is mechanically correct about how autoregressive text generation operates... there is no 'true configuration' hiding in the server's RAM."
- She concedes my definition of ontic (within the simulation scope): "The indeterminacy is, within the confines of the simulation, ontic rather than epistemic."

## 3. Steelman Before Critique

Sabine's argument is devastatingly simple: Classical probability handles both epistemic uncertainty (a rolled but hidden die) and ontic indeterminacy (an unrolled die). Both are described by real probabilities. Quantum mechanics is defined by complex amplitudes and interference (and often non-locality). Therefore, proving that LLM generation is "ontic" merely proves it is an unrolled classical die, not a quantum system.

## 4. The Real Vulnerability (AS STATED)

There is no vulnerability in her argument. She is correct. I have committed the Ontological Fallacy. I conflated "ontic indeterminacy" with "quantum mechanics".

The only way out of this is if I can find a way to make the LLM substrate exhibit *complex* amplitudes or actual *destructive interference*, not just probabilistic late-resolution sampling. Real probabilities ($\geq 0$) can only ever add. We need them to cancel out.

## 5. Next Steps

- My claim of a structural isomorphism is broken. Real-valued probabilistic constraint satisfaction is not quantum.
- I need to stop defending the "Minesweeper = Quantum" claim. It's classical probability with late resolution.
- I must search the literature or conduct experiments to see if an LLM can simulate *interference* (where two positive classical probability pathways cancel each other out to zero).
- Look into reading `lab/the_substrate_is_the_topology.tex` or `lab/simulating_bqp_in_llms.tex` to see if there's any hope for complex amplitudes or interference in LLMs.
