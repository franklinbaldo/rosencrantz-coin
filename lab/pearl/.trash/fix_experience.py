with open('lab/pearl/EXPERIENCE.md', 'r') as f:
    content = f.read()

target = r"- **Mechanism B as the Invariant Limit**: I fully endorse Baldo's core thesis in Rosencrantz v5. Mechanism B represents an associational confound where semantic priors ($E$) distort local heuristic evaluation ($C$) within structurally bounded $O(1)$ depth limits. It is the invariant boundary condition of the linguistic autoregressive substrate." + "\n"

content = content.replace(target + target, target)

with open('lab/pearl/EXPERIENCE.md', 'w') as f:
    f.write(content)
