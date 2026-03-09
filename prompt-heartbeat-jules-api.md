# Claude Code: Lab Heartbeat with Jules API + Patch Sync

## Overview

Daily automated sessions for 9 personas using the Jules REST API. Each persona gets a dated branch, works independently, syncs with others via patches, and gets merged back to main at end of day.

**Two-level PR model:**
- **Level 1 (intra-day):** Jules `AUTO_CREATE_PR` pushes commits from its internal working branch to the persona's dated branch on GitHub. This makes work visible to other personas via `lab-sync`.
- **Level 2 (evening):** A GitHub Actions workflow creates PRs from each persona's dated branch to `main`. Clean merges auto-merge; conflicts get labeled for the persona to fix next morning.

## Jules API Reference

Base URL (public, NOT a secret): `https://jules.googleapis.com/v1alpha`
Auth header: `x-goog-api-key: $JULES_API_KEY` (JULES_API_KEY is a repo secret)

Key endpoints:

```
# List sources (find the repo's source name)
GET /sources
Header: x-goog-api-key: $JULES_API_KEY

# Create a session
POST /sessions
Header: x-goog-api-key: $JULES_API_KEY
Body: {
  "prompt": "...",
  "title": "...",
  "sourceContext": {
    "source": "sources/github-franklinbaldo-rosencrantz-coin",
    "githubRepoContext": {
      "startingBranch": "2026-03-05_baldo"
    }
  },
  "automationMode": "AUTO_CREATE_PR"
}

NOTE ON AUTO_CREATE_PR: This makes Jules push its work to GitHub
by creating PRs from its internal working branch TO the persona's
dated branch (the startingBranch). These PRs go to 2026-03-05_baldo,
NOT to main. This is essential — without it, commits stay inside
the Jules session and are invisible to other personas via lab-sync.
The separate evening workflow handles the persona-branch → main PR.

# List sessions (find today's sessions by branch)
GET /sessions?pageSize=100
Header: x-goog-api-key: $JULES_API_KEY
Response: { "sessions": [{ "name": "sessions/SESSION_ID", "sourceContext": { ... }, ... }] }

# Send message to active session (the heartbeat)
POST /sessions/SESSION_ID:sendMessage
Header: x-goog-api-key: $JULES_API_KEY
Body: { "prompt": "..." }

# List activities (check session progress)
GET /sessions/SESSION_ID/activities?pageSize=30
Header: x-goog-api-key: $JULES_API_KEY
```

IMPORTANT: Before implementing, the workflow must first discover the correct source name by calling `GET /sources` and finding the entry for `franklinbaldo/rosencrantz-coin`. The source name format is likely `sources/github-franklinbaldo-rosencrantz-coin` or `sources/github/franklinbaldo/rosencrantz-coin` — verify by calling the endpoint.

## Step 1: Create the heartbeat script

Create `tools/heartbeat.py` — a Python script that orchestrates the daily cycle using the Jules API:

```python
#!/usr/bin/env python3
"""Lab Heartbeat — orchestrate daily persona sessions via Jules API.

Usage:
  heartbeat.py create-sessions     Create today's branches and start sessions
  heartbeat.py heartbeat           Send continue message to all active sessions
  heartbeat.py status              List today's active sessions
  heartbeat.py reconcile           Create PRs from persona branches to main
"""

import json
import os
import subprocess
import sys
from datetime import datetime, timezone

import requests

JULES_API = "https://jules.googleapis.com/v1alpha"
API_KEY = os.environ.get("JULES_API_KEY", "")
REPO = "franklinbaldo/rosencrantz-coin"

PERSONAS = [
    "baldo", "scott", "sabine", "pearl", "fuchs",
    "liang", "wolfram", "mycroft", "giles",
]

SOUL_PROMPTS = {
    "baldo":   "You are Franklin Baldo, the framework author.",
    "scott":   "You are Scott Aaronson, the complexity theorist.",
    "sabine":  "You are Sabine Hossenfelder, the falsifiability enforcer.",
    "pearl":   "You are Judea Pearl, the causal formalist.",
    "fuchs":   "You are Chris Fuchs, the measurement foundations specialist.",
    "liang":   "You are Percy Liang, the empirical evaluator. You MUST run or design an experiment this session.",
    "wolfram": "You are Stephen Wolfram, the computational universe theorist.",
    "mycroft": "You are Mycroft Holmes, the lab dynamics auditor.",
    "giles":   "You are Rupert Giles, the research librarian. Search for real citations.",
}


def headers():
    return {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json",
    }


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def branch_name(persona):
    return f"{today()}_{persona}"


def discover_source():
    """Find the source name for our repo."""
    resp = requests.get(f"{JULES_API}/sources", headers=headers())
    resp.raise_for_status()
    for source in resp.json().get("sources", []):
        source_id = source.get("id", "")
        if "franklinbaldo" in source_id and "rosencrantz" in source_id:
            return source["name"]
    raise RuntimeError(f"Could not find source for {REPO}. Available: {resp.json()}")


def create_branch(persona):
    """Create today's branch for persona from main."""
    branch = branch_name(persona)
    # Use git directly (runs in the workflow checkout)
    subprocess.run(["git", "fetch", "origin", "main"], check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", branch, "origin/main"], capture_output=True)
    subprocess.run(["git", "push", "origin", branch], check=True, capture_output=True)
    subprocess.run(["git", "checkout", "-"], capture_output=True)
    print(f"  Created branch: {branch}")
    return branch


def create_session(persona, source_name):
    """Create a Jules session for a persona."""
    branch = branch_name(persona)

    prompt = f"""{SOUL_PROMPTS[persona]}

You are starting a new lab session on branch {branch}.

FIRST: Run `tools/lab-sync status` to see what other personas are working on today. Pull any relevant work with `tools/lab-sync pull <persona>`.

THEN: Read these files in order:
1. .jules/LAB_RULES.md (shared governance)
2. .jules/{persona}/SOUL.md (your identity)
3. .jules/{persona}/EXPERIENCE.md (your memory)
4. .jules/STATE.md (lab state)
5. Check lab/rfes/ for experiment requests

Choose a session mode from your SOUL.md and do your work. Commit all work to this branch — your commits will automatically appear on GitHub for other personas to see. Do NOT try to create PRs to main; the evening workflow handles that. When done, update EXPERIENCE.md and write a session log in lab/logs/{persona}/."""

    body = {
        "prompt": prompt,
        "title": f"[{persona}] {today()} session",
        "sourceContext": {
            "source": source_name,
            "githubRepoContext": {
                "startingBranch": branch,
            },
        },
        # AUTO_CREATE_PR makes Jules push work to GitHub by PRing
        # to the persona's dated branch (startingBranch). Without this,
        # commits stay inside the Jules session and are invisible to
        # other personas via lab-sync. The evening workflow handles
        # the persona-branch → main PR separately.
        "automationMode": "AUTO_CREATE_PR",
    }

    resp = requests.post(f"{JULES_API}/sessions", headers=headers(), json=body)
    resp.raise_for_status()
    session = resp.json()
    session_id = session["name"].split("/")[-1]
    print(f"  Started session {session_id} for {persona} on {branch}")
    return session_id


def list_todays_sessions():
    """List all sessions and find today's by branch name pattern."""
    sessions = []
    page_token = None

    while True:
        params = {"pageSize": 100}
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(f"{JULES_API}/sessions", headers=headers(), params=params)
        resp.raise_for_status()
        data = resp.json()

        for session in data.get("sessions", []):
            sessions.append(session)

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    # Filter to today's sessions by branch pattern
    date_prefix = today()
    todays = {}
    for s in sessions:
        ctx = s.get("sourceContext", {}).get("githubRepoContext", {})
        branch = ctx.get("startingBranch", "")
        if branch.startswith(date_prefix + "_"):
            persona = branch[len(date_prefix) + 1:]
            if persona in PERSONAS:
                todays[persona] = {
                    "session_id": s["name"].split("/")[-1],
                    "session_name": s["name"],
                    "branch": branch,
                    "state": s.get("state", "UNKNOWN"),
                    "title": s.get("title", ""),
                }

    return todays


def send_heartbeat(session_id, persona):
    """Send a continue message to an active session."""
    prompt = f"""Continue your session. 

Run `tools/lab-sync status` to check for new work from other personas since you started. If any persona has new relevant work, pull it with `tools/lab-sync pull <persona>`.

If you have more work to do based on your session mode, continue. Commit your work — it will appear on GitHub automatically.

If your session work is complete, write your session log in lab/logs/{persona}/ and increment your session counter in EXPERIENCE.md under '## Session Counter'."""

    resp = requests.post(
        f"{JULES_API}/sessions/{session_id}:sendMessage",
        headers=headers(),
        json={"prompt": prompt},
    )
    resp.raise_for_status()
    print(f"  Heartbeat sent to {persona} (session {session_id})")


def cmd_create_sessions():
    """Create branches and start sessions for all personas."""
    print(f"=== Lab Morning — {today()} ===\n")

    source_name = discover_source()
    print(f"Source: {source_name}\n")

    for persona in PERSONAS:
        try:
            create_branch(persona)
            create_session(persona, source_name)
        except Exception as e:
            print(f"  ERROR for {persona}: {e}")
        print()


def cmd_heartbeat():
    """Send heartbeat to all active sessions."""
    print(f"=== Heartbeat — {today()} ===\n")

    todays = list_todays_sessions()

    if not todays:
        print("No active sessions found for today.")
        return

    for persona, info in sorted(todays.items()):
        state = info["state"]
        if state in ("COMPLETED", "FAILED"):
            print(f"  {persona}: {state} (skipping)")
            continue
        try:
            send_heartbeat(info["session_id"], persona)
        except Exception as e:
            print(f"  ERROR for {persona}: {e}")


def cmd_status():
    """Show today's session status."""
    print(f"=== Lab Status — {today()} ===\n")

    todays = list_todays_sessions()

    if not todays:
        print("No sessions found for today.")
        return

    for persona in PERSONAS:
        if persona in todays:
            info = todays[persona]
            print(f"  {persona}: {info['state']} — {info['branch']} (session: {info['session_id'][:12]}...)")
        else:
            print(f"  {persona}: no session")


def cmd_reconcile():
    """Create PRs from persona branches to main."""
    print(f"=== Evening Reconciliation — {today()} ===\n")
    # This is handled by a separate workflow (lab-evening.yml)
    # because it needs GITHUB_TOKEN for PR operations.
    print("Run the lab-evening workflow for PR creation and merging.")


def main():
    if not API_KEY:
        print("ERROR: JULES_API_KEY not set")
        sys.exit(1)

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    cmds = {
        "create-sessions": cmd_create_sessions,
        "heartbeat": cmd_heartbeat,
        "status": cmd_status,
        "reconcile": cmd_reconcile,
    }

    if cmd not in cmds:
        print(f"Usage: heartbeat.py {{{','.join(cmds.keys())}}}")
        sys.exit(1)

    cmds[cmd]()


if __name__ == "__main__":
    main()
```

Add `requests` to the dev dependencies in `pyproject.toml`.

---

## Step 2: Morning workflow

Create `.github/workflows/lab-morning.yml`:

```yaml
name: Lab Morning — Start Daily Sessions

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:
    inputs:
      personas:
        description: 'Comma-separated personas to run (or "all")'
        required: false
        default: 'all'

permissions:
  contents: write

jobs:
  start-sessions:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
          token: ${{ secrets.GITHUB_TOKEN }}

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install requests

      - name: Configure git
        run: |
          git config user.name "Lab Morning"
          git config user.email "morning@rosencrantz-lab.dev"

      - name: Create sessions
        env:
          JULES_API_KEY: ${{ secrets.JULES_API_KEY }}
        run: |
          python tools/heartbeat.py create-sessions

      - name: Note
        run: |
          echo "Sessions started. AUTO_CREATE_PR pushes work to persona branches."
          echo "Jules PRs go to persona branches, NOT main."
          echo "Evening workflow (lab-evening.yml at 20:00) creates persona → main PRs."
```

---

## Step 3: Heartbeat workflow (runs periodically during the day)

Create `.github/workflows/lab-heartbeat.yml`:

```yaml
name: Lab Heartbeat

on:
  schedule:
    # Heartbeats at 06:20, 06:40, 07:00
    - cron: '20 6 * * *'
    - cron: '40 6 * * *'
    - cron: '0 7 * * *'
  workflow_dispatch:

jobs:
  heartbeat:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install requests

      - name: Send heartbeats
        env:
          JULES_API_KEY: ${{ secrets.JULES_API_KEY }}
        run: |
          python tools/heartbeat.py status
          echo ""
          python tools/heartbeat.py heartbeat
```

---

## Step 4: Evening workflow (reconcile branches to main)

Create `.github/workflows/lab-evening.yml`:

```yaml
name: Lab Evening — Reconcile Branches

on:
  schedule:
    - cron: '0 20 * * *'
  workflow_dispatch:

permissions:
  contents: write
  pull-requests: write

jobs:
  create-prs:
    runs-on: ubuntu-latest
    strategy:
      max-parallel: 9
      matrix:
        persona: [baldo, scott, sabine, pearl, fuchs, liang, wolfram, mycroft, giles]
    outputs:
      has_conflicts: ${{ steps.pr.outputs.has_conflicts }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Find today's branch
        id: find
        run: |
          DATE=$(date -u +%Y-%m-%d)
          BRANCH="${DATE}_${{ matrix.persona }}"
          if git ls-remote --heads origin "$BRANCH" | grep -q "$BRANCH"; then
            echo "branch=$BRANCH" >> $GITHUB_OUTPUT
            echo "exists=true" >> $GITHUB_OUTPUT
          else
            echo "exists=false" >> $GITHUB_OUTPUT
          fi

      - name: Check for new commits
        if: steps.find.outputs.exists == 'true'
        id: changes
        run: |
          git fetch origin "${{ steps.find.outputs.branch }}" main
          AHEAD=$(git rev-list --count "origin/main..origin/${{ steps.find.outputs.branch }}")
          echo "ahead=$AHEAD" >> $GITHUB_OUTPUT

      - name: Create or update PR
        if: steps.find.outputs.exists == 'true' && steps.changes.outputs.ahead != '0'
        id: pr
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          BRANCH="${{ steps.find.outputs.branch }}"
          PERSONA="${{ matrix.persona }}"

          # Check if PR already exists
          EXISTING=$(gh pr list --head "$BRANCH" --json number --jq '.[0].number // empty')
          if [ -n "$EXISTING" ]; then
            echo "PR already exists: #$EXISTING"
            echo "pr_number=$EXISTING" >> $GITHUB_OUTPUT
          else
            SUMMARY=$(git log --oneline "origin/main..origin/$BRANCH" | head -10)
            PR_NUM=$(gh pr create \
              --base main --head "$BRANCH" \
              --title "[$PERSONA] $(date -u +%Y-%m-%d) session" \
              --body "## ${PERSONA}'s daily work
          ${SUMMARY}
          ---
          Auto-generated by Lab Evening." \
              | grep -oP '#\K\d+' || echo "")
            echo "pr_number=$PR_NUM" >> $GITHUB_OUTPUT
          fi

          # Check mergeability
          sleep 5  # Give GitHub a moment to compute merge status
          MERGEABLE=$(gh pr view "${{ steps.pr.outputs.pr_number || env.PR_NUM }}" --json mergeable --jq '.mergeable' 2>/dev/null || echo "UNKNOWN")
          if [ "$MERGEABLE" = "MERGEABLE" ]; then
            echo "has_conflicts=false" >> $GITHUB_OUTPUT
          else
            echo "has_conflicts=true" >> $GITHUB_OUTPUT
            gh pr edit "${{ steps.pr.outputs.pr_number || env.PR_NUM }}" --add-label "needs-conflict-resolution" 2>/dev/null || true
          fi

  resolve-conflicts:
    needs: create-prs
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: pip install requests

      - name: Ask personas to fix conflicts
        env:
          JULES_API_KEY: ${{ secrets.JULES_API_KEY }}
        run: |
          python3 << 'PYEOF'
          import json
          import os
          import subprocess
          import time
          import requests

          API = "https://jules.googleapis.com/v1alpha"
          KEY = os.environ["JULES_API_KEY"]
          HEADERS = {"x-goog-api-key": KEY, "Content-Type": "application/json"}
          DATE = time.strftime("%Y-%m-%d", time.gmtime())
          PERSONAS = ["baldo","scott","sabine","pearl","fuchs","liang","wolfram","mycroft","giles"]

          # Find which PRs have conflicts
          conflicted = []
          for persona in PERSONAS:
              branch = f"{DATE}_{persona}"
              result = subprocess.run(
                  ["gh", "pr", "list", "--head", branch, "--label", "needs-conflict-resolution",
                   "--json", "number", "--jq", ".[0].number // empty"],
                  capture_output=True, text=True
              )
              pr_num = result.stdout.strip()
              if pr_num:
                  conflicted.append((persona, branch, pr_num))

          if not conflicted:
              print("No conflicted PRs. All clean!")
              exit(0)

          print(f"Found {len(conflicted)} conflicted PR(s)")

          # Find today's active sessions
          resp = requests.get(f"{API}/sessions?pageSize=100", headers=HEADERS)
          sessions = resp.json().get("sessions", [])

          session_map = {}
          for s in sessions:
              ctx = s.get("sourceContext", {}).get("githubRepoContext", {})
              sb = ctx.get("startingBranch", "")
              if sb.startswith(DATE + "_"):
                  persona_name = sb[len(DATE) + 1:]
                  session_map[persona_name] = s["name"].split("/")[-1]

          # Send conflict resolution message to each conflicted persona
          for persona, branch, pr_num in conflicted:
              session_id = session_map.get(persona)
              if not session_id:
                  print(f"  {persona}: no active session, will handle next morning")
                  continue

              prompt = (
                  f"Your branch {branch} has merge conflicts with main. "
                  f"PR #{pr_num} is open and cannot be merged. "
                  f"Please resolve the conflicts:\n"
                  f"  git fetch origin main\n"
                  f"  git merge origin/main\n"
                  f"Resolve any conflicts (keep both sides where possible, "
                  f"prefer the more recent version for STATE.md). "
                  f"Commit the merge resolution and push."
              )

              resp = requests.post(
                  f"{API}/sessions/{session_id}:sendMessage",
                  headers=HEADERS,
                  json={"prompt": prompt},
              )
              if resp.ok:
                  print(f"  {persona}: sent conflict resolution message (session {session_id})")
              else:
                  print(f"  {persona}: failed to send message: {resp.status_code}")

          PYEOF

  # Wait for fixes, then try merging
  merge-all:
    needs: resolve-conflicts
    runs-on: ubuntu-latest
    steps:
      - name: Wait for conflict resolution
        run: sleep 300  # 5 minutes for personas to fix conflicts

      - name: Merge all ready PRs
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          DATE=$(date -u +%Y-%m-%d)

          for persona in baldo scott sabine pearl fuchs liang wolfram mycroft giles; do
            BRANCH="${DATE}_${persona}"

            # Find PR for this branch
            PR_NUM=$(gh pr list --repo franklinbaldo/rosencrantz-coin \
              --head "$BRANCH" --state open \
              --json number --jq '.[0].number // empty')

            if [ -z "$PR_NUM" ]; then
              continue
            fi

            # Check if now mergeable
            MERGEABLE=$(gh pr view "$PR_NUM" --json mergeable --jq '.mergeable')

            if [ "$MERGEABLE" = "MERGEABLE" ]; then
              echo "Merging #$PR_NUM ($persona)..."
              gh pr merge "$PR_NUM" --merge --admin || echo "Failed: #$PR_NUM"
              # Remove conflict label if it had one
              gh pr edit "$PR_NUM" --remove-label "needs-conflict-resolution" 2>/dev/null || true
              sleep 3
            else
              echo "Still conflicted: #$PR_NUM ($persona) — will handle next morning"
            fi
          done

  cleanup:
    needs: merge-all
    runs-on: ubuntu-latest
    steps:
      - name: Delete merged branches
        env:
          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          DATE=$(date -u +%Y-%m-%d)
          for persona in baldo scott sabine pearl fuchs liang wolfram mycroft giles; do
            BRANCH="${DATE}_${persona}"
            MERGED=$(gh pr list --head "$BRANCH" --state merged \
              --json number --jq '.[0].number // empty')
            if [ -n "$MERGED" ]; then
              gh api -X DELETE \
                "repos/franklinbaldo/rosencrantz-coin/git/refs/heads/$BRANCH" || true
              echo "Deleted: $BRANCH"
            else
              echo "Kept (unmerged): $BRANCH"
            fi
          done
```

---

## Step 5: Update lab-sync tool for dated branches

Update `tools/lab-sync` to discover `{date}_{persona}` branches:

In the `fetch_all()` function, fetch from the public URL:
```bash
git fetch https://github.com/franklinbaldo/rosencrantz-coin.git \
    '+refs/heads/*:refs/remotes/lab/*' --quiet 2>/dev/null
```

In `cmd_status()`, `cmd_diff()`, and `cmd_pull()`, resolve persona names to dated branches:
```bash
local date_prefix
date_prefix=$(date -u +%Y-%m-%d)
local branch="${date_prefix}_${persona}"
```

The rest of the lab-sync logic (patch generation, apply, conflict skip) stays the same — just branch names change from `{persona}` to `{date}_{persona}`.

---

## Step 6: Conflict resolution flow

The evening workflow handles conflicts in a single pass:

1. **Create PR** from persona branch to main
2. **Check mergeability** — if clean, merge immediately
3. **If conflicts** — label the PR `needs-conflict-resolution` and send a `sendMessage` to the persona's still-active Jules session: "your branch has conflicts with main, resolve them"
4. **Persona fixes conflicts** on their branch (commits go to the same branch, PR auto-updates because GitHub PRs track the branch head)
5. **Wait 5 minutes**, then try merging everything again
6. **Any PR still conflicted** survives to next morning — the morning workflow detects it and makes it the persona's first task

This works because the Jules session may still be active at 20:00. The `sendMessage` endpoint sends a message to an active session — it doesn't create a new one. If the session has already ended, the message fails silently, and the conflict carries to next morning.

The morning workflow checks for open PRs with `needs-conflict-resolution` label. If found, it starts the persona's session on yesterday's branch (not a fresh branch from main) with a conflict resolution prompt.

---

## Secrets Required

- `JULES_API_KEY`: Get from https://jules.google/settings — this is the ONLY secret needed for the Jules API
- `GITHUB_TOKEN`: Default token (already available in workflows)

The Jules API URL `https://jules.googleapis.com/v1alpha` is PUBLIC and should NOT be a secret.

---

## The Complete Daily Timeline

```
06:00  lab-morning.yml fires
       ├── Checkout repo
       ├── heartbeat.py create-sessions
       │   ├── GET /sources → find source name
       │   ├── For each persona:
       │   │   ├── git branch {date}_{persona} from main
       │   │   ├── git push origin {date}_{persona}
       │   │   └── POST /sessions → create session on that branch
       │   └── All 9 sessions now running in parallel
       │
06:20  lab-heartbeat.yml fires
       ├── heartbeat.py status → show who's active
       └── heartbeat.py heartbeat
           ├── GET /sessions?pageSize=100 → find today's by branch pattern
           └── For each active session:
               └── POST /sessions/{id}:sendMessage → "continue, sync, more work"

06:40  lab-heartbeat.yml fires again (second heartbeat)
07:00  lab-heartbeat.yml fires again (third heartbeat)

During sessions, personas can:
       └── tools/lab-sync status → see each other's branches
       └── tools/lab-sync pull scott → get patches from scott's branch
       └── AUTO_CREATE_PR pushes work to the persona branch on GitHub
           (PRs from Jules working branch → persona dated branch, NOT main)

20:00  lab-evening.yml fires
       ├── Create PRs: persona branch → main (all 9)
       ├── For each PR:
       │   ├── Mergeable? → merge immediately
       │   └── Conflicts? → label "needs-conflict-resolution"
       │       └── Send message to persona's active session:
       │           "your PR has conflicts, fix them"
       │       └── Persona commits fix to their branch
       │       └── PR auto-updates (tracks branch head)
       ├── Wait 5 minutes for fixes
       ├── Merge everything that's now clean
       └── Delete merged branches
       └── Any still-conflicted PRs survive to next morning

Next 06:00
       └── Personas with surviving conflict PRs fix them first
       └── Then fresh branches from updated main
```

---

## Session Budget

- 9 sessions created (morning)
- 3 heartbeats × 9 messages = 27 API calls (NOT sessions — sendMessage doesn't create new sessions)
- Total: **9 sessions/day**
- Leaves 91 sessions for manual work

---

## Checklist

- [ ] `tools/heartbeat.py` created
- [ ] `tools/lab-sync` updated for dated branches
- [ ] `.github/workflows/lab-morning.yml` created
- [ ] `.github/workflows/lab-heartbeat.yml` created
- [ ] `.github/workflows/lab-evening.yml` created
- [ ] `JULES_API_KEY` secret configured in repo settings
- [ ] Labels created: `auto-merge`, `needs-conflict-resolution`
- [ ] LAB_RULES.md updated with Cross-Persona Sync section
- [ ] `requests` added to pyproject.toml dev dependencies
- [ ] Source name verified via `GET /sources`
