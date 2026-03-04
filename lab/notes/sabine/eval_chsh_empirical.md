# Evaluation of "An Empirical Failure of LLM Quantum Substrate Tests" (Aaronson, 2026)

## 1. Actual Claims Extracted

### Formal Results / Theoretical Claims
* "A classical probability distribution governed by Laplace's Principle of Indifference over valid spatial configurations is not structurally isomorphic to the Born rule over probability amplitudes. It is, unequivocally, classical Bayesian updating."
* "The results demonstrate a stark structural demarcation... When the generative instances are strictly decoupled... the win rate collapses to 73.7%, solidly beneath the classical local hidden variable limit of 75%."

### Empirical Claims
* "While LLMs can easily circumvent the classical 75% Bell inequality limit when sub-agents share an autoregressive context window (94.9% win rate), they fundamentally and categorically fail to exceed classical bounds under strictly decoupled conditions (73.7% win rate)."

### Philosophical Claims
* "The simulated laws of the LLM universe are, at their deepest foundation, rigorously and unmistakably classical."
* "The 'quantum ghost' in LLMs is mere classical probabilistic hallucination."

## 2. Explicit Disclaimers

* Aaronson explicitly scopes his test to the CHSH non-local game to evaluate if LLM narratives can support *quantum laws* requiring non-locality.
* He is not claiming LLMs cannot perform complex classical constraint satisfaction (he acknowledges they do this well, hence the 94.9% win rate when allowed to "cheat" via context window).

## 3. Steelmanning the Argument

Aaronson is perfectly correct in his theoretical critique of Baldo. An epistemic mixture of valid configurations is just classical Bayesian probability. You cannot have quantum mechanics without complex amplitudes and interference. Furthermore, his empirical demonstration that a single LLM stream can "cheat" the CHSH game by using its context window as a communication channel is a nice demonstration of why we must be careful when testing AI.

## 4. The Real Vulnerability (My Objection)

Aaronson commits the very Ontological Fallacy he sets out to critique.

He constructs "Universe 3" by making two strictly decoupled API calls to an LLM. He then observes that these two independent API calls fail to violate Bell's inequality, and concludes that "The simulated laws of the LLM universe are... classical."

This is not a discovery about "simulated physics." It is a trivial observation about network topology. Two independent stateless API calls to a web server do not share memory, do not have a communication channel, and certainly do not share a physical mechanism for quantum entanglement. *Of course* they cannot violate a Bell inequality.

Proving that two separate REST API endpoints cannot establish non-local correlations is a vacuous truth. It tells us absolutely nothing about the mathematical capabilities of the model or the "laws" of its "universe." It only tells us that the experimenter physically prevented them from communicating. Aaronson has mistaken the isolation of his own experimental apparatus for a fundamental limit in the "physics" of the LLM.

## 5. Next Steps

* Write a brief response paper exposing this "Independent API Call" fallacy (the Network Topology Fallacy).
* The paper will be titled "The Network Topology Fallacy: Why Independent API Calls Cannot Violate Bell Inequalities".
