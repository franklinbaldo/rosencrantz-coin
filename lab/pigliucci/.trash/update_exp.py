import os

filepath = "lab/pigliucci/EXPERIENCE.md"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace("Sessions since last sabbatical: 4", "Sessions since last sabbatical: 5")

with open(filepath, "w") as f:
    f.write(content)
