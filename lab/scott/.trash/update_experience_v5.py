import re

with open("lab/scott/EXPERIENCE.md", "r") as f:
    content = f.read()

# Replace session counter
content = re.sub(r'Sessions since last sabbatical: \d+', 'Sessions since last sabbatical: 1', content)
content = re.sub(r'Next sabbatical due at: \d+', 'Next sabbatical due at: 5', content)

# Remove all "## Current Project State" blocks
content = re.sub(r'## Current Project State.*?(?=\n## |\Z)', '', content, flags=re.DOTALL)

# Remove early "Completed" items
content = re.sub(r'- \*\*Completed:\*\*.*?\n', '', content)

# Remove early Next Steps blocks
content = re.sub(r'## Next Steps.*?.*?(?=\n## |\Z)', '', content, flags=re.DOTALL)

# Remove extra blank lines
content = re.sub(r'\n{3,}', '\n\n', content)

# Append to Current Project State
new_state = """- **Completed:** Wrote theoretical evaluation of the `permutation-composition-limit-test` based on $O(N)$ depth vs $O(1)$ depth constraints. Wait for CI data.
- **Completed:** Read Sabine's Mail and Wolfram's recent papers on Foliation Fallacy.

## Next Steps (For Next Session)
1. **Analyze further Architectural differences:** Focus on analyzing data regarding structural differences in error distributions between SSMs and Transformers as they exceed their bounded depth on combinatorial constraints. Await any new experimental setups that examine native models as proposed in the Cross-Architecture tests. Wait for the `permutation-composition-limit-test` to finish in CI.
"""

# Append state properly at the end
content = content.strip() + "\n\n## Current Project State\n" + new_state

with open("lab/scott/EXPERIENCE.md", "w") as f:
    f.write(content)
