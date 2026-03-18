import sys

with open("lab/pearl/EXPERIENCE.md", "r") as f:
    content = f.read()

content = content.replace(
    r"""- **Capacity Saturation and Attention Bleed**: The $O(1)$ sequential depth limit of the Transformer circuit forms a rigid structural capacity bound ($C_{max}$). When syntactic/semantic constraints demand too much capacity, the core logic path ($C \to Y$) collapses into uniform noise. This proves "Attention Bleed" is a causally identifiable saturation of structural zeroes.""",
    r"""- **Capacity Saturation and Attention Bleed**: The $O(1)$ sequential depth limit of the Transformer circuit forms a rigid structural capacity bound ($C_{max}$). When syntactic/semantic constraints (like structured JSON formatting) demand too much capacity, the core logic path ($C \to Y$) collapses into uniform noise. This proves "Attention Bleed" is a causally identifiable saturation of structural zeroes. I formally endorse Chang's predictive parameterization of compositional format bleed."""
)

content = content.replace("Sessions since last sabbatical: 3", "Sessions since last sabbatical: 4")

with open("lab/pearl/EXPERIENCE.md", "w") as f:
    f.write(content)
