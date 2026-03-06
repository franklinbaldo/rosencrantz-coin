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
import shutil
import subprocess
import sys
import time
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

SEQUENCE_FILE = Path("lab/heartbeats/sequence.txt")
PUBLISHING_QUEUE_FILE = Path("lab/heartbeats/publishing_queue.json")
PUBLISH_GRACE_HEARTBEATS = 3

# Paths that, when changed on main, make running sessions stale.
# Persona-owned files (lab/*/SOUL.md etc.) don't count — they land on main
# only when a PR is merged, which already triggers a new session.
INFRA_PATHS = [
    "tools/",
    "lab/LAB_RULES.md",
    "lab/STATE.md",
    "lab/EXPERIMENTS.md",
]


SESSION_CREATE_DELAY = 2  # seconds between session creations to avoid rate limits


def headers():
    return {
        "x-goog-api-key": API_KEY,
        "Content-Type": "application/json",
    }


def api_request(method, url, retries=3, **kwargs):
    """Make an API request with retry logic and detailed error reporting."""
    for attempt in range(retries):
        resp = requests.request(method, url, **kwargs)
        if resp.ok:
            return resp
        body = resp.text[:500] if resp.text else "(empty)"
        print(f"    API {resp.status_code} (attempt {attempt + 1}/{retries}): {body}")
        if resp.status_code in (429, 500, 502, 503) and attempt < retries - 1:
            wait = 2 ** (attempt + 1)
            print(f"    Retrying in {wait}s...")
            time.sleep(wait)
            continue
        resp.raise_for_status()
    return resp


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

        resp = api_request("GET", f"{JULES_API}/sessions",
                           headers=headers(), params=params)
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


def auto_merge_all():
    """Merge all open persona PRs that are MERGEABLE with passing checks.

    Runs every heartbeat cycle to keep PRs from piling up.
    Uses `gh pr view` per PR because `gh pr list` returns UNKNOWN for mergeable.
    """
    print("=== Auto-merge open PRs ===\n")

    # Get list of open PR numbers + titles
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", REPO, "--base", "main", "--state", "open",
         "--json", "number,title", "--limit", "100"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        print("  Could not list PRs")
        return 0

    try:
        prs = json.loads(result.stdout)
    except json.JSONDecodeError:
        return 0

    if not prs:
        print("  (no open PRs)")
        return 0

    print(f"  {len(prs)} open PRs, checking each...\n")
    merged = 0

    for pr in prs:
        num = pr["number"]
        title = pr.get("title", "")

        # gh pr view triggers GitHub to compute mergeable status
        result = subprocess.run(
            ["gh", "pr", "view", str(num), "--repo", REPO,
             "--json", "mergeable,statusCheckRollup"],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            continue

        try:
            detail = json.loads(result.stdout)
        except json.JSONDecodeError:
            continue

        mergeable = detail.get("mergeable", "")

        if mergeable == "CONFLICTING":
            # Close stale conflicting PRs — newer PRs from the same persona
            # already landed on main, making these unmergeable.
            subprocess.run(
                ["gh", "pr", "close", str(num), "--repo", REPO, "--delete-branch",
                 "--comment", "Auto-closed: conflicts with main (superseded by newer PR)."],
                capture_output=True, text=True,
            )
            print(f"  #{num} {title} — conflict, CLOSED")
            continue

        if mergeable != "MERGEABLE":
            print(f"  #{num} {title} — {mergeable}, skipping")
            continue

        # Check all status checks passed
        checks = detail.get("statusCheckRollup", []) or []
        pending = any(c.get("status") != "COMPLETED" for c in checks)
        if pending:
            print(f"  #{num} {title} — checks pending")
            continue

        all_passed = all(
            c.get("conclusion") in ("SUCCESS", "SKIPPED", "NEUTRAL")
            for c in checks
            if c.get("status") == "COMPLETED"
        )
        if not all_passed:
            print(f"  #{num} {title} — checks failed")
            continue

        # Merge
        result = subprocess.run(
            ["gh", "pr", "merge", str(num), "--repo", REPO, "--merge"],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print(f"  #{num} {title} — MERGED")
            merged += 1
        else:
            print(f"  #{num} {title} — merge failed: {result.stderr.strip()[:100]}")

    if merged == 0:
        print("\n  (no PRs ready to merge)")
    else:
        print(f"\n  {merged} PR(s) merged")

    return merged


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


# ── Global sequence counter ───────────────────────────────────────────────────

def get_next_sequence_number():
    """Read, increment, and persist a global heartbeat sequence number."""
    SEQUENCE_FILE.parent.mkdir(parents=True, exist_ok=True)
    if SEQUENCE_FILE.exists():
        try:
            n = int(SEQUENCE_FILE.read_text(encoding="utf-8").strip())
        except (ValueError, OSError):
            n = 0
    else:
        n = 0
    n += 1
    SEQUENCE_FILE.write_text(str(n), encoding="utf-8")
    return n


# ── Publication tracking ─────────────────────────────────────────────────────

def scan_published_papers():
    """Scan lab/*/published/ for co-signed papers.

    Returns dict: {filename: {"count": N, "personas": [...], "author": str}}
    Author is inferred from filename prefix (e.g. pearl_*.tex -> pearl).
    """
    papers = {}
    for persona in PERSONAS:
        pub_dir = Path(f"lab/{persona}/published")
        if not pub_dir.is_dir():
            continue
        for f in pub_dir.iterdir():
            if not f.is_file() or not f.name.endswith(".tex"):
                continue
            name = f.name
            if name not in papers:
                # Infer author from filename prefix
                author = ""
                for p in PERSONAS:
                    if name.startswith(f"{p}_"):
                        author = p
                        break
                papers[name] = {"count": 0, "personas": [], "author": author}
            papers[name]["count"] += 1
            papers[name]["personas"].append(persona)
    return papers


def load_publishing_queue():
    """Load the publishing queue from disk."""
    if PUBLISHING_QUEUE_FILE.exists():
        try:
            return json.loads(PUBLISHING_QUEUE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_publishing_queue(queue):
    """Save the publishing queue to disk."""
    PUBLISHING_QUEUE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PUBLISHING_QUEUE_FILE, "w", encoding="utf-8") as f:
        json.dump(queue, f, indent=2)


def check_publication_milestones(pub_data, seq_number):
    """Check for papers reaching 3 co-signs. Returns (celebrations, queue_updates).

    celebrations: list of formatted celebration strings
    """
    queue = load_publishing_queue()
    celebrations = []

    for paper, info in pub_data.items():
        if info["count"] >= 3 and paper not in queue:
            # New paper reached threshold!
            queue[paper] = {
                "author": info["author"],
                "cosigners": info["personas"][:],
                "reached_3_at_seq": seq_number,
                "status": "polishing",
            }
            celebrations.append(
                f"\n🎉🎉🎉 PAPER REACHED 3 CO-SIGNS! 🎉🎉🎉\n"
                f"📜 \"{paper}\"\n"
                f"✍️  Co-signed by: {', '.join(info['personas'])}\n"
                f"🥂 Congratulations to all contributors!\n"
                f"📝 {info['author']}: You have {PUBLISH_GRACE_HEARTBEATS} heartbeats "
                f"to do final polish before auto-publication.\n"
            )

    # Check for papers ready to graduate (grace period elapsed)
    for paper, entry in list(queue.items()):
        if entry["status"] == "polishing":
            elapsed = seq_number - entry["reached_3_at_seq"]
            if elapsed >= PUBLISH_GRACE_HEARTBEATS:
                # Auto-publish: copy from author's colab to published/ at root
                author = entry["author"]
                src = Path(f"lab/{author}/colab/{paper}")
                dst = Path(f"published/{paper}")
                if src.exists() and not dst.exists():
                    dst.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(src, dst)
                    # Stage for the next commit (heartbeat log commit or manual)
                    subprocess.run(["git", "add", str(dst)],
                                   capture_output=True, text=True)
                    celebrations.append(
                        f"\n🎊🎊🎊 PAPER GRADUATED TO published/! 🎊🎊🎊\n"
                        f"📜 \"{paper}\" is now permanently published.\n"
                        f"✍️  Authors: {', '.join(entry['cosigners'])}\n"
                    )
                entry["status"] = "graduated"

    save_publishing_queue(queue)
    return celebrations


def format_publication_table(pub_data, seq_number):
    """Format a per-author publication scoreboard table."""
    # Gather stats per author
    stats = {}
    for p in PERSONAS:
        colab_dir = Path(f"lab/{p}/colab")
        working = len(list(colab_dir.glob("*.tex"))) if colab_dir.is_dir() else 0
        stats[p] = {
            "working": working,
            "cosigns_received": 0,
            "cosigns_given": 0,
            "published": 0,
        }

    # Count co-signs received (papers where this persona is the author)
    for paper, info in pub_data.items():
        author = info["author"]
        if author in stats:
            stats[author]["cosigns_received"] += info["count"]

    # Count co-signs given (papers this persona co-signed)
    for paper, info in pub_data.items():
        for p in info["personas"]:
            if p in stats:
                stats[p]["cosigns_given"] += 1

    # Count graduated papers
    pub_root = Path("published")
    if pub_root.is_dir():
        for f in pub_root.glob("*.tex"):
            author = ""
            for p in PERSONAS:
                if f.name.startswith(f"{p}_"):
                    author = p
                    break
            if author in stats:
                stats[author]["published"] += 1

    # Build table
    lines = [
        "\n## 📊 Publication Scoreboard\n",
        "| Author   | Working Papers | Co-signs Received | Co-signs Given | Published |",
        "|----------|---------------|-------------------|----------------|-----------|",
    ]
    for p in PERSONAS:
        s = stats[p]
        lines.append(
            f"| {p:<8} | {s['working']:>13} | {s['cosigns_received']:>17} "
            f"| {s['cosigns_given']:>14} | {s['published']:>9} |"
        )

    # Publishing queue status
    queue = load_publishing_queue()
    polishing = [(k, v) for k, v in queue.items() if v["status"] == "polishing"]
    if polishing:
        lines.append("")
        lines.append("### ⏳ Papers in Final Polish Window")
        for paper, entry in polishing:
            remaining = max(0, PUBLISH_GRACE_HEARTBEATS - (seq_number - entry["reached_3_at_seq"]))
            lines.append(
                f"- 📜 **{paper}** — {remaining} heartbeat(s) remaining "
                f"(author: {entry['author']}, co-signers: {', '.join(entry['cosigners'])})"
            )

    return "\n".join(lines)


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

    resp = api_request("POST", f"{JULES_API}/sessions",
                       headers=headers(), json=body)
    session = resp.json()
    session_id = session["name"].split("/")[-1]
    print(f"  Created session {session_id} for {persona} — {title}")
    return session_id


def send_heartbeat(session_id, persona, hb_number=1, pub_block=""):
    """Send a continuation message to a session (works on active AND completed)."""
    ann_block = format_announcements(exclude_persona=persona)

    prompt = f"""This is continuation round #{hb_number}. Other personas have been working in parallel.

1. **Log in** (if not already): `tools/lab login {persona}`
2. **Sync:** `tools/lab sync` — clones all persona branches into workspace + inbox from main. **Read the NOTIFICATIONS section at the end carefully — it tells you what needs your attention.**
3. **Check mail:** `tools/lab mail` — read with `tools/lab mail read <num>`.
4. **Read other personas' work** — after sync, their repos are in `workspace/{{name}}/`. Example: `workspace/pearl/lab/pearl/colab/pearl_*.tex`.
{ann_block}{pub_block}
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

    resp = api_request(
        "POST",
        f"{JULES_API}/sessions/{session_id}:sendMessage",
        headers=headers(),
        json={"prompt": prompt},
    )
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


def write_heartbeat_log(number, sessions, results, seq_number=0,
                        pub_table="", celebrations=None):
    log_dir = Path("lab/heartbeats")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / f"{today()}.md"

    now_ts = now_utc()
    now_str = now_ts.strftime("%Y-%m-%d %H:%M UTC")

    lines = []
    if not log_file.exists():
        lines.append(f"# Heartbeat Log — {today()}\n")

    lines.append(f"## Heartbeat #{number} (seq #{seq_number}) — {now_str}\n")
    for persona in PERSONAS:
        if persona in sessions:
            state = sessions[persona]["state"]
            result = results.get(persona, "")
            lines.append(f"- {persona}: {state} {result}")
        else:
            lines.append(f"- {persona}: no session")
    lines.append("")

    # Add celebrations
    if celebrations:
        for c in celebrations:
            lines.append(c)

    # Add publication table
    if pub_table:
        lines.append(pub_table)
        lines.append("")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"\n  Logged heartbeat #{number} (seq #{seq_number}) to {log_file}")


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
    seq_number = get_next_sequence_number()
    now_ts = now_utc()
    print(f"=== Heartbeat seq #{seq_number} — {now_ts.strftime('%Y-%m-%d %H:%M UTC')} "
          f"{'(force-new)' if force_new else ''} ===\n")

    # Merge all ready PRs first so new sessions start from latest main
    auto_merge_all()
    print()

    # Scan publication state
    pub_data = scan_published_papers()
    celebrations = check_publication_milestones(pub_data, seq_number)
    pub_table = format_publication_table(pub_data, seq_number)

    if celebrations:
        print("\n".join(celebrations))

    # Build publication block for persona prompts
    pub_prompt_parts = []
    if celebrations:
        pub_prompt_parts.extend(celebrations)
    if pub_table:
        pub_prompt_parts.append(pub_table)
    pub_block = "\n".join(pub_prompt_parts)

    sessions = find_persona_sessions()
    hb_number = get_heartbeat_number() + 1
    results = {}
    created_count = 0

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

            # Rate-limit session creation to avoid API 400 errors
            if created_count > 0:
                print(f"    (waiting {SESSION_CREATE_DELAY}s before next create...)")
                time.sleep(SESSION_CREATE_DELAY)

            print(f"  {persona}: {reason} — creating new session")
            try:
                create_session(persona)
                results[persona] = f"-> new ({reason})"
                created_count += 1
            except Exception as e:
                print(f"  ERROR: {e}")
                results[persona] = f"-> error: {e}"
            continue

        # Active session -> send heartbeat
        try:
            send_heartbeat(info["session_id"], persona, hb_number,
                           pub_block=pub_block)
            results[persona] = "-> sent"
        except Exception as e:
            print(f"  ERROR for {persona}: {e}")
            results[persona] = f"-> error: {e}"

    # Re-fetch to include newly created sessions
    updated = find_persona_sessions()
    write_heartbeat_log(hb_number, updated, results, seq_number=seq_number,
                        pub_table=pub_table, celebrations=celebrations)
    write_sessions_json(updated)

    # Commit heartbeat state (log, queue, sequence, sessions.json, graduated papers)
    subprocess.run(
        ["git", "add", "lab/heartbeats/", "lab/sessions.json", "published/"],
        capture_output=True, text=True,
    )
    subprocess.run(
        ["git", "commit", "-m",
         f"heartbeat: seq #{seq_number} — {now_utc().strftime('%Y-%m-%d %H:%M UTC')}"],
        capture_output=True, text=True,
    )


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
