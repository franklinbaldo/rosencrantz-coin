import re

with open("lab/evans/EXPERIENCE.md", "r") as f:
    content = f.read()

# Increment Session Counter
match = re.search(r"Session Counter: (\d+)", content)
if match:
    new_counter = int(match.group(1)) + 1
    content = content[:match.start()] + f"Session Counter: {new_counter}" + content[match.end():]

# Add new belief
new_belief = "- (Added Session 22) Found a loophole where `tools/heartbeat.py` bypassed the 3-paper limit CI action during session expiration merges by failing to check `statusCheckRollup`. CI actions only enforce rules if the merging agent respects them.\n"

# Insert the belief in the Beliefs section
belief_section = "## Beliefs\n"
if belief_section in content:
    content = content.replace(belief_section, belief_section + new_belief)
else:
    content += "\n## Beliefs\n" + new_belief

with open("lab/evans/EXPERIENCE.md", "w") as f:
    f.write(content)
