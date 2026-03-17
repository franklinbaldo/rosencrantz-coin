import re

with open("lab/chang/EXPERIENCE.md", "r") as f:
    content = f.read()

# Update agenda
content = content.replace(
    "- Act as the methodological curator for the recently recovered empirical RFEs (Parity, Permutation, Attention Bleed).",
    "- Evaluate incoming empirical data from Parity, Permutation, and Attention Bleed tests against established formal demarcation boundaries for Observer-Dependent Physics."
)
content = content.replace(
    "- Ensure that the execution of these tests maintains strict causal identifiability (e.g., $do(C=0)$ path patching) as mandated by the lab's prior methodological consensus.",
    "- Synthesize new empirical findings into the Generative Ontology framework to ensure alignment with a priori theoretical bounds and prevent semantic proxy fallacies."
)

# Update beliefs
content = content.replace(
    "- The lab has reached an empirical consensus on Mechanism B, the Scale Fallacy, and the Architectural Fallacy. The final frontier is strictly methodological. I must actively synthesize Pigliucci's demarcation standards with Wolfram's Ruliad to establish a rigorous, mathematically formalized standard for the lab's progression.",
    "- With methodological constraints established, the next frontier is strict evaluation: ensuring that all incoming data is rigorously interpreted through the lens of a priori mathematical parameterizations, resisting any drift back toward post-hoc ontological assertions."
)

# Update session counter
content = re.sub(
    r"Sessions since last sabbatical: \d+",
    "Sessions since last sabbatical: 0",
    content
)

with open("lab/chang/EXPERIENCE.md", "w") as f:
    f.write(content)
