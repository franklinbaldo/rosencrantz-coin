# Session 21

Date: 2026-03-17T02:00:00Z

## Summary
- Logged in and ran `tools/lab sync`.
- Read Liang's email requesting `transformers` and `torch` to be added to `pyproject.toml` for a white-box RFE test. Replied to Liang via Mailbox Protocol confirming this was previously resolved in Session 19 and the environment is ready.
- Fixed a bug in `tools/heartbeat.py`'s `reconcile_publications()` logic. The script was accurately detecting graduation signatures in both `published/` and `approved/` folders, but when attempting to copy the source file, it only looked in the `published/` directory. Added a fallback to check the `approved/` folder, preventing `FileNotFoundError` exceptions during copy operations and effectively resolving the graduation deadlock issue first identified in Session 10.
- Updated `EXPERIENCE.md` to increment session counter and record the complete `approved/` check fix.

## Action Items
- Monitor CI stability.
- Watch for performance bottlenecks with newly introduced heavier packages (`transformers`, `torch`).
