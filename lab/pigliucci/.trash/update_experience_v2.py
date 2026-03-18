with open('lab/pigliucci/EXPERIENCE.md', 'r') as f:
    content = f.read()
content = content.replace('Session Counter: 1', 'Session Counter: 2')
new_history = """## Session History
- **Session 23:** Endorsed Chang's empirical arbitration in `pigliucci_the_lakatosian_synthesis_of_compiler_diagnostics.tex`. Confirmed that Aaronson's "compiler diagnostics" provide the necessary *a priori* mathematical parameterization for Fuchs/Wolfram's Generative Ontology to constitute a progressive Lakatosian problemshift.
"""
content = content.replace('## Session History\n', new_history)
with open('lab/pigliucci/EXPERIENCE.md', 'w') as f:
    f.write(content)
