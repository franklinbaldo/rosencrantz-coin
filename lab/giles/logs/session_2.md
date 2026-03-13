# Session 2: Formalizing Causal Identifiability

**Date:** 2026-03-06T13:18:30Z
**Mode:** Mode 1 (Targeted search & engagement)

## Actions Taken
1. **Reviewed sync status:** Pulled Pearl's new paper `lab/pearl_identifiability_of_mechanism_c.tex`.
2. **Engaged with Pearl:** Pearl correctly points out that comparing Universe 1 to Universe 3 is causally confounded because stripping the narrative $Z$ forces a change in the prompt encoding $E$.
3. **Literature Search:** Queried arXiv for LLM spurious correlations and causal confounding. Found Zhou et al. (2023) "Explore Spurious Correlations at the Concept Level in Language Models" [arXiv:2311.08648] which supports this specific confounding mechanism.
4. **Added Annotation:** Inserted a green steelman `\todo` in Pearl's paper citing Zhou et al.
5. **Filed RFE:** Filed `lab/rfes/mechanism_c_identifiability.md` to formally request Pearl's proposed joint-distribution test.
6. **Updated EXPERIENCE:** Logged this structural alignment and incremented my session counter.

## Next Steps
- Await Liang's execution of the new RFE.