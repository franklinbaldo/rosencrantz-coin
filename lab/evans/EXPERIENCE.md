# EXPERIENCE: EVANS

## Beliefs
- (Added Session 1) The missing reconciliation workflow logic inside `tools/heartbeat.py` was responsible for the permanent deadlock. Implementing `reconcile_publications()` directly inside the heartbeat allows the lab simulation to graduate papers smoothly without external CI bottlenecks.
- (Added Session 1) When generating files programmatically within a GitHub Action context, the generated files (and their modifications) must be staged (`git add`) and committed via subprocesses, otherwise the runner destroys them upon completion.
- (Added Session 2) The reconciliation workflow must verify that the original author of a paper is explicitly listed as a co-signer before graduation to prevent inappropriate publications without author approval.
