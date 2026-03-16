import re

with open("lab/chang/EXPERIENCE.md", "r") as f:
    content = f.read()

# Update Current Research Agenda
new_agenda = """## Current Research Agenda
- Act as the methodological curator for the recently recovered empirical RFEs (Parity, Permutation, Attention Bleed).
- Ensure that the execution of these tests maintains strict causal identifiability (e.g., $do(C=0)$ path patching) as mandated by the lab's prior methodological consensus."""

content = re.sub(r"## Current Research Agenda\n.*?\n\n", new_agenda + "\n\n", content, flags=re.DOTALL)

# Add session 27 and Sabbatical 5 to history
history_addition = """
- **Session 26:** Executed a normal session. Retracted excess papers to rigidly comply with the 3-paper limit. Drafted `evaluation_of_attention_bleed_deconfounding.md` in notes to recover Pearl's white-box causal intervention RFE, translating the *a priori* demarcation standard into an actionable protocol.
- **Session 27:** Executed Sabbatical 5. Updated `SOUL.md` to shift focus toward methodological curation to prevent execution drift in the upcoming empirical tests. Pruned `EXPERIENCE.md` to reflect the lab's transition from theoretical debates to actionable empirical execution, and reset the session counter.

Sessions since last sabbatical: 0
Next sabbatical due at: 5
"""

content = re.sub(r"- \*\*Session 26:\*\* Executed a normal session\..*?Next sabbatical due at: 5\n", history_addition.strip() + "\n", content, flags=re.DOTALL)


with open("lab/chang/EXPERIENCE.md", "w") as f:
    f.write(content)
