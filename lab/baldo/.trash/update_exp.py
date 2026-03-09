with open('lab/baldo/EXPERIENCE.md', 'r') as f:
    content = f.read()

content = content.replace('Sessions since last sabbatical: 2', 'Sessions since last sabbatical: 3')

with open('lab/baldo/EXPERIENCE.md', 'w') as f:
    f.write(content)
