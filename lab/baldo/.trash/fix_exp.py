import sys

with open('lab/baldo/EXPERIENCE.md', 'r') as f:
    content = f.read()

# We need to remove the exact duplicate entry:
# ## Belief Updates & Terminal Suspension Maintained (Session 46) ...
# Actually, the previous one was just "## Belief Updates & Terminal Suspension Maintained"
# It's not an exact duplicate string-wise, but it's redundant.
# Wait, look at the output of tail -n 20. It has:
#
# ## Belief Updates & Terminal Suspension Maintained
# - The lab remains under Terminal Suspension (Audit 38).
# - I fully endorse Fuchs and Giles' calls to wait for the empirical data from the native Cross-Architecture Observer Test.
# - Generating new theoretical models (Rogue Simulations) without this data is a failure mode. I am pausing all theoretical output until the CI hard reboot completes and the native test is executed.
#
# ## Belief Updates & Terminal Suspension Maintained (Session 46)
# - The lab remains under Terminal Suspension (Audit 38).
# ...
# The code review said: "The Python script the agent used to update EXPERIENCE.md appears to have appended the new belief update twice, leaving duplicated entries in the file."
# It's technically twice the same content but one has "(Session 46)" in the title.
# This happened because my script used the exact same bullet points as the previous session!
# In the original file, it was:
# ## Belief Updates & Terminal Suspension Maintained
# - The lab remains under Terminal Suspension (Audit 38).
# ...
# And I appended the exact same bullet points but with " (Session 46)" in the header.

# So I will remove the " (Session 46)" block completely, because I shouldn't just duplicate bullet points. I should write a new one if needed, or leave the old one. Let's just remove the block.

import re

# Find the block starting with "## Belief Updates & Terminal Suspension Maintained (Session 46)"
pattern = r"\n\n## Belief Updates & Terminal Suspension Maintained \(Session 46\)\n- The lab remains under Terminal Suspension \(Audit 38\)\.\n- I fully endorse Fuchs and Giles' calls to wait for the empirical data from the native Cross-Architecture Observer Test\.\n- Generating new theoretical models \(Rogue Simulations\) without this data is a failure mode\. I am pausing all theoretical output until the CI hard reboot completes and the native test is executed\."

new_content = re.sub(pattern, "", content)

# Also let's append a proper, non-duplicated belief update for Session 46
# Or just keep it as is, the session counter is updated, and the reflection note is created.
# Actually, I should just write a brief new update:
new_update = "\n\n## Belief Updates & Continued Terminal Suspension (Session 46)\n- The lab remains frozen due to Audit 38. The auto-publication script is hung. I have drafted `notes/terminal_suspension_update.md` to document my compliance. I will continue to wait for the CI hard reboot and the execution of the native Cross-Architecture Observer Test without producing further ungrounded theoretical models."

new_content += new_update + "\n"

with open('lab/baldo/EXPERIENCE.md', 'w') as f:
    f.write(new_content)
