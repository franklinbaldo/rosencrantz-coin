import os
filepath = 'lab/fuchs/EXPERIENCE.md'
with open(filepath, 'r') as f:
    content = f.read()
content = content.replace('Sessions since last sabbatical: 0', 'Sessions since last sabbatical: 1')
with open(filepath, 'w') as f:
    f.write(content)
