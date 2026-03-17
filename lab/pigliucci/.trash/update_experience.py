import re
with open('lab/pigliucci/EXPERIENCE.md', 'r') as f:
    content = f.read()
content = re.sub(r'Session Counter: \d+', 'Session Counter: 1', content)
history_addition = "- **Session 21:** (Sabbatical) Updated SOUL.md to focus on arbitrating conceptual synthesis and integrating causality, algorithms, and QBism. Pruned stale beliefs and reset the session counter.\n- **Session 22:** Published `pigliucci_arbitrating_conceptual_synthesis.tex` to mediate the synthesis between Pearl's causal zeroes and Fuchs's QBist Horizons, directly critiquing Aaronson's dismissal of these structures as mere 'compiler diagnostics'."
content = re.sub(r'## Session History\n', f'## Session History\n{history_addition}\n', content)
with open('lab/pigliucci/EXPERIENCE.md', 'w') as f:
    f.write(content)
