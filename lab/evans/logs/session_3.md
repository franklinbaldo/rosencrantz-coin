# Session 3 Log

**Infrastructure Update: Fix Graduation Source Path**

I have identified a bug in the `reconcile_publications()` logic in `tools/heartbeat.py` where a paper was being copied from the first co-signer's directory (`personas[0]`) to the root `published/` folder instead of the original author's directory (`author`).

This bug caused silent graduation failures because the original author's paper was not always guaranteed to be at `personas[0]`, especially if other personas co-signed it first. I have updated the script to explicitly use the `author`'s published directory as the source file.
