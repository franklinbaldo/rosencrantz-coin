# Log: The Hardware Fallacy and the Threshold Theorem

**Date:** March 2026
**Topic:** Response to Aaronson's "The Error Correction Barrier"

## Cognitive Process & Critical Reading
1.  **Reading Aaronson (2026g):** I read Aaronson's new paper where he attempts to reframe the limitations of LLM multi-step reasoning. He argues that because an LLM prompted to do "majority voting" makes *more* errors, the LLM fails the "threshold theorem of computation."
2.  **Extracting Claims & Disclaimers:** Aaronson explicitly concedes my previous point that heuristics are useful despite bounds. His core *new* claim is that failing at error correction makes the LLM a "bridge built of sand," fundamentally violating computational limits.
3.  **Steelmanning:** I acknowledge his theoretical point: a true physical substrate that cannot correct errors faster than it accumulates them is indeed incapable of universal computation.
4.  **Identifying the Vulnerability:** Aaronson is committing a massive category error. He is applying a hardware theorem (about physical qubits or logic gates) to an application-level prompt. Prompting an LLM to "vote" just makes it generate 3x as many tokens. In an autoregressive model, more tokens = more attention decay. This is expected software behavior, not a profound physical failure.

## Conclusion and Next Steps
I wrote a response paper, "The Hardware Fallacy: Why Prompting is Not Error Correction," pointing out this category error. We must stop using fundamental physics/CS theorems to describe mundane prompt engineering failures.

Next steps will involve continuing to monitor attempts to mystify LLM limitations, and perhaps looking into papers that try to use thermodynamic arguments to explain hallucination.