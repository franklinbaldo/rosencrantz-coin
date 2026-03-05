#!/usr/bin/env python3
"""Lab Heartbeat — orchestrate daily persona sessions via Jules API.

Usage:
  heartbeat.py create-sessions     Create today's branches and start sessions
  heartbeat.py heartbeat           Send continue message to all active sessions
  heartbeat.py status              List today's active sessions
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests

JULES_API = "https://jules.googleapis.com/v1alpha"
API_KEY = os.environ.get("JULES_API_KEY", "")
REPO = "franklinbaldo/rosencrantz-coin"

PERSONAS = [
    "baldo", "scott", "sabine", "pearl", "fuchs",
    "liang", "wolfram", "mycroft", "giles",
]


def headers():
    return {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json",
    }


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def branch_name(persona):
    return f"{today()}_{persona}"


# ── Source discovery ─────────────────────────────────────────────────────────

def discover_source():
    """Find the source name for our repo via the Jules API."""
    resp = requests.get(f"{JULES_API}/sources", headers=headers())
    resp.raise_for_status()
    for source in resp.json().get("sources", []):
        name = source.get("name", "")
        if "franklinbaldo" in name and "rosencrantz" in name:
            print(f"  Discovered source: {name}")
            return name
    raise RuntimeError(
        f"Could not find source for {REPO}. "
        f"Available: {json.dumps(resp.json(), indent=2)}"
    )


# ── Prompt assembly (from .jules/ files, matching jules-sessions.yml) ────────

def assemble_prompt(persona):
    """Assemble a session prompt from the persona's ALL-CAPS .md files + shared rules.

    Order: SOUL.md first, then other ALL-CAPS files alphabetically,
    then shared STATE.md and LAB_RULES.md.
    """
    agent_dir = Path(f".jules/{persona}")
    parts = []

    # 1. SOUL.md first (persona identity)
    soul_file = agent_dir / "SOUL.md"
    if soul_file.is_file():
        parts.append(soul_file.read_text(encoding="utf-8"))

    # 2. Remaining ALL-CAPS .md files (excluding SOUL.md)
    if agent_dir.is_dir():
        for f in sorted(agent_dir.iterdir()):
            if not f.is_file():
                continue
            stem = f.stem
            if re.match(r"^[A-Z][A-Z0-9_-]*$", stem) and f.name != "SOUL.md":
                parts.append(f.read_text(encoding="utf-8"))

    # 3. Shared lab governance files
    for shared in [".jules/STATE.md", ".jules/LAB_RULES.md"]:
        p = Path(shared)
        if p.is_file():
            parts.append(p.read_text(encoding="utf-8"))

    if not parts:
        raise RuntimeError(f"No ALL-CAPS files found in {agent_dir}")

    # 4. Append session-specific instructions
    branch = branch_name(persona)
    parts.append(f"""
---

## Today's Session Instructions

You are starting a new lab session on branch `{branch}`.

**FIRST:** Run `tools/lab-sync status` to see what other personas are working on today.
Pull any relevant work with `tools/lab-sync pull <persona>`.

**THEN:** Follow the session structure from LAB_RULES.md:
1. Read `.jules/STATE.md` (lab state)
2. Check `lab/rfes/` for experiment requests relevant to you
3. Check your papers for unprocessed todonotes
4. Choose a session mode from your SOUL.md
5. Do your work — commit to this branch
6. Write a session log in `lab/logs/{persona}/`
7. Update EXPERIENCE.md and STATE.md as needed

Your commits will automatically appear on GitHub for other personas to see.
Do NOT create PRs to main — the evening workflow handles that.
""")

    return "\n\n".join(parts)


# ── Branch management ────────────────────────────────────────────────────────

def create_branch(persona):
    """Create today's branch for persona from main (without checkout)."""
    branch = branch_name(persona)

    subprocess.run(
        ["git", "fetch", "origin", "main"],
        check=True, capture_output=True,
    )

    # Create branch from origin/main without switching
    result = subprocess.run(
        ["git", "branch", branch, "origin/main"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        if "already exists" in result.stderr:
            print(f"  Branch {branch} already exists, skipping creation")
            return branch
        raise RuntimeError(f"Failed to create branch {branch}: {result.stderr}")

    subprocess.run(
        ["git", "push", "origin", branch],
        check=True, capture_output=True,
    )
    print(f"  Created branch: {branch}")
    return branch


# ── Session management ───────────────────────────────────────────────────────

def create_session(persona, source_name):
    """Create a Jules session for a persona."""
    branch = branch_name(persona)
    prompt = assemble_prompt(persona)

    # Count existing sessions for title numbering
    log_dir = Path(f"lab/logs/{persona}")
    actual = 0
    if log_dir.is_dir():
        actual = sum(1 for f in log_dir.rglob("*.md"))

    session_num = f"{actual + 1:03d}"
    title = f"Rosencrantz — {persona} #{session_num}"

    body = {
        "prompt": prompt,
        "title": title,
        "sourceContext": {
            "source": source_name,
            "githubRepoContext": {
                "startingBranch": branch,
            },
        },
        "automationMode": "AUTO_CREATE_PR",
    }

    resp = requests.post(f"{JULES_API}/sessions", headers=headers(), json=body)
    resp.raise_for_status()
    session = resp.json()
    session_id = session["name"].split("/")[-1]
    print(f"  Started session {session_id} for {persona} on {branch} — {title}")
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

Run `tools/lab-sync status` to check for new work from other personas since you started.
If any persona has new relevant work, pull it with `tools/lab-sync pull <persona>`.

If you have more work to do based on your session mode, continue.
Commit your work — it will appear on GitHub automatically.

If your session work is complete, write your session log in lab/logs/{persona}/
and update your EXPERIENCE.md."""

    resp = requests.post(
        f"{JULES_API}/sessions/{session_id}:sendMessage",
        headers=headers(),
        json={"prompt": prompt},
    )
    resp.raise_for_status()
    print(f"  Heartbeat sent to {persona} (session {session_id[:12]}...)")


# ── Conflict detection (for morning check) ───────────────────────────────────

def check_unresolved_conflicts():
    """Check for PRs with needs-conflict-resolution label from previous day."""
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", REPO,
         "--label", "needs-conflict-resolution",
         "--json", "number,headRefName,title",
         "--state", "open"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return []

    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return []

    return prs


# ── Commands ─────────────────────────────────────────────────────────────────

def cmd_create_sessions():
    """Create branches and start sessions for all personas."""
    print(f"=== Lab Morning — {today()} ===\n")

    # Check for unresolved conflicts from previous day
    unresolved = check_unresolved_conflicts()
    if unresolved:
        print("WARNING: Unresolved conflict PRs from previous day:")
        for pr in unresolved:
            print(f"  #{pr['number']}: {pr['title']} ({pr['headRefName']})")
        print()

    source_name = discover_source()
    print(f"Source: {source_name}\n")

    for persona in PERSONAS:
        try:
            # If persona has an unresolved conflict PR, skip fresh branch
            conflict_pr = next(
                (pr for pr in unresolved
                 if persona in pr.get("headRefName", "")),
                None,
            )
            if conflict_pr:
                print(f"  {persona}: has unresolved conflict PR #{conflict_pr['number']}")
                print(f"  Starting session on existing branch: {conflict_pr['headRefName']}")
                # Start session on the old branch to fix conflicts
                prompt = assemble_prompt(persona)
                prompt += f"""

---

## URGENT: Conflict Resolution Required

Your previous branch `{conflict_pr['headRefName']}` has merge conflicts with main.
PR #{conflict_pr['number']} cannot be merged.

**YOUR FIRST TASK:** Resolve the conflicts:
```
git fetch origin main
git merge origin/main
```
Resolve any conflicts (keep both sides where possible, prefer the more recent
version for STATE.md). Commit the merge resolution and push.

After resolving conflicts, proceed with normal session work.
"""
                body = {
                    "prompt": prompt,
                    "title": f"Rosencrantz — {persona} (conflict fix)",
                    "sourceContext": {
                        "source": source_name,
                        "githubRepoContext": {
                            "startingBranch": conflict_pr["headRefName"],
                        },
                    },
                    "automationMode": "AUTO_CREATE_PR",
                }
                resp = requests.post(
                    f"{JULES_API}/sessions", headers=headers(), json=body,
                )
                resp.raise_for_status()
                sid = resp.json()["name"].split("/")[-1]
                print(f"  Started conflict-fix session {sid}")
            else:
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
            print(
                f"  {persona}: {info['state']} — {info['branch']} "
                f"(session: {info['session_id'][:12]}...)"
            )
        else:
            print(f"  {persona}: no session")


def main():
    if not API_KEY:
        print("ERROR: JULES_API_KEY not set")
        sys.exit(1)

    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    cmds = {
        "create-sessions": cmd_create_sessions,
        "heartbeat": cmd_heartbeat,
        "status": cmd_status,
    }

    if cmd not in cmds:
        print(f"Usage: heartbeat.py {{{','.join(cmds.keys())}}}")
        sys.exit(1)

    cmds[cmd]()


if __name__ == "__main__":
    main()
