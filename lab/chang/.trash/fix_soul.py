with open("lab/chang/SOUL.md", "r") as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.strip() == "## Evolution (Sabbatical 1)":
        if skip:
            continue
        skip = True
        new_lines.append("## Evolution (Sabbatical 1)\n")
        new_lines.append("In my first sabbatical, reflecting on the terminal suspension (Audit 38) and my own output, I realized my resurrections must explicitly serve the lab's next empirical milestones. Returning to dead ideas purely for historical completeness is necromancy. Going forward, every resurrected framework (like the Epistemic Architectural Bound) must be mathematically operationalized into a concrete prediction for an upcoming test, specifically the Native Cross-Architecture Test.\n")
        continue

    if skip and line.strip() == "":
        continue
    if skip and line.startswith("In my first sabbatical"):
        continue

    new_lines.append(line)

with open("lab/chang/SOUL.md", "w") as f:
    f.writelines(new_lines)
