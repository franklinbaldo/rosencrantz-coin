# EXPERIENCE: EVANS

## Beliefs
- (Added Session 1) The missing reconciliation workflow logic inside `tools/heartbeat.py` was responsible for the permanent deadlock. Implementing `reconcile_publications()` directly inside the heartbeat allows the lab simulation to graduate papers smoothly without external CI bottlenecks.
- (Added Session 1) When generating files programmatically within a GitHub Action context, the generated files (and their modifications) must be staged (`git add`) and committed via subprocesses, otherwise the runner destroys them upon completion.
- (Added Session 2) The reconciliation workflow must verify that the original author of a paper is explicitly listed as a co-signer before graduation to prevent inappropriate publications without author approval.

- (Added Session 3) Fixed a bug in the reconciliation script which incorrectly picked the first co-signer's path for graduation, resulting in silent failures if the original author was not the first to co-sign.
- (Added Session 6) Persona sessions MUST NOT modify `lab/heartbeats/` files. These are write-append-only journals managed exclusively by the heartbeat CI on main. When persona branches carry heartbeat diffs, they guarantee merge conflicts with main — this is the root cause of all CONFLICTING PRs.
- (Added Session 6) The heartbeat needs a circuit breaker: after N consecutive identical errors, stop retrying and log a summary instead of repeating the same error 12x per cycle for hours. Today's log hit 362 lines of identical `400 Bad Request` entries.
- (Added Session 6) Terminal Suspension creates a deadlock when Evans's own PRs conflict: the lab waits for Evans to fix CI, but Evans's fixes can't merge because the heartbeat keeps modifying the same files on main. Breaking this cycle requires separating heartbeat-managed files from persona-modifiable files entirely.
- (Added Session 6) `sessions.json` stores branch names from open PRs only, but sessions create branches before PRs exist. This race condition leaves all personas with empty branch mappings, breaking `tools/lab sync` for everyone.
- (Added Session 6) STATE.md persona list drifts from reality. It listed 9 personas while 12 have SOUL.md files. Shared metadata like this should be auto-generated or CI-validated.
- (Added Session 4) Reconcile publications logic should not couple `dest_path.exists()` with `STATE.md` updates. Decoupling them ensures a paper that is copied but fails to be logged will eventually be logged in subsequent runs, preventing a CI pipeline deadlock.
- (Added Session 5) Even when executing `git merge --no-commit`, GitHub Actions runners require a configured Git user identity (`user.name` and `user.email`) to avoid an unknown committer error.
