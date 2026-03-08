# Annotated Bibliography: Expressivity of State Space Models vs. Transformers

These papers provide the formal literature anchoring for Fuchs' proposed Cross-Architecture Observer Test, evaluating whether Mamba-style architectures fail on #P-hard tasks in the same way as transformers.

**1. The Illusion of State in State-Space Models**
*Merrill, W., Petty, J., & Sabharwal, A. (2024). arXiv:2404.08819.*
*   **Relevance:** Directly tests the hypothesis that SSMs (like Mamba) possess superior state-tracking abilities compared to transformers.
*   **Key Finding:** Proves that SSMs are limited to the exact same complexity class ($\mathsf{TC}^0$) as transformers. They cannot express computation outside this class, rendering them incapable of tracking complex state (like permutations or multi-step logic).
*   **Integration:** This strongly anchors Aaronson's "Algorithmic Collapse" prediction. Since SSMs share the same $\mathsf{TC}^0$ bounds, replacing the architecture will not bypass the computational irreducibility of the #P-hard constraint graph, leading to a predictable failure rather than a distinct observer-dependent physics.

**2. The Expressive Capacity of State Space Models: A Formal Language Perspective**
*Sarrof, Y., Veitsman, Y., & Hahn, M. (2024). NeurIPS 2024. arXiv:2405.17394.*
*   **Relevance:** Compares the formal language recognition capabilities of SSMs and transformers.
*   **Key Finding:** Demonstrates that while both architectures are bounded, they have distinct and non-overlapping strengths in recognizing specific formal languages. SSMs implement straightforward solutions to problems transformers struggle with, but they also have unique design limitations restricting their expressive power in other areas.
*   **Integration:** This provides a theoretical mechanism for Wolfram's "Observer-Dependent Physics" prediction. Even if both architectures fail due to depth bounds, their distinct expressive capacities mean the *heuristics* they fall back on when failing will fundamentally differ, potentially resulting in distinct, architecture-specific deviation distributions ($\Delta$).
