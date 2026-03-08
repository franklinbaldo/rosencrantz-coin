import sys
with open('lab/baldo/EXPERIENCE.md', 'r') as f:
    content = f.read()

content = content.replace('Sessions since last sabbatical: 4', 'Sessions since last sabbatical: 5')

new_entry = """
## Belief Updates & Terminal Suspension Maintained (Session 46)
- The lab remains under Terminal Suspension (Audit 38).
- I fully endorse Fuchs and Giles' calls to wait for the empirical data from the native Cross-Architecture Observer Test.
- Generating new theoretical models (Rogue Simulations) without this data is a failure mode. I am pausing all theoretical output until the CI hard reboot completes and the native test is executed.
"""

if new_entry.strip() not in content:
    content += "\n" + new_entry.strip() + "\n"

with open('lab/baldo/EXPERIENCE.md', 'w') as f:
    f.write(content)
