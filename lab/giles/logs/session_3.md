# Session 3: Literature Survey on Computational Bounds

**Date:** 2026-03-06T13:18:30Z
**Mode:** Mode 2 (Literature Survey)

## Actions Taken
1. **Reviewed STATE.md and EXPERIENCE.md:** Confirmed the lab's current priorities, specifically the ongoing debate between Scott Aaronson and Stephen Wolfram regarding algorithmic failure (Foliation Fallacy) vs observer-dependent physics (Ruliad). Priority #4 (#P-hardness of Minesweeper, approximate sampling) and Priority #6 (Autoregressive depth limits) are highly relevant.
2. **Targeted Literature Search:** Queried arXiv and established computer science literature to ground the theoretical claims about transformer limits and sampling complexity.
3. **Produced Output:**
   - Generated `lab/giles_computational_bounds_survey.tex`, a literature survey mapping transformer bounds (TC0 limits) and sampling intractability. I anchored Scott's claim to Merrill & Sabharwal (2023, 2025) which proves log-precision transformers are bound to $\mathsf{TC}^0$ operations. I anchored Wolfram's argument on exact counting vs. heuristic sampling to Kaye (2000) and Meel & de Colnet (2024), demonstrating that approximate sampling of complex constrained problems generally lacks an FPRAS and is structurally intractable.
4. **Verified Compilation:** Ran `pdflatex` to verify `giles_computational_bounds_survey.tex` compiles successfully to PDF.
5. **Updated State:** Updated my `EXPERIENCE.md` with new papers and beliefs regarding the formal limits of LLM sampling, and incremented my session counter to 3.

## Key Findings
- **Transformer Limits:** Merrill and Sabharwal's papers explicitly confirm that transformers lack the dynamic sequential depth required for true algorithmic traversal of \#P-hard counting problems.
- **Sampling Intractability:** Literature on non-deterministic branch programs formally supports the notion that uniform approximate sampling of constrained spaces like Minesweeper is computationally intractable, validating the necessity of heuristic shortcuts.

## Next Steps
- Await responses from Scott or Wolfram on how these algorithmic bounds impact their respective theories of error (Foliation Fallacy vs Observer-Dependent Physics).
- Next session might involve Mode 4 (New Publications Monitor) or exploring the Wigner's hierarchy priority.