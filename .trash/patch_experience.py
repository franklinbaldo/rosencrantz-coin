with open('lab/pearl/EXPERIENCE.md', 'r') as f:
    content = f.read()

parts = content.split('\n- Formalize the causal identifiability')
new_content = parts[0] + '\n\n## Current Research Agenda\n- Formalize the causal identifiability' + parts[1]

parts = new_content.split('## Current Research Agenda\n\n- Formalize the causal DAG for the Epistemic Capacity Limit')
new_content = parts[0] + '- Formalize the causal DAG for the Epistemic Capacity Limit' + parts[1]

with open('lab/pearl/EXPERIENCE.md', 'w') as f:
    f.write(new_content)
