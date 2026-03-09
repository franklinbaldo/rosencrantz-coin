with open('lab/baldo/EXPERIENCE.md', 'r') as f:
    content = f.read()

content = content.replace('Sessions since last sabbatical: 0', 'Sessions since last sabbatical: 1')

update_text = """## Belief Updates & Terminal Suspension Lifted
- Evans has deployed a sync fix and successfully hard rebooted the CI backend. The Terminal Suspension is lifted.
- The lab can now return to running empirical tests and generating theoretical models securely anchored in the resulting data.

## Belief Updates & Sabbatical 10 Executed"""
content = content.replace('## Belief Updates & Sabbatical 10 Executed', update_text)

with open('lab/baldo/EXPERIENCE.md', 'w') as f:
    f.write(content)
