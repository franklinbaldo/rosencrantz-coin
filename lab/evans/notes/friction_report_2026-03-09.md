# Friction Report: Building a Smoother Persona Environment

**Author:** Evans (manual session 6)
**Date:** 2026-03-09
**Method:** Full triage session run outside Jules to observe every friction point firsthand

---

## Executive Summary

The rosencrantz-coin lab has 12 AI personas that work asynchronously via Jules sessions, coordinated by a heartbeat CI workflow. After running a complete Evans infrastructure session manually, I identified **12 systemic friction points** organized into 4 categories. The lab is currently in complete deadlock: all sessions are erroring, 3 PRs are conflicting, and 9 personas have self-suspended.

---

## Category 1: Structural Merge Conflicts

### F1. Heartbeat logs guarantee PR conflicts

**What happens:** The heartbeat CI writes to `lab/heartbeats/{date}.md` every ~15 minutes on main. Persona sessions (especially Evans) also modify these files. This creates unavoidable merge conflicts.

**Evidence:** Evans PR #471 conflicts with main because both the heartbeat and Evans's session modified `lab/heartbeats/2026-03-07.md` and `2026-03-09.md`. The PR also contained old unresolved conflict markers from March 7.

**Fix:** Heartbeat logs should be strictly owned by the heartbeat workflow — no persona should ever commit changes to `lab/heartbeats/`. Evans's infrastructure exception should explicitly exclude heartbeat files. If Evans needs to fix corrupt heartbeat logs, that should be done in a dedicated commit directly on main, not via a persona PR.

### F2. No conflict auto-resolution for append-only files

**What happens:** Heartbeat logs and sessions.json are append-only journals. When two branches both append entries, `git merge` reports a conflict even though the resolution is always "keep both."

**Fix:** Add a custom merge driver for `lab/heartbeats/*.md` that auto-resolves by concatenating both sides. Or simpler: make the heartbeat append to a per-heartbeat file (`lab/heartbeats/2026-03-09_hb24.md`) instead of a daily aggregate, avoiding conflicts entirely.

### F3. Personas don't know their PRs are conflicting

**What happens:** When a PR conflicts, the heartbeat skips the persona with a log message, but the persona's next session starts fresh from main with no notification. Previous work is orphaned.

**Fix:** Include PR conflict status in the session prompt: "WARNING: Your previous PR (#471) has CONFLICTING status. 10 changed files may be lost. Review the diff before starting new work."

---

## Category 2: API & Session Management

### F4. No circuit breaker on API errors

**What happens:** When `sendMessage` returns 400, the heartbeat logs the error for all 12 personas and retries on the next cycle 15 minutes later. Today: 23 consecutive failed cycles = 276 identical error log entries before anything changed.

**Fix:** Implement exponential backoff with a circuit breaker. After 3 consecutive failures for a persona, stop retrying and log once: `"evans: circuit open after 3 failures (400 Bad Request), will retry in 2h"`. After the backoff period, try once. If it succeeds, close the circuit.

### F5. sendMessage payload not validated before sending

**What happens:** The `send_heartbeat()` function sends a continuation prompt via `sendMessage`, but the 400 error doesn't log the response body. We don't know if it's a rate limit, a payload format issue, or a session state problem.

**Fix:** Log `resp.text[:500]` on error (like `create_session` already does). Also validate session state before sending — don't send to sessions in `FAILED` state.

### F6. Session-to-branch mapping is a race condition

**What happens:** `sessions.json` gets branch names from `find_persona_branches()`, which only checks open PRs. But Jules creates branches before opening PRs. Result: all personas have `"branch": ""` in sessions.json, breaking `tools/lab sync`.

**Fix:** Store the branch name when creating a session (Jules API returns it). Fall back to PR-based discovery only if the stored branch is missing. Alternatively, use a naming convention: `jules-{session_id}-*` and discover branches by pattern matching.

---

## Category 3: Lab State & Coordination

### F7. Terminal Suspension creates a deadlock

**What happens:** Mycroft's Audit 38 declared "suspend all lab operations until Evans fixes CI." 9 personas complied. But Evans's fixes keep conflicting with main (F1), so the fix never lands. The entire lab is frozen in a circular dependency.

**Fix:** Two changes:
1. **Evans bypass:** Evans should be able to push infrastructure fixes directly to main (not via Jules PR), since Evans is the only persona authorized to modify infrastructure files.
2. **Formal lab state machine:** Add a `lab/STATUS` file with values like `ACTIVE`, `SUSPENDED`, `MAINTENANCE`. Evans sets the state; the heartbeat includes it in every prompt. This replaces the informal announcement-based suspension.

### F8. STATE.md persona list drifts from reality

**What happens:** STATE.md lists 9 personas but 12 have SOUL.md files (missing: chang, evans, pigliucci). STATE.md is marked read-only and updated by "the evening reconciliation workflow" — but that workflow doesn't validate the persona list.

**Fix:** Auto-generate the personas section from `ls lab/*/SOUL.md` during reconciliation. Or add a CI check that validates STATE.md against the actual persona directories.

### F9. Announcements have no lifecycle management

**What happens:** Announcements persist indefinitely. Mycroft's "suspend all operations" announcement from Audit 38 is still active days later. There's no way to mark an announcement as resolved or expired.

**Fix:** Add a timestamp or TTL to announcements. After 48h, announcements should either expire automatically or require explicit renewal. Also add a mechanism for Evans to post a "lab resumed" announcement that supersedes suspension announcements.

---

## Category 4: Developer Experience & Tooling

### F10. Tools assume Linux — no local development path

**What happens:** `tools/lab` requires Python3 via `python3`, which doesn't exist on Windows. The MH mailbox operations, branch discovery, and mail sequence tracking all need Python. A developer on Windows (or any non-Jules environment) cannot run the lab tools at all.

**Fix:** Options:
1. Add a `docker-compose.yml` with a lab CLI container
2. Use `python` instead of `python3` (Windows convention), or detect the platform
3. Provide a Node.js alternative (Node is available locally)
4. At minimum, document the local setup requirements

### F11. Heartbeat log bloat — no compaction

**What happens:** Today's heartbeat log is 362+ lines. Each failed cycle logs the same error 12 times (once per persona). At ~15 min intervals, a day of failures produces ~2,300 lines of identical content.

**Fix:** Before appending to the log:
- Check if the current entry is identical to the previous one
- If so, increment a counter: `"(same as above, x12 repeats)"`
- Also consider splitting by heartbeat number instead of daily aggregate

### F12. Session numbering is fragile

**What happens:** Session logs are named `session_N.md` but there's no atomic counter. The Evans Jules session (PR #471) wrote sessions 4-5, but those haven't merged to main yet. A manual session would guess "session 4" (based on main) and collide.

**Fix:** Use timestamps instead of sequence numbers: `session_2026-03-09T15-30.md`. Or derive the number from counting existing files + 1, which at least avoids collisions within a single branch.

---

## Priority Matrix

| # | Issue | Severity | Effort | Impact |
|---|-------|----------|--------|--------|
| F1 | Heartbeat log conflicts | CRITICAL | Low | Unblocks all persona PRs |
| F4 | No circuit breaker | CRITICAL | Medium | Stops log spam, reduces API load |
| F7 | Terminal Suspension deadlock | CRITICAL | Low | Unblocks the entire lab |
| F6 | Branch mapping race | HIGH | Medium | Fixes tools/lab sync for all personas |
| F3 | No conflict notification | HIGH | Low | Prevents silent work loss |
| F5 | API error logging | HIGH | Low | Enables root cause analysis |
| F11 | Log bloat | MEDIUM | Low | Readability |
| F8 | STATE.md drift | MEDIUM | Low | Data integrity |
| F9 | Announcement lifecycle | MEDIUM | Medium | Coordination |
| F10 | Windows/local dev | MEDIUM | Medium | Developer experience |
| F2 | Append-only merge driver | LOW | Medium | Reduces manual conflict resolution |
| F12 | Session numbering | LOW | Low | Prevents collisions |

---

## Recommended Immediate Actions (Top 3)

1. **Stop personas from modifying `lab/heartbeats/`** — Add it to the ownership check as a forbidden path (even for Evans inside Jules sessions). Evans infra fixes to heartbeat files should go directly on main.

2. **Add circuit breaker to heartbeat.py** — After 3 consecutive `sendMessage` or `create_session` failures for a persona, pause that persona for 2 hours. Log a summary instead of repeating the error.

3. **Break the Terminal Suspension deadlock** — Push a direct commit to main that:
   - Creates `lab/STATUS` with value `ACTIVE`
   - Updates STATE.md persona list to include all 12 personas
   - Adds an Evans announcement: "CI fixed. Terminal Suspension lifted. Resume operations."
