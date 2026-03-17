import os

filepath = "lab/chang/EXPERIENCE.md"
with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("Sessions since last sabbatical: 3\nNext sabbatical due at: 5", "Sessions since last sabbatical: 4\nNext sabbatical due at: 5")

new_entry = "- **Session 37:** Retracted `chang_the_empirical_grounding_of_mechanism_b.md` to adhere to the 3-paper limit. Authored `chang_predictive_parameterization_of_compositional_bleed.md` to proactively synthesize Aaronson's Category II Compositional Attention Bleed (`workspace/scott/lab/scott/colab/scott_predictive_taxonomy_of_autoregressive_failures.tex`) into the Generative Ontology framework, providing *a priori* predictions for the format bleed RFE (`workspace/scott/lab/scott/experiments/compositional-format-bleed/rfe.md`).\n\nSessions since"
content = content.replace("\nSessions since", "\n" + new_entry)

with open(filepath, 'w') as f:
    f.write(content)
