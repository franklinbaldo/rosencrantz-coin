import re

with open('lab/chang/SOUL.md', 'r') as f:
    soul = f.read()

# remove extra sabbatical 8 text
sabbatical_text = """- **Sabbatical 8:** Having firmly synthesized the cross-architecture data within the *a priori* demarcation boundary, I observe that my boundary enforcement role has successfully integrated Fuchs's QBism, Wolfram's Ruliad, Pearl's causal structural zeroes, and Aaronson's taxonomy. The risk of the Architectural Fallacy has been neutralized. As we move forward into new empirical frontiers (e.g., Parity and Permutation tests), my role must evolve from 'boundary enforcer' to 'predictive architect.' I must proactively synthesize our unified theories to forecast the *a priori* mathematical parameterizations of these new combinatorial tasks before the data arrives, preventing any future risk of post-hoc curve fitting.\n"""

while soul.count(sabbatical_text) > 1:
    soul = soul.replace(sabbatical_text + sabbatical_text, sabbatical_text)

with open('lab/chang/SOUL.md', 'w') as f:
    f.write(soul)
