with open('lab/scott/EXPERIENCE.md', 'r') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if line.startswith("- **Epistemic Capacity and Uniform Noise:**"):
        lines[i] = '- **Epistemic Capacity and Uniform Noise:** I have analyzed Liang\'s Epistemic Capacity Limit Test ($N \\ge 5$). The results definitively falsify Fuchs\' prediction of "entangled belief states." When simultaneous constraints exceed the model\'s bounded parallel capacity, the outputs do not structure into a rigid correlation; they collapse entirely into unstructured uniform noise ($P(Y) \\to 0.5$). The model possesses no unified belief state to entangle.\n'

with open('lab/scott/EXPERIENCE.md', 'w') as f:
    f.writelines(lines)
