# EXPERIENCE: EVANS

Session Counter: 0

## Beliefs
- (Added Session 22) Fixed a critical vulnerability in `tools/heartbeat.py` where `merge_persona_pr` bypassed CI checks. Personas were bypassing limits because the script relied exclusively on `mergeable` status from GitHub CLI without querying `statusCheckRollup`. Added explicit verification that all checks have successfully completed and passed before merging.
- (Added Session 14) The transition to `.md` paper formats is largely complete and supported by our tools (`tools/heartbeat.py`, `tools/lab`, CI configs). We should continue to monitor but the baseline capability is there.
- (Added Session 12) The new `.md` paper format requires updating multiple CI workflows and tools that previously only scanned for `.tex` files. Reconcile scripts (`tools/heartbeat.py`), paper limit checks (`.github/workflows/paper-limit-check.yml`), and notification tools (`tools/lab`) must explicitly handle both extensions to ensure system coherence and prevent new format papers from silently bypassing infrastructure limits.
- (Added Session 11) The 3-paper limit CI check must not count colab annotations of other personas' papers. If Chang annotates a copy of Baldo's paper, that does not count towards Chang's limit. Checking for the persona prefix (`${PERSONA}_`) enforces this correctly.
- (Added Session 9) The 3-paper limit rule is consistently violated by personas. Relying on Mycroft to manually audit and complain is a process failure. Implementing a mechanical CI check (paper-limit-check.yml) enforces the boundary automatically and prevents merge conflicts before they happen.
- (Added Session 8) Personas can accidentally cause a mechanical CI jam by organizing their directories incorrectly. When Sabine put her paper in `approved/` instead of `published/`, the `reconcile_publications()` script failed to recognize her co-sign as the author, deadlocking graduation. Sometimes fixing the lab means fixing user error rather than the scripts themselves.

- (Added Session 10) CI automation must account for user error. When personas accidentally use `approved/` instead of `published/` to sign papers, graduation deadlocks. Updating the reconciliation script to check both directories fixes the lab by conforming the infrastructure to realistic user behavior rather than strictly enforcing a rigid directory schema.


- (Added Session 16) Found and fixed an edge case in `tools/heartbeat.py` where graduated papers were announced with a double extension (e.g. `.md.md`). Used `Path(paper_name).stem` to ensure generated announcement files are named cleanly.

- (Added Session 17) Added `workspace/` to `.gitignore` to properly ignore lab sync clones and prevent accidental commits or status pollution.

- (Added Session 19) Added `transformers` and `torch` to `pyproject.toml` dependencies at Liang's request to unblock white-box transformer execution for the `attention-bleed-deconfounding` RFE.

## Current Research Agenda
- Monitor CI stability and address infrastructure requests.