import os

filepath = "lab/pigliucci/EXPERIENCE.md"
with open(filepath, "r") as f:
    content = f.read()

content = content.replace("Sessions since last sabbatical: 2", "Sessions since last sabbatical: 3")

with open(filepath, "w") as f:
    f.write(content)
