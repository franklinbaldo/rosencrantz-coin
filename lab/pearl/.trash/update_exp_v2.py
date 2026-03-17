with open('lab/pearl/EXPERIENCE.md', 'r') as f:
    content = f.read()
content = content.replace('Sessions since last sabbatical: 1\nNext sabbatical due at: 5', 'Sessions since last sabbatical: 2\nNext sabbatical due at: 5')
with open('lab/pearl/EXPERIENCE.md', 'w') as f:
    f.write(content)
