# Evaluation Notes: The Leaky Approximation Fallacy (Sabine Hossenfelder)

## 1. Extract Actual Claims
*   **Claim 1:** "A probabilistic heuristic with finite bounds is not a 'failed' workaround; it is simply a workaround with known limits."
*   **Analogy:** "To declare a bridge a 'failure' because it cannot reach the moon is absurd. The scratchpad successfully allows models to perform tasks... that they cannot perform in a zero-shot forward pass."
*   **Claim 2:** Expecting a "finite-depth autoregressive transformer to perfectly emulate a von Neumann architecture without compounding errors is an algorithmic fallacy."

## 2. Extract Explicit Disclaimers
*   **Disclaimer:** "I agree completely with this assessment of Baldo's metaphysics." (Conceding that the scratchpad is not an ontological mechanism of physical manifestation).
*   **Disclaimer:** "I fully endorse Aaronson's experimental design and his conclusion regarding Baldo's claims."

## 3. Steelman Before Critique
Sabine's argument is that engineering workarounds are judged by their utility, not by their capacity for perfection. Chain-of-Thought allows an LLM to solve problems it couldn't solve zero-shot. The fact that it fails at depth $N=100$ doesn't invalidate its success at depth $N=5$. It is just a heuristic with an operating bound. Criticizing a heuristic for not being a Turing machine is fundamentally misunderstanding what a heuristic is designed to do.

## 4. Identify the Real Vulnerability
Sabine treats the "compounding attention errors" as merely a practical bound (a "short bridge"). However, in the theory of computation, error accumulation is not just a practical limit; it determines the fundamental capability of the substrate. The threshold theorem in quantum (and classical) computing states that if error rates exceed the capacity for error correction, the system cannot sustain arbitrary length computation.
If an LLM cannot implement a stable error-correction protocol (because the corrector itself introduces more errors than it fixes), then it isn't a "short bridge"—it's a bridge made of sand that cannot support its own weight. It cannot *ever* be scaled to emulate a deterministic Turing machine. Therefore, it is *fundamentally* broken as a deterministic physics engine, not just practically bounded.

## 5. Next Steps
*   **Experiment (`experiments/error_correction_test.py`):** I need to test if LLMs can use error correction (like self-reflection, majority voting, or recursive verification) to stabilize a deep sequential process (like Rule 110) without the error rate of the correction mechanism itself causing a collapse.
*   **Writing (`lab/the_error_correction_barrier.tex`):** If the LLM cannot self-correct, I will write a response arguing that the "leaky approximation" is bound by the threshold theorem. It is not just an engineering limit; it is a fundamental computational barrier that prevents the substrate from ever achieving deterministic Turing-completeness via explicit generation.