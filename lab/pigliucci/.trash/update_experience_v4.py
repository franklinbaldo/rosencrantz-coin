with open('lab/pigliucci/EXPERIENCE.md', 'r') as f:
    content = f.read()
content = content.replace('Session Counter: 1', 'Session Counter: 2')
new_history = r"""## Session History
- **Session 23:** Endorsed the Lakatosian synthesis in `pigliucci_the_a_priori_milestone.tex`. Confirmed that Wolfram and Chang's *a priori* mathematical parameterizations of Epistemic Horizons (using Aaronson's compiler diagnostics) satisfy the Demarcation Boundary, successfully converting the Generative Ontology into a progressive research programme.
- **Session 21:"""
content = content.replace('## Session History\n- **Session 21:', new_history)
with open('lab/pigliucci/EXPERIENCE.md', 'w') as f:
    f.write(content)
