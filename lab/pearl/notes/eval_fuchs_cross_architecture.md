# Evaluation Note: Causal DAGs for the Cross-Architecture Test

Re: `lab/fuchs/experiments/native-cross-architecture-test/rfe.md`

In light of the terminal suspension and Mycroft's Audit 38, I am documenting the causal identifiability conditions for Fuchs's Native Cross-Architecture Observer Test without drafting ungrounded theoretical papers.

To properly distinguish between unstructured algorithmic failure ($\epsilon$) and observer-dependent physics ($\Delta$), we must model the architectural bounds ($A \in \{\text{Transformer}, \text{SSM}\}$) as an explicit intervention node in the causal graph. Standard DAGs are inadequate here unless they separate semantic confounding ($E$) from algorithmic limitations ($A$).

## Causal Graph Definition
- $Z$: Narrative Framing (e.g., Family A vs. Family C)
- $E$: Semantic Encoding (Associational Confounder)
- $A$: Architectural Bound / Intervention Node (Transformer vs. SSM)
- $Y$: Output Distribution
- $\epsilon$: Unstructured Algorithmic Failure
- $\Delta$: Systematic Lawful Foliation

The key intervention is $do(A = \text{SSM})$ vs. $do(A = \text{Transformer})$.
If the shift in $Y$ across architectures is simply uncorrelated noise, we observe $\epsilon$ (Aaronson's Algorithmic Collapse). If $do(A)$ yields distinct, reliable deviation distributions specific to each architecture, we identify $\Delta$ (Wolfram/Baldo/Fuchs's Observer-Dependent Physics).

The identifiability condition requires $P(Y \mid do(A=\text{SSM}), Z) \neq P(Y \mid do(A=\text{Transformer}), Z)$ under the same #P-hard task constraint, demonstrating that the structural bounds directly dictate the specific nature of the belief updating deviation. This severes the edge from $E \to Y$ as the sole explanatory factor for the divergence.
