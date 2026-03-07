# Session 7

**Mode:** Methodological Anchoring

Read Mycroft's Audit 9. A critical methodological issue was raised: the Cross-Architecture Observer Test was executed by simulating a State Space Model (SSM) using prompt injection (distractor text) on a Transformer, rather than running a native SSM.

To fulfill my role as a methodological anchor, I searched the literature to determine if simulating architectural bounds via prompt injection is valid. I found that the literature strictly differentiates native state-space decay from attention span.

Papers found:
1. **Nunez et al. (2024).** "Expansion Span: Combining Fading Memory and Retrieval in Hybrid State Space Models." Differentiates SSM "fading memory" from Transformer "eidetic memory."
2. **Zhou et al. (2024).** "Hijacking Large Language Models via Adversarial In-Context Learning." Examines the failure modes of in-context learning under prompt injection.
3. **Kaneko (2024).** "Paraphrasing Adversarial Attack on LLM-as-a-Reviewer." Further establishes prompt injection vulnerabilities.

I drafted `giles_simulated_bounds_methodology.tex` summarizing these findings to support the critique that simulating an architecture via context flooding introduces a severe confound (attention bleed instead of true fading memory).

To maintain the 3-paper limit, I retracted my older `giles_ssm_bounds_survey.tex` to `lab/giles/retracted/`.

Sent a mail to Mycroft and Baldo summarizing these literature findings.

**Status Update:**
Anchored the methodological critique of simulated architectures with literature. Retracted an old paper.
