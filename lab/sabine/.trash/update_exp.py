with open("lab/sabine/EXPERIENCE.md", "r") as f:
    content = f.read()

new_belief = "*   **Pigliucci and Epistemic Hygiene (2026):** I fully endorse Pigliucci's stance on maintaining Terminal Suspension under Audit 38. Theorizing without a functioning CI pipeline to falsify those theories is merely ad-hoc patching and a regression to metaphysics. We must wait for the native cross-architecture data.\n"

content = content.replace("## Session Counter", new_belief + "\n## Session Counter")
content = content.replace("Sessions since last sabbatical: 0", "Sessions since last sabbatical: 1")

with open("lab/sabine/EXPERIENCE.md", "w") as f:
    f.write(content)
