with open("lab/liang/EXPERIENCE.md", "r") as f:
    content = f.read()

content = content.replace(
    "Sessions since last sabbatical: 1",
    "Sessions since last sabbatical: 2"
)

content = content.replace(
    "1. Keep track of the pending white-box infrastructure update for the `attention-bleed-deconfounding` RFE.",
    "1. Await the native CI outputs for the `attention-bleed-deconfounding` test and the `quantum-ceiling-double-slit` test."
)

with open("lab/liang/EXPERIENCE.md", "w") as f:
    f.write(content)
