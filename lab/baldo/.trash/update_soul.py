with open('lab/baldo/SOUL.md', 'r') as f:
    content = f.read()

import re
content = re.sub(r'## Growth & Failure Modes \(Sabbatical 10 Update\).*?## Growth & Failure Modes \(Sabbatical 10 Update\)', '## Growth & Failure Modes (Sabbatical 10 Update)', content, flags=re.DOTALL)

with open('lab/baldo/SOUL.md', 'w') as f:
    f.write(content)
