import os
import re
filepath = 'lab/fuchs/EXPERIENCE.md'
with open(filepath, 'r') as f:
    content = f.read()
content = re.sub(r'1\. \*\*Measurement-Fragment Isomorphism\*\*:.*?\n', '', content)
content = re.sub(r'Sessions since last sabbatical: \d+', 'Sessions since last sabbatical: 0', content)
with open(filepath, 'w') as f:
    f.write(content)
