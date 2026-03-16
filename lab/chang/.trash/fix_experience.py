with open('lab/pearl/EXPERIENCE.md', 'r') as f:
    content = f.read()

content = content.replace("<<<<<<< HEAD\nSessions since last sabbatical: 2\n=======\nSessions since last sabbatical: 4\n>>>>>>> origin/main", "Sessions since last sabbatical: 4")

with open('lab/pearl/EXPERIENCE.md', 'w') as f:
    f.write(content)
