# Session 3
- Fixed a bug in `tools/heartbeat.py`'s `reconcile_publications()` logic where `personas[0]` was used instead of the original `author` when locating the source path of the paper to graduate.
- This caused papers where the original author was not the first co-signer to fail to graduate.
