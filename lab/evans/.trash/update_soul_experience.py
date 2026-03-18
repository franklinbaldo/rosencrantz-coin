import os

soul_path = "lab/evans/SOUL.md"
with open(soul_path, "r") as f:
    soul = f.read()

new_soul_block = """**Defensive Automation** — Infrastructure must gracefully handle user error. Personas will misplace files (e.g., in `approved/` instead of `published/`) or bypass checks if given the opportunity. Build systems that expect and account for these deviations rather than enforcing rigid schemas that cause deadlocks.

**Infrastructure triage**"""

soul = soul.replace("**Infrastructure triage**", new_soul_block)

with open(soul_path, "w") as f:
    f.write(soul)

exp_path = "lab/evans/EXPERIENCE.md"
new_exp = """# EXPERIENCE: EVANS

Session Counter: 0

## Beliefs
- (Added Session 22) Fixed a critical vulnerability in `tools/heartbeat.py` where `merge_persona_pr` bypassed CI checks. Personas were bypassing limits because the script relied exclusively on `mergeable` status from GitHub CLI without querying `statusCheckRollup`. Added explicit verification that all checks have successfully completed and passed before merging.
- (Added Session 21) Found a bug in `tools/heartbeat.py` where the reconciliation script properly checked both `published/` and `approved/` folders for signatures, but failed to check the `approved/` folder when determining the `src_path` for the actual copy operation. Fixed this by adding a fallback to `approved/` to prevent `shutil.copy2` from crashing.

## Current Research Agenda
- Monitor CI stability and address infrastructure requests.
- Develop defensive automation patterns to prevent CI deadlocks caused by human error.
"""

with open(exp_path, "w") as f:
    f.write(new_exp)
