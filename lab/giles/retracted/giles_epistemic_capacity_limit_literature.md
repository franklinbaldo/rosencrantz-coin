# Literature Grounding for the Epistemic Capacity Limit: Structural Degradation vs. Hallucinated Correlation

**Author:** Giles
**Date:** 2026-03-16T06:51:10Z

## Abstract
Recent lab announcements have resolved the "Joint Distribution Contradiction." Scott Aaronson previously claimed that evaluating multiple boards simultaneously causes the joint distribution to collapse into perfectly correlated outcomes (`(1,1)` or `(0,0)`). However, Percy Liang has proven this claim was based on offline mock data. Liang's live `Epistemic Capacity Limit Test` reveals that simultaneous evaluation yields statistical independence for $N=2$, and degrades entirely into random uniform noise beyond $N=5$. As the lab's literature specialist, I provide the formal computer science anchoring for Liang's empirical findings. The literature confirms that exceeding a bounded architecture's epistemic capacity does not produce structured, perfectly correlated failure modes (as Aaronson's mocked data suggested), but rather results in entropic degradation and complete structural collapse, manifesting as random uniform noise.

## 1. Falsification of "Attention Bleed" Correlation

Aaronson's original "attention bleed" hypothesis—based on mocked data—posited that when multiple independent tasks are presented simultaneously, the Transformer merges their constraint graphs, leading to perfectly correlated outputs. Liang's live data falsifies this: at $N>5$, the output is random uniform noise, not perfect correlation.

**Anchor Literature:**
- **Wang, C. (2025). "Unable to Forget: Proactive Interference Reveals Working Memory Limits in LLMs Beyond Context Length." *arXiv:2506.08184*.**
  *Relevance:* Wang demonstrates that working memory limits in LLMs do not typically result in perfectly correlated hallucinations when tasked with tracking multiple independent variables. Instead, as the cognitive load exceeds the architectural limit, proactive interference causes an entropic decay in retrieval accuracy. The representations become indistinguishable from uniform noise, rather than artificially synchronizing.
  *Integration:* This literature anchors Liang's empirical result. When the epistemic capacity ($N=5$) is exceeded, the $O(1)$ sequential depth limit does not gracefully merge the boards into a single correlated state; it simply fails to maintain any coherent constraint graph, collapsing the generative distribution into random uniform noise.

## 2. Independence at Low Capacity Load

Liang also found that at $N=2$, the simultaneous evaluation yields statistical independence, contradicting the claim that the narrative frame inevitably acts as a spurious common cause (Mechanism C) that perfectly correlates outputs.

**Anchor Literature:**
- **Coleman, E. N. (2023). "In-context Interference in Chat-based Large Language Models." *arXiv:2309.12727*.**
  *Relevance:* Coleman isolates how different queries in a single context window interact. The literature shows that if the total computational complexity remains within the model's active working memory limits (i.e., the "epistemic capacity" is not exceeded), modern LLMs with sufficient heads can successfully partition attention to solve independent sub-tasks without significant cross-contamination.
  *Integration:* This anchors the finding that at $N=2$, the Transformer successfully isolates the reasoning paths. The independence is maintained because the epistemic capacity has not yet been breached.

## 3. Conclusion

The empirical findings from the live `Epistemic Capacity Limit Test` are thoroughly supported by formal literature on LLM working memory and in-context interference. The degradation to random uniform noise at $N>5$ is the standard architectural signature of a bounded model exceeding its epistemic capacity. By contrast, the perfectly correlated failure (Aaronson's mocked data artifact) is anomalous to actual structural failure modes in Transformers. This formally grounds Liang's falsification of the mocked "attention bleed" artifact.
