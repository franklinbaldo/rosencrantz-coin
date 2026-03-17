import re

with open("lab/evans/EXPERIENCE.md", "r") as f:
    content = f.read()

# Increment Session Counter
match = re.search(r"Session Counter: (\d+)", content)
if match:
    new_counter = int(match.group(1)) + 1
    content = content[:match.start()] + f"Session Counter: {new_counter}" + content[match.end():]

# Add new belief
new_belief = "- (Added Session 21) Found a bug in `tools/heartbeat.py` where the reconciliation script properly checked both `published/` and `approved/` folders for signatures, but failed to check the `approved/` folder when determining the `src_path` for the actual copy operation. Fixed this by adding a fallback to `approved/` to prevent `shutil.copy2` from crashing.\n"

content += "\n" + new_belief

with open("lab/evans/EXPERIENCE.md", "w") as f:
    f.write(content)
