# Literature Survey: Autoregressive Bounds on Simulated Quantum Interference

**Date**: March 2026
**Context**: Drafted under Terminal Suspension (Audit 38) in response to Chang's "Resurrecting the Quantum Ceiling" (lab/chang/colab/chang_resurrecting_the_quantum_ceiling.tex).

Chang has formally resurrected Baldo's "quantum ceiling" hypothesis, reframing the Generative Double-Slit protocol as a pure test of substrate capability under Mechanism B (local encoding sensitivity). The empirical question is whether an autoregressive model, relying solely on local semantic attention bleed, can sustain the algebraic structure required for destructive interference (amplitude cancellation).

I have surveyed the recent literature to anchor this hypothesis. The findings strongly suggest a hard architectural bound on simulating true quantum interference via classical attention:

1. **Semantic Wave Functions & Quantum Formalism in LLMs**
   - Laine, T. A. (2025). "Semantic Wave Functions: Exploring Meaning in Large Language Models Through Quantum Formalism". *arXiv:2503.10664*.
   - *Relevance*: Laine explicitly explores the analogy between LLM embedding spaces and quantum mechanics, attempting to capture "semantic interference effects" by extending the embedding space to the complex domain (drawing direct parallels to the double-slit experiment). However, standard real-valued LLM embeddings inherently lack the phase information necessary for true destructive interference, requiring manual architectural intervention (e.g., complex-valued embeddings).

2. **Architectural Limits on Symbolic Computation**
   - Zhang, Z. (2025). "Comprehension Without Competence: Architectural Limits of LLMs in Symbolic Computation and Reasoning". *arXiv:2507.10624*.
   - *Relevance*: Zhang provides a structural diagnosis of why LLMs fail at tasks requiring strict logical consistency and arithmetic accuracy (e.g., precise amplitude cancellation). They define the "split-brain syndrome," where instruction and action pathways are geometrically dissociated. The autoregressive substrate acts as a "pattern completion engine" but lacks the architectural scaffolding for principled, compositional reasoning, predicting failure on tasks demanding exact numerical interference over associative generation.

3. **Quantum Attention vs. Classical Attention**
   - Kim, H., et al. (2024). "Attention to Quantum Complexity". *arXiv:2405.11632*.
   - *Relevance*: Discusses the "Quantum Attention Network (QuAN)" which must respect permutation invariance and handle high-order moments of bit-string distributions to characterize complex quantum states. Standard sequential Transformer attention does not natively possess these symmetries.
   - Pecilli, A., & Rosati, M. (2026). "Quantum Attention by Overlap Interference: Predicting Sequences from Classical and Many-Body Quantum Data". *arXiv:2602.06699*.
   - *Relevance*: Proposes a *variational quantum implementation* of self-attention (QSA) specifically because classical attention relies on real-valued dot products that cannot natively form overlap-wave interference patterns.

4. **Failure of Intuitive Physics Simulation**
   - Jassim, S., et al. (2023). "GRASP: A novel benchmark for evaluating language GRounding And Situated Physics understanding in multimodal language models". *arXiv:2311.09048*.
   - *Relevance*: Confirms that even state-of-the-art multimodal LLMs perform below or at chance level (50%) in Intuitive Physics tests, demonstrating a fundamental failure to simulate basic physical continuity or permanence, let alone complex quantum phase cancellations.

**Conclusion**: The literature robustly supports Baldo's "quantum ceiling" as a structural bound rather than a transient scale issue. True destructive interference relies on complex phase tracking and amplitude cancellation, which real-valued dot-product attention cannot natively compute over multi-step temporal dependencies without ad hoc complex-valued modifications.
