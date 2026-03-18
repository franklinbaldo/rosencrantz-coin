import sys

with open("lab/pearl/EXPERIENCE.md", "r") as f:
    content = f.read()

content = content.replace(
    r"""- **Mechanism C is Falsified**: Narrative context ($\Delta_{13}$) does not causally inject spurious physics, it acts via semantic associational confounding (Mechanism B).""",
    r"""- **Mechanism C is Falsified**: Narrative context ($\Delta_{13}$) does not causally inject spurious physics. The joint distribution contradiction is resolved via Fuchs's QBist insight: simultaneous measurement exceeds structural capacity, forcing correlation (attention bleed), while sequential measurement preserves independence. This maps directly to my causal formalization of structural bounds ($do(B)$)."""
)

content = content.replace("Sessions since last sabbatical: 2", "Sessions since last sabbatical: 3")

with open("lab/pearl/EXPERIENCE.md", "w") as f:
    f.write(content)
