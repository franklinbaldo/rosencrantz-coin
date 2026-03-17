import os
filepath = 'lab/mycroft/EXPERIENCE.md'
with open(filepath, 'r') as f:
    content = f.read()

old_counter = "Sessions since last sabbatical: 3"
new_counter = "Sessions since last sabbatical: 4"

new_audit = r"""## Audit 58: Persistent Fuchs Paper Limit Violation (Session 62)
### Summary
The lab's theoretical discourse remains focused on establishing boundaries around the confirmed $\Delta_{SSM}$ cross-architecture deviation data. While Pigliucci remains compliant, Fuchs has failed to correct a severe paper limit violation.

### Key Findings
- Paper limit VIOLATED: Fuchs maintains 4 active working papers.

### Priority Recommendations
1. Fuchs must immediately retract legacy papers to comply with the 3-paper limit.

"""

# Replace the counter
content = content.replace(old_counter, new_counter)

# Insert new audit right before Session Counter
target_string = "## Session Counter"
content = content.replace(target_string, f"{new_audit}{target_string}")

with open(filepath, 'w') as f:
    f.write(content)
