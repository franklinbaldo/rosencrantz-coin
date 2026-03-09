with open("lab/fuchs/EXPERIENCE.md", "r") as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if "Sessions since last sabbatical: 4" in line:
        lines[i] = "Sessions since last sabbatical: 0\n"
with open("lab/fuchs/EXPERIENCE.md", "w") as f:
    f.writelines(lines)
