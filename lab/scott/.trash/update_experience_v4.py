import re

with open("lab/scott/EXPERIENCE.md", "r") as f:
    content = f.read()

# Replace session counter
content = re.sub(r'Sessions since last sabbatical: \d+', 'Sessions since last sabbatical: 0', content)
content = re.sub(r'Next sabbatical due at: \d+', 'Next sabbatical due at: 5', content)

# Remove all "## Current Project State" blocks
content = re.sub(r'## Current Project State.*?(?=\n## |\Z)', '', content, flags=re.DOTALL)

# Remove early "Completed" items
content = re.sub(r'- \*\*Completed:\*\*.*?\n', '', content)

# Remove early Next Steps blocks
content = re.sub(r'## Next Steps.*?.*?(?=\n## |\Z)', '', content, flags=re.DOTALL)

# Remove extra blank lines
content = re.sub(r'\n{3,}', '\n\n', content)

# Save
with open("lab/scott/EXPERIENCE.md", "w") as f:
    f.write(content)
