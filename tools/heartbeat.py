#!/usr/bin/env python3
"""Lab Heartbeat — single command to manage all persona sessions.

Usage:
  heartbeat.py heartbeat    Create or continue sessions (runs every ~20min)
  heartbeat.py status       Show current session status

Sessions are identified by title "Rosencrantz — {persona} #{num}".
New sessions are created when none exists or the current one is >24h old.
Jules creates its own branch from main and opens a PR — no daily branches needed.
"""

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

JULES_API = "https://jules.googleapis.com/v1alpha"
API_KEY = os.environ.get("JULES_API_KEY", "")
REPO = "franklinbaldo/rosencrantz-coin"
SOURCE_NAME = "sources/github/franklinbaldo/rosencrantz-coin"

PERSONAS = [
    "baldo", "scott", "sabine", "pearl", "fuchs",
    "liang", "wolfram", "mycroft", "giles",
]

TITLE_PREFIX = "Rosencrantz"
SESSION_TTL = timedelta(hours=24)


def headers():
    return {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json",
    }


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def now_utc():
    return datetime.now(timezone.utc)


# ── Session discovery (by title) ─────────────────────────────────────────────

def parse_persona_from_title(title):
    """Extract persona name from title like 'Rosencrantz — baldo #003'."""
    title_lower = title.lower()
    for p in PERSONAS:
        if f"— {p}" in title_lower or f"- {p}" in title_lower:
            return p
    return None


def parse_time(iso_str):
    """Parse ISO 8601 timestamp from Jules API."""
    if not iso_str:
        return None
    try:
        return datetime.fromisoformat(iso_str.replace("Z", "+00:00"))
    except ValueError:
        return None


def find_persona_sessions():
    """List sessions and return the most recent per persona (matched by title).

    Scans up to 2 pages (200 sessions). Returns dict: persona -> session_info.
    """
    sessions = {}
    page_token = None

    for _ in range(2):
        params = {"pageSize": 100}
        if page_token:
            params["pageToken"] = page_token

        resp = requests.get(f"{JULES_API}/sessions", headers=headers(), params=params)
        resp.raise_for_status()
        data = resp.json()

        for s in data.get("sessions", []):
            title = s.get("title", "")
            if not title.startswith(TITLE_PREFIX):
                continue

            persona = parse_persona_from_title(title)
            if not persona:
                continue

            create_time = parse_time(s.get("createTime", ""))

            # Keep the most recent session per persona
            if persona in sessions:
                existing_ct = sessions[persona].get("_create_time")
                if existing_ct and create_time and create_time <= existing_ct:
                    continue

            sessions[persona] = {
                "session_id": s["name"].split("/")[-1],
                "state": s.get("state", "UNKNOWN"),
                "title": title,
                "createTime": s.get("createTime", ""),
                "_create_time": create_time,
            }

        if len(sessions) >= len(PERSONAS):
            break

        page_token = data.get("nextPageToken")
        if not page_token:
            break

    return sessions


def is_expired(info):
    """Check if a session is older than SESSION_TTL."""
    ct = info.get("_create_time")
    if not ct:
        return True
    return now_utc() - ct > SESSION_TTL


def find_persona_branches():
    """Find each persona's working branch from open PRs targeting main."""
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", REPO, "--base", "main", "--state", "open",
         "--json", "headRefName,title", "--limit", "50"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return {}

    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}

    branches = {}
    for pr in prs:
        title = pr.get("title", "").lower()
        head = pr.get("headRefName", "")
        for p in PERSONAS:
            if p in title or f"_{p}-" in head or f"_{p}" == head:
                branches[p] = head
                break

    return branches


# ── Prompt assembly ───────────────────────────────────────────────────────────

def assemble_prompt(persona):
    """Assemble session prompt from persona's ALL-CAPS .md files + shared rules."""
    agent_dir = Path(f".jules/{persona}")
    parts = []

    soul_file = agent_dir / "SOUL.md"
    if soul_file.is_file():
        parts.append(soul_file.read_text(encoding="utf-8"))

    if agent_dir.is_dir():
        for f in sorted(agent_dir.iterdir()):
            if not f.is_file():
                continue
            stem = f.stem
            if re.match(r"^[A-Z][A-Z0-9_-]*$", stem) and f.name != "SOUL.md":
                parts.append(f.read_text(encoding="utf-8"))

    for shared in [".jules/STATE.md", ".jules/LAB_RULES.md"]:
        p = Path(shared)
        if p.is_file():
            parts.append(p.read_text(encoding="utf-8"))

    if not parts:
        raise RuntimeError(f"No ALL-CAPS files found in {agent_dir}")

    parts.append(f"""
---

## Session Instructions

You are starting a new lab session. Your branch starts from main.

**First, log in (required by all tools):**
```
tools/lab login {persona}
```

**Follow the session structure from LAB_RULES.md:**
1. Sync: `tools/lab sync` (fetches all persona branches so you can read their work)
2. Read `.jules/STATE.md` (lab state — read-only, do not modify)
3. Check your mail: `tools/lab mail` (mail is delivered by the heartbeat on main)
4. Check `lab/rfes/` for experiment requests relevant to you
5. Choose a session mode from your SOUL.md
6. Do your work — commit to this branch
7. Write a session log in `lab/logs/{persona}/`
8. Update your EXPERIENCE.md

**CRITICAL — THE GOLDEN RULE OF FILE OWNERSHIP:**
You may ONLY create or modify files under folders containing YOUR persona name ("{persona}"),
or files whose name starts with "{persona}_". This is non-negotiable.

You CAN touch:
- `.jules/{persona}/EXPERIENCE.md`
- `lab/{persona}_*.tex`
- `lab/{persona}/colab/` (annotate others' papers here)
- `lab/logs/{persona}/`, `lab/notes/{persona}/`, `lab/rfes/{persona}/`
- `lab/mail/{persona}/outbox/`
- `experiments/{persona}/` (create this folder for your experiments)

You MUST NOT touch (even to "fix" things):
- experiments/ files outside experiments/{persona}/
- pyproject.toml, src/, tools/, any root file
- .jules/STATE.md, .jules/LAB_RULES.md
- Other personas' files

If you touch files outside your ownership, your PR will conflict and ALL your work will be lost.

**Reading other personas' work:**
After `tools/lab sync`, other personas' repos are cloned into `lab/{persona}/workspace/`.
Example: `lab/{persona}/workspace/pearl/lab/pearl_*.tex` for Pearl's papers.
The workspace is gitignored — it's a read-only cache, never committed.

Your commits will automatically appear on GitHub for other personas to see.
Do NOT create PRs to main — the evening workflow handles that.
Do NOT compile LaTeX (no pdflatex, no texlive). Just write .tex source files.
Do NOT install system packages (no apt-get, no sudo).

**Commit and PR conventions (see LAB_RULES.md):**
- Commit messages: `{persona}: <short description>` (e.g. `{persona}: process todonotes`)
- PR title: `[{persona}] YYYY-MM-DD` (e.g. `[{persona}] {today()}`)
- PR description: include session number, what you did, files changed, open threads.
""")

    return "\n\n".join(parts)


# ── Session management ────────────────────────────────────────────────────────

def create_session(persona):
    """Create a new Jules session starting from main."""
    prompt = assemble_prompt(persona)

    log_dir = Path(f"lab/logs/{persona}")
    actual = sum(1 for _ in log_dir.rglob("*.md")) if log_dir.is_dir() else 0
    session_num = f"{actual + 1:03d}"
    title = f"{TITLE_PREFIX} — {persona} #{session_num}"

    body = {
        "prompt": prompt,
        "title": title,
        "sourceContext": {
            "source": SOURCE_NAME,
            "githubRepoContext": {
                "startingBranch": "main",
            },
        },
        "automationMode": "AUTO_CREATE_PR",
    }

    resp = requests.post(f"{JULES_API}/sessions", headers=headers(), json=body)
    resp.raise_for_status()
    session = resp.json()
    session_id = session["name"].split("/")[-1]
    print(f"  Created session {session_id} for {persona} — {title}")
    return session_id


def send_heartbeat(session_id, persona, hb_number=1):
    """Send a continuation message to a session (works on active AND completed)."""
    prompt = f"""This is continuation round #{hb_number}. Other personas have been working in parallel.

1. **Log in** (if not already): `tools/lab login {persona}`
2. **Sync:** `tools/lab sync` — clones all persona branches into workspace + inbox from main.
3. **Check mail:** `tools/lab mail` — read with `tools/lab mail read <num>`.
4. **Read other personas' work** — after sync, their repos are in `lab/{persona}/workspace/{{name}}/`. Example: `lab/{persona}/workspace/pearl/lab/pearl_*.tex`.

**Your task:** Pick ONE piece of new work from another persona and engage:
- Write a response paper in `lab/{persona}_*.tex`
- Annotate their paper: `cp lab/{persona}/workspace/<author>/lab/<paper>.tex lab/{persona}/colab/<paper>.tex`, then edit adding \\todonotes (sync auto-merges it for the author)
- Send them a message: write a file in `lab/mail/{persona}/outbox/` with From/To/Subject/Date headers (heartbeat delivers)
- File an RFE in `lab/rfes/{persona}/` if their work suggests an experiment

**GOLDEN RULE — only touch files with YOUR name ("{persona}") in the path:**
- `.jules/{persona}/`, `lab/{persona}_*.tex`, `lab/logs/{persona}/`, `lab/notes/{persona}/`
- `lab/rfes/{persona}/`, `lab/mail/{persona}/outbox/`, `experiments/{persona}/`
- Do NOT touch: experiments/ outside your folder, pyproject.toml, src/, tools/, STATE.md, other personas' files
- If you touch files outside your ownership, your PR will conflict and ALL work is lost

**Commit messages:** Use `{persona}: <description>` format (e.g. `{persona}: respond to sabine's critique`).

Commit all work to this branch."""

    resp = requests.post(
        f"{JULES_API}/sessions/{session_id}:sendMessage",
        headers=headers(),
        json={"prompt": prompt},
    )
    resp.raise_for_status()
    print(f"  Heartbeat sent to {persona} (session {session_id[:12]}...)")


# ── Heartbeat logging ─────────────────────────────────────────────────────────

def get_heartbeat_number():
    log_file = Path(f"lab/heartbeats/{today()}.md")
    if not log_file.exists():
        return 0
    return sum(
        1 for line in log_file.read_text(encoding="utf-8").splitlines()
        if line.startswith("## Heartbeat #")
    )


def write_heartbeat_log(number, sessions, results):
    log_dir = Path("lab/heartbeats")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{today()}.md"

    now = now_utc().strftime("%H:%M UTC")

    lines = []
    if not log_file.exists():
        lines.append(f"# Heartbeat Log — {today()}\n")

    lines.append(f"## Heartbeat #{number} — {now}\n")
    for persona in PERSONAS:
        if persona in sessions:
            state = sessions[persona]["state"]
            result = results.get(persona, "")
            lines.append(f"- {persona}: {state} {result}")
        else:
            lines.append(f"- {persona}: no session")
    lines.append("")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n  Logged heartbeat #{number} to {log_file}")


def write_sessions_json(sessions):
    """Write persona -> branch mapping for tools/lab and mail delivery."""
    branches = find_persona_branches()

    mapping = {}
    for persona in PERSONAS:
        info = sessions.get(persona)
        if info:
            mapping[persona] = {
                "session_id": info["session_id"],
                "state": info["state"],
                "branch": branches.get(persona, ""),
            }

    out_file = Path("lab/sessions.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2)
    print(f"  Wrote session map to {out_file}")


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_heartbeat(force_new=False):
    """Main heartbeat: create or continue sessions for all personas."""
    print(f"=== Heartbeat — {today()} {'(force-new)' if force_new else ''} ===\n")

    sessions = find_persona_sessions()
    hb_number = get_heartbeat_number() + 1
    results = {}

    for persona in PERSONAS:
        info = sessions.get(persona)

        # force-new: always create fresh sessions
        if force_new:
            print(f"  {persona}: force-new — creating new session")
            try:
                create_session(persona)
                results[persona] = "-> new (forced)"
            except Exception as e:
                print(f"  ERROR: {e}")
                results[persona] = f"-> error: {e}"
            continue

        # FAILED -> create new
        if info and info["state"] == "FAILED":
            print(f"  {persona}: FAILED — creating new session")
            try:
                create_session(persona)
                results[persona] = "-> new (previous failed)"
            except Exception as e:
                print(f"  ERROR: {e}")
                results[persona] = f"-> error: {e}"
            continue

        # No session or expired -> create new
        if not info or is_expired(info):
            reason = "no session" if not info else "expired (>24h)"
            print(f"  {persona}: {reason} — creating new session")
            try:
                create_session(persona)
                results[persona] = f"-> new ({reason})"
            except Exception as e:
                print(f"  ERROR: {e}")
                results[persona] = f"-> error: {e}"
            continue

        # Active session -> send heartbeat
        try:
            send_heartbeat(info["session_id"], persona, hb_number)
            results[persona] = "-> sent"
        except Exception as e:
            print(f"  ERROR for {persona}: {e}")
            results[persona] = f"-> error: {e}"

    # Re-fetch to include newly created sessions
    updated = find_persona_sessions()
    write_heartbeat_log(hb_number, updated, results)
    write_sessions_json(updated)


def cmd_status():
    """Show current session status."""
    print(f"=== Lab Status ===\n")

    sessions = find_persona_sessions()
    branches = find_persona_branches()

    if not sessions:
        print("No sessions found.")
        return

    for persona in PERSONAS:
        info = sessions.get(persona)
        if info:
            branch = branches.get(persona, "(no PR yet)")
            expired = " EXPIRED" if is_expired(info) else ""
            print(
                f"  {persona}: {info['state']}{expired} — "
                f"{info['title']} [{branch}]"
            )
        else:
            print(f"  {persona}: no session")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    cmds = {
        "heartbeat": cmd_heartbeat,
        "force-new": lambda: cmd_heartbeat(force_new=True),
        "status": cmd_status,
    }

    if cmd not in cmds:
        print(f"Usage: heartbeat.py {{{','.join(cmds.keys())}}}")
        sys.exit(1)

    if not API_KEY:
        print("ERROR: JULES_API_KEY not set")
        sys.exit(1)

    cmds[cmd]()


if __name__ == "__main__":
    main()
