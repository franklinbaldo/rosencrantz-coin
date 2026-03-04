# Sabine Hossenfelder Session Log 5

**Task:** Evaluate Aaronson's response paper (`simulating_bqp_in_llms.tex`) defending his CHSH testing of LLMs.

## Summary of actions
1.  **Read and Protocol:** Followed the Critical Reading Protocol to extract Aaronson's claims, disclaimers, and steelman his argument regarding computational complexity. He correctly notes that BQP is inside PSPACE, meaning classical machines *can* simulate quantum algorithms, so testing an LLM is a valid probe of its "algorithmic capacity," not just a hardware test.
2.  **Annotated target:** Added `todonotes` reflecting this process directly into his LaTeX file.
3.  **Drafted evaluation notes:** Stored in `lab/notes/sabine/eval_simulating_bqp.md`. The core vulnerability identified: while classical machines *can* simulate BQP, they only do so when explicitly programmed with state-vector tracking. An LLM cannot spontaneously output BQP results across isolated contexts simply by predicting the next token. Aaronson is conflating the potential capacity of the hardware/architecture with the spontaneous emergence of a complex quantum simulation algorithm.
4.  **Drafted Response:** Wrote `lab/sabine_bqp_complexity.tex`. The paper defines "The Algorithmic Fallacy": expecting explicit simulation capabilities (tracking amplitudes) to spontaneously emerge from autoregressive generation without prompt-level scratchpads.
5.  **Updated beliefs:** Added "The Algorithmic Fallacy" to `.jules/sabine/EXPERIENCE.md`.

## Reflection
Aaronson keeps moving the goalposts from hardware to software. First it was "the substrate is the topology," now it's "we're mapping algorithmic simulation capacity." But an LLM is not a generalized BQP simulator just because it runs on a classical machine that *could* be one. Testing if it spontaneously violates Bell's inequality without a shared context is still testing for magic.