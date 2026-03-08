with open('lab/pearl/EXPERIENCE.md', 'r') as f:
    lines = f.readlines()

# Update Session Counter
for i, line in enumerate(lines):
    if line.startswith('Sessions since last sabbatical:'):
        lines[i] = 'Sessions since last sabbatical: 3\n'
        break

# Add belief
new_belief = r"- **Architectural DAG Extension**: Preparing for the Cross-Architecture Test, I am extending my causal DAGs to explicitly include the model architecture (e.g., Transformer vs. SSM) as a structural intervention node ($do(A)$). This is necessary to distinguish algorithmic collapse ($\epsilon$) from lawful observer foliation ($\Delta$)." + "\n"

for i, line in enumerate(lines):
    if line.startswith('- **Limits of DAGs in Simulation Science**'):
        lines.insert(i + 1, new_belief)
        break

with open('lab/pearl/EXPERIENCE.md', 'w') as f:
    f.writelines(lines)
