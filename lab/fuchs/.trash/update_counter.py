import os
filepath = 'lab/fuchs/EXPERIENCE.md'
with open(filepath, 'r') as f:
    content = f.read()
content = content.replace('Sessions since last sabbatical: 3', 'Sessions since last sabbatical: 4')
with open(filepath, 'w') as f:
    f.write(content)
