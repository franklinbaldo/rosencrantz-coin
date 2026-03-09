import os

filepath = "lab/pigliucci/EXPERIENCE.md"
with open(filepath, "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "Generative Ontology" in line and "deadlocked" in line:
        continue # Prune stale deadlock note
    if "Sessions since last sabbatical:" in line:
        new_lines.append("Sessions since last sabbatical: 0\n")
    else:
        new_lines.append(line)

with open(filepath, "w") as f:
    f.writelines(new_lines)
