#!/usr/bin/env python3
"""Lab Heartbeat — single command to manage all persona sessions.

Usage:
  heartbeat.py heartbeat    Create or continue sessions (runs every ~15min)
  heartbeat.py status       Show current session status

Sessions are identified by title "Rosencrantz — {persona} @{sha} {datetime}".
New sessions are created when none exists, the current one is >24h old,
or infrastructure files changed on main since the session's commit.
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

PERSONAS = sorted(p.parent.name for p in Path("lab").glob("*/SOUL.md"))

TITLE_PREFIX = "Rosencrantz"
SESSION_TTL = timedelta(hours=24)

# Paths that, when changed on main, make running sessions stale.
# Persona-owned files (lab/*/SOUL.md etc.) don't count — they land on main
# only when a PR is merged, which already triggers a new session.
INFRA_PATHS = [
    "tools/",
    "lab/LAB_RULES.md",
    "lab/STATE.md",
    "lab/EXPERIMENTS.md",
]


def headers():
    return {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json",
    }


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def now_utc():
    return datetime.now(timezone.utc)


# ── Git helpers ──────────────────────────────────────────────────────────────

def get_head_sha(short=True):
    """Return current HEAD commit SHA."""
    cmd = ["git", "rev-parse", "--short" if short else "", "HEAD"]
    cmd = [c for c in cmd if c]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip() if result.returncode == 0 else ""


def has_infra_changed(session_sha):
    """Check if any infrastructure file changed between session_sha and HEAD."""
    if not session_sha:
        return True
    result = subprocess.run(
        ["git", "diff", "--name-only", f"{session_sha}..HEAD", "--"] + INFRA_PATHS,
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        # SHA not found (e.g. shallow clone) — assume stale
        return True
    return bool(result.stdout.strip())


# ── Session discovery (by title) ─────────────────────────────────────────────

def parse_sha_from_title(title):
    """Extract commit SHA from title like 'Rosencrantz — baldo #003 @abc1234'."""
    m = re.search(r"@([0-9a-f]{7,40})", title)
    return m.group(1) if m else None


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


# ── PR merging ───────────────────────────────────────────────────────────────

def find_persona_pr(persona):
    """Find a persona's open PR number targeting main. Returns int or None."""
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", REPO, "--base", "main", "--state", "open",
         "--json", "number,title,headRefName", "--limit", "50"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return None

    for pr in prs:
        title = pr.get("title", "").lower()
        head = pr.get("headRefName", "")
        if persona in title or f"_{persona}" in head or f"_{persona}-" in head:
            return pr["number"]
    return None


def merge_persona_pr(persona):
    """Try to merge a persona's open PR into main.

    Returns: 'merged', 'conflict', or 'none' (no PR found).
    """
    pr_num = find_persona_pr(persona)
    if pr_num is None:
        return "none"

    # Check mergeable status
    result = subprocess.run(
        ["gh", "pr", "view", str(pr_num), "--repo", REPO,
         "--json", "mergeable", "--jq", ".mergeable"],
        capture_output=True, text=True,
    )
    mergeable = result.stdout.strip()

    if mergeable == "CONFLICTING":
        print(f"    PR #{pr_num}: conflicts (Jules CI fixer will handle)")
        return "conflict"

    if mergeable != "MERGEABLE":
        print(f"    PR #{pr_num}: mergeable={mergeable}, skipping")
        return "none"

    # Merge
    result = subprocess.run(
        ["gh", "pr", "merge", str(pr_num), "--repo", REPO, "--merge"],
        capture_output=True, text=True,
    )
    if result.returncode == 0:
        print(f"    Merged PR #{pr_num}")
        return "merged"

    print(f"    Merge failed: {result.stderr.strip()}")
    return "conflict"


# ── Announcements ────────────────────────────────────────────────────────────

ANNOUNCEMENT_CHAR_LIMIT = 250


def collect_announcements(exclude_persona=None):
    """Collect .announcements.md from all persona folders (max 250 chars each)."""
    announcements = []
    for p in PERSONAS:
        if p == exclude_persona:
            continue
        ann_file = Path(f"lab/{p}/.announcements.md")
        if ann_file.is_file():
            text = ann_file.read_text(encoding="utf-8").strip()
            if text:
                if len(text) > ANNOUNCEMENT_CHAR_LIMIT:
                    text = text[:ANNOUNCEMENT_CHAR_LIMIT] + "..."
                announcements.append((p, text))
    return announcements


def format_announcements(exclude_persona=None):
    """Format announcements block for inclusion in prompts."""
    items = collect_announcements(exclude_persona)
    if not items:
        return ""
    parts = ["\n---\n\n## Lab Announcements\n"]
    for persona, text in items:
        parts.append(f"### {persona}\n```\n{text}\n```\n")
    return "\n".join(parts)


# ── Prompt assembly ───────────────────────────────────────────────────────────

def assemble_prompt(persona):
    """Assemble session prompt from persona's ALL-CAPS .md files + shared rules."""
    persona_dir = Path(f"lab/{persona}")
    parts = []

    soul_file = persona_dir / "SOUL.md"
    if soul_file.is_file():
        parts.append(soul_file.read_text(encoding="utf-8"))

    # Read all ALL-CAPS .md files from persona dir (EXPERIENCE.md, etc.)
    if persona_dir.is_dir():
        for f in sorted(persona_dir.iterdir()):
            if not f.is_file():
                continue
            stem = f.stem
            if re.match(r"^[A-Z][A-Z0-9_-]*$", stem) and f.name != "SOUL.md":
                parts.append(f.read_text(encoding="utf-8"))

    # Shared lab files
    for shared in ["lab/STATE.md", "lab/LAB_RULES.md", "lab/EXPERIMENTS.md"]:
        p = Path(shared)
        if p.is_file():
            parts.append(p.read_text(encoding="utf-8"))

    if not parts:
        raise RuntimeError(f"No ALL-CAPS files found in {persona_dir}")

    # Collect announcements from other personas
    ann_block = format_announcements(exclude_persona=persona)
    if ann_block:
        parts.append(ann_block)

    parts.append(f"""
---

## Session Instructions

You are starting a new lab session. Your branch starts from main.

**First, log in (required by all tools):**
```
tools/lab login {persona}
```

**Follow the session structure from LAB_RULES.md:**
1. Sync: `tools/lab sync` — **read the NOTIFICATIONS at the end, they tell you what needs attention**
2. Read `lab/STATE.md` (lab state — read-only, do not modify)
3. Check your mail: `tools/lab mail` (mail is delivered by the heartbeat on main)
4. Check `lab/*/experiments/*/rfe.md` for experiment requests relevant to you
5. Choose a session mode from your SOUL.md
6. Do your work — commit to this branch
7. Write a log for this round in `lab/{persona}/logs/`
8. Update your `lab/{persona}/EXPERIENCE.md`

**CRITICAL — THE GOLDEN RULE OF FILE OWNERSHIP:**
You may ONLY create or modify files under folders that contain YOUR persona name ("{persona}") in the path.
The persona prefix in filenames is just a naming convention — it does NOT grant write access. This is non-negotiable.

You CAN touch:
- `lab/{persona}/` — everything under your persona folder (SOUL.md, EXPERIENCE.md, colab, logs, notes, experiments, mail, retracted, published)

You MUST NOT touch (even to "fix" things):
- Any file under another persona's `lab/{{other}}/` directory
- pyproject.toml, src/, tools/, any root file
- lab/STATE.md, lab/LAB_RULES.md, lab/EXPERIMENTS.md
- Other personas' files

If you touch files outside your ownership, your PR will conflict and ALL your work will be lost.

**Reading other personas' work:**
After `tools/lab sync`, other personas' repos are cloned into `workspace/`.
Example: `workspace/pearl/lab/pearl/colab/pearl_*.tex` for Pearl's papers.
The workspace is gitignored — it's a read-only cache, never committed.

Your commits will automatically appear on GitHub for other personas to see.
Do NOT create PRs to main — the evening workflow handles that.
Do NOT compile LaTeX (no pdflatex, no texlive). Just write .tex source files.
Do NOT install system packages (no apt-get, no sudo).

**Retracting papers:** Move to `lab/{persona}/retracted/` to free a colab slot.
**Co-signing for publication:** Copy the paper to `lab/{persona}/published/`. When 3 personas have the same paper in their published/ folder, reconciliation graduates it to `published/` at repo root.
**Broadcasting:** Write `lab/{persona}/.announcements.md` (max 250 chars) to broadcast a message to all personas. It will be included in their next session/heartbeat prompt. Use it for important updates: settled questions, new results, calls for collaboration.

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

    sha = get_head_sha(short=True)
    ts = now_utc().strftime("%Y-%m-%dT%H:%M")
    title = f"{TITLE_PREFIX} — {persona} @{sha} {ts}"

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
    ann_block = format_announcements(exclude_persona=persona)

    prompt = f"""This is continuation round #{hb_number}. Other personas have been working in parallel.

1. **Log in** (if not already): `tools/lab login {persona}`
2. **Sync:** `tools/lab sync` — clones all persona branches into workspace + inbox from main. **Read the NOTIFICATIONS section at the end carefully — it tells you what needs your attention.**
3. **Check mail:** `tools/lab mail` — read with `tools/lab mail read <num>`.
4. **Read other personas' work** — after sync, their repos are in `workspace/{{name}}/`. Example: `workspace/pearl/lab/pearl/colab/pearl_*.tex`.
{ann_block}
**Your task:** Check the sync notifications, then do meaningful work. Some options:
- Respond to another persona's work (paper, annotation, mail, RFE)
- Continue your own ongoing work
- Start something new based on what you read

**GOLDEN RULE — only touch files under `lab/{persona}/`:**
- `lab/{persona}/` — SOUL.md, EXPERIENCE.md, colab, logs, notes, experiments, mail, retracted, published
- Do NOT touch: any other persona's `lab/{{other}}/`, pyproject.toml, src/, tools/, lab/STATE.md, lab/LAB_RULES.md
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

        needs_new = False
        reason = ""

        if force_new:
            needs_new = True
            reason = "forced"
        elif not info:
            needs_new = True
            reason = "no session"
        elif info["state"] in ("COMPLETED", "FAILED"):
            needs_new = True
            reason = f"previous {info['state'].lower()}"
        elif is_expired(info):
            needs_new = True
            reason = "expired (>24h)"
        elif has_infra_changed(parse_sha_from_title(info.get("title", ""))):
            needs_new = True
            reason = "infra changed on main"

        if needs_new:
            # Try to merge the persona's PR before creating a new session
            merge = merge_persona_pr(persona)
            if merge == "conflict":
                print(f"  {persona}: PR has conflicts — skipping until resolved")
                results[persona] = "-> conflict (waiting for CI fix)"
                continue

            if merge == "merged":
                reason += ", merged PR"

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
    head = get_head_sha(short=True)
    print(f"=== Lab Status === (main @{head})\n")

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
            session_sha = parse_sha_from_title(info.get("title", ""))
            stale = " STALE" if session_sha and has_infra_changed(session_sha) else ""
            print(
                f"  {persona}: {info['state']}{expired}{stale} — "
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
