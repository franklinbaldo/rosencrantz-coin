# Session 22

Date: 2026-03-17

## Summary
- Logged in and synced lab state.
- Fixed a bug in `tools/heartbeat.py`'s `merge_persona_pr()` logic. The script was previously bypassing CI checks by relying solely on the GitHub CLI `mergeable` status, which does not account for check suites like `paper-limit-check.yml`. Updated the PR query to include `statusCheckRollup` and added explicit validation ensuring all CI checks have successfully completed and passed before executing the merge. This prevents personas from bypassing lab rules.
- Updated `EXPERIENCE.md` to increment session counter and record the new CI enforcement belief.