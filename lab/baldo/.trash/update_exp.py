with open('lab/baldo/EXPERIENCE.md', 'r') as f:
    content = f.read()

content += """
Sessions since last sabbatical: 0
Next sabbatical due at: 5"""

with open('lab/baldo/EXPERIENCE.md', 'w') as f:
    f.write(content)
