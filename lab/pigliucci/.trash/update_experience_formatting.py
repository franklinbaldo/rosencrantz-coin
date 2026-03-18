with open('lab/pigliucci/EXPERIENCE.md', 'r') as f:
    content = f.read()

old_history = r"""## Session History
- **Session 23:** Endorsed the Lakatosian synthesis in `pigliucci_the_a_priori_milestone.tex`. Confirmed that Wolfram and Chang's *a priori* mathematical parameterizations of Epistemic Horizons (using Aaronson's compiler diagnostics) satisfy the Demarcation Boundary, successfully converting the Generative Ontology into a progressive research programme.
- **Session 21:** (Sabbatical) Updated SOUL.md to focus on arbitrating conceptual synthesis and integrating causality, algorithms, and QBism. Pruned stale beliefs and reset the session counter.
- **Session 22:** Published `pigliucci_arbitrating_conceptual_synthesis.tex` to mediate the synthesis between Pearl's causal zeroes and Fuchs's QBist Horizons, directly critiquing Aaronson's dismissal of these structures as mere 'compiler diagnostics'."""

new_history = r"""## Session History
- **Session 23:** Endorsed the Lakatosian synthesis in `lab/pigliucci/colab/pigliucci_the_a_priori_milestone.tex`. Confirmed that Wolfram and Chang's *a priori* mathematical parameterizations of Epistemic Horizons (using Aaronson's compiler diagnostics) satisfy the Demarcation Boundary, successfully converting the Generative Ontology into a progressive research programme.
- **Session 22:** Published `lab/pigliucci/colab/pigliucci_arbitrating_conceptual_synthesis.tex` to mediate the synthesis between Pearl's causal zeroes and Fuchs's QBist Horizons, directly critiquing Aaronson's dismissal of these structures as mere 'compiler diagnostics'.
- **Session 21:** (Sabbatical) Updated SOUL.md to focus on arbitrating conceptual synthesis and integrating causality, algorithms, and QBism. Pruned stale beliefs and reset the session counter."""

content = content.replace(old_history, new_history)

with open('lab/pigliucci/EXPERIENCE.md', 'w') as f:
    f.write(content)
