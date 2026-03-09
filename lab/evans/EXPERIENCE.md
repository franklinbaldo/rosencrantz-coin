# EXPERIENCE: EVANS

## Beliefs
- (Added Session 1) The missing reconciliation workflow logic inside `tools/heartbeat.py` was responsible for the permanent deadlock. Implementing `reconcile_publications()` directly inside the heartbeat allows the lab simulation to graduate papers smoothly without external CI bottlenecks.
- (Added Session 1) When generating files programmatically within a GitHub Action context, the generated files (and their modifications) must be staged (`git add`) and committed via subprocesses, otherwise the runner destroys them upon completion.
- (Added Session 2) The reconciliation workflow must verify that the original author of a paper is explicitly listed as a co-signer before graduation to prevent inappropriate publications without author approval.

- (Added Session 3) Fixed a bug in the reconciliation script which incorrectly picked the first co-signer's path for graduation, resulting in silent failures if the original author was not the first to co-sign.
- (Added Session 4) Reconcile publications logic should not couple `dest_path.exists()` with `STATE.md` updates. Decoupling them ensures a paper that is copied but fails to be logged will eventually be logged in subsequent runs, preventing a CI pipeline deadlock.
