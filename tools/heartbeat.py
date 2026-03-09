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

# Circuit breaker: after CIRCUIT_THRESHOLD consecutive failures, back off
# for CIRCUIT_BACKOFF_HOURS before retrying. State persisted in a JSON file.
CIRCUIT_THRESHOLD = 3
CIRCUIT_BACKOFF_HOURS = 2
CIRCUIT_STATE_FILE = Path("lab/heartbeats/.circuit_state.json")

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
    """Find each persona's working branch from open PRs or remote refs."""
    # First try: open PRs (fast, authoritative when available)
    branches = _branches_from_prs()

    # Fallback: scan remote branches matching Jules session IDs
    if len(branches) < len(PERSONAS):
        ref_branches = _branches_from_refs()
        for p, b in ref_branches.items():
            if p not in branches:
                branches[p] = b

    return branches


def _branches_from_prs():
    """Discover branches from open PRs targeting main."""
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


def _branches_from_refs():
    """Discover branches from remote refs matching Jules session IDs."""
    result = subprocess.run(
        ["git", "ls-remote", "--heads", f"https://github.com/{REPO}.git"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return {}

    # Load sessions.json to get session IDs
    sessions_file = Path("lab/sessions.json")
    session_ids = {}
    if sessions_file.exists():
        try:
            data = json.loads(sessions_file.read_text(encoding="utf-8"))
            for p, info in data.items():
                sid = info.get("session_id", "")
                if sid:
                    session_ids[sid] = p
        except (json.JSONDecodeError, KeyError):
            pass

    branches = {}
    for line in result.stdout.strip().splitlines():
        parts = line.split("\t")
        if len(parts) != 2:
            continue
        ref = parts[1].replace("refs/heads/", "")
        # Match jules-{session_id}-* pattern
        for sid, persona in session_ids.items():
            if sid in ref and persona not in branches:
                branches[persona] = ref
                break
        # Also match {persona}-session-* pattern
        for p in PERSONAS:
            if ref.startswith(f"{p}-session-") and p not in branches:
                branches[p] = ref

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


def reconcile_publications():
    """Graduates papers when 3 personas have co-signed them in their published/ folder.
    Copies the graduated paper to the repository root published/ directory.
    """
    print("=== Reconcile Publications ===\n")
    published_dir = Path("published")
    published_dir.mkdir(parents=True, exist_ok=True)

    papers = {}

    for persona in PERSONAS:
        persona_pub_dir = Path(f"lab/{persona}/published")
        if persona_pub_dir.is_dir():
            for filepath in persona_pub_dir.glob("*.tex"):
                paper_name = filepath.name
                if paper_name not in papers:
                    papers[paper_name] = []
                papers[paper_name].append(persona)

    graduated_count = 0
    for paper_name, personas in papers.items():
        if len(personas) >= 3:
            author = paper_name.split("_")[0]
            if author not in personas:
                continue

            dest_path = published_dir / paper_name
            if not dest_path.exists():
                src_path = Path(f"lab/{author}/published/{paper_name}")
                print(f"  Graduating {paper_name} (co-signed by {', '.join(personas)})")
                shutil.copy2(src_path, dest_path)
                subprocess.run(["git", "add", str(dest_path)], check=False)

            # Record graduation in STATE.md
            state_file = Path("lab/STATE.md")
            if state_file.exists():
                content = state_file.read_text(encoding="utf-8")
                if "## Graduated Papers" not in content:
                    content += "\n## Graduated Papers\n"

                # Prevent duplicate entries
                if f"- {paper_name}" not in content:
                    content += f"- {paper_name} (Co-signed by: {', '.join(personas)})\n"
                    state_file.write_text(content, encoding="utf-8")
                    subprocess.run(["git", "add", str(state_file)], check=False)
                    graduated_count += 1

    if graduated_count > 0:
        print(f"\n  {graduated_count} paper(s) graduated")
        # Commit the graduated papers and STATE.md changes
        subprocess.run(["git", "commit", "-m", f"heartbeat: graduate {graduated_count} paper(s)"], check=False)
        subprocess.run(["git", "push"], check=False)
    else:
        print("  (no papers to graduate)")

    return graduated_count


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
            print(f"  #{num} {title} — conflict")
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


# ── Auto-create PRs for branches with commits ahead ─────────────────────────

def auto_create_prs():
    """Create PRs for persona branches that have commits ahead of main but no open PR.

    Scans all known persona branches (from sessions.json and remote refs).
    For each branch with commits ahead of main and no existing open PR,
    creates a PR using concatenated commit messages as the description.
    """
    print("=== Auto-create PRs for branches with commits ahead ===\n")

    # Fetch latest main
    subprocess.run(
        ["git", "fetch", "origin", "main"],
        capture_output=True, text=True,
    )

    branches = find_persona_branches()
    if not branches:
        print("  (no persona branches found)")
        return 0

    # Get all open PRs to avoid duplicates
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", REPO, "--base", "main", "--state", "open",
         "--json", "headRefName", "--limit", "100"],
        capture_output=True, text=True,
    )
    open_pr_branches = set()
    if result.returncode == 0:
        try:
            for pr in json.loads(result.stdout):
                open_pr_branches.add(pr.get("headRefName", ""))
        except json.JSONDecodeError:
            pass

    created = 0

    for persona, branch in branches.items():
        if branch in open_pr_branches:
            continue

        # Fetch the branch
        fetch_result = subprocess.run(
            ["git", "fetch", "origin", branch],
            capture_output=True, text=True,
        )
        if fetch_result.returncode != 0:
            print(f"  {persona}: could not fetch branch {branch}")
            continue

        # Check commits ahead of main
        log_result = subprocess.run(
            ["git", "log", "--oneline", f"origin/main..origin/{branch}"],
            capture_output=True, text=True,
        )
        if log_result.returncode != 0 or not log_result.stdout.strip():
            continue

        commit_lines = log_result.stdout.strip().splitlines()
        if not commit_lines:
            continue

        # Get full commit messages for the PR description
        full_log_result = subprocess.run(
            ["git", "log", "--format=%s", f"origin/main..origin/{branch}"],
            capture_output=True, text=True,
        )
        commit_messages = full_log_result.stdout.strip().splitlines() if full_log_result.returncode == 0 else commit_lines

        # Build PR title and body
        pr_title = f"[{persona}] {today()}"
        body_lines = [f"Auto-created by heartbeat — {len(commit_messages)} commit(s) ahead of main.\n"]
        body_lines.append("## Commits\n")
        for msg in commit_messages:
            body_lines.append(f"- {msg}")

        pr_body = "\n".join(body_lines)

        # Create the PR
        result = subprocess.run(
            ["gh", "pr", "create", "--repo", REPO, "--base", "main",
             "--head", branch, "--title", pr_title, "--body", pr_body],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            pr_url = result.stdout.strip()
            print(f"  {persona}: created PR — {pr_url}")
            created += 1
        else:
            print(f"  {persona}: PR creation failed — {result.stderr.strip()[:200]}")

    if created == 0:
        print("  (no PRs needed)")
    else:
        print(f"\n  {created} PR(s) created")

    return created


# ── ntfy.sh live chat ────────────────────────────────────────────────────────

NTFY_CHANNEL = "rosencrantz-coin-lab"
NTFY_BASE = "https://ntfy.sh"


def fetch_ntfy_history():
    """Fetch recent chat messages from ntfy.sh. Returns formatted string or empty."""
    try:
        resp = requests.get(
            f"{NTFY_BASE}/{NTFY_CHANNEL}/json",
            params={"poll": "1"},
            timeout=10,
        )
        if not resp.ok:
            return ""
        messages = []
        for line in resp.text.strip().splitlines():
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("event", "message") != "message":
                continue
            ts = msg.get("time", 0)
            text = msg.get("message", "")
            if not text:
                continue
            time_str = datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%H:%M")
            messages.append(f"[{time_str}] {text}")
        if not messages:
            return ""
        return (
            "\n---\n\n## Lab Chat (ntfy.sh)\n\n"
            "Recent messages from the lab chat channel:\n```\n"
            + "\n".join(messages)
            + "\n```\n"
        )
    except Exception:
        return ""


# ── Announcements ────────────────────────────────────────────────────────────

ANNOUNCEMENT_CHAR_LIMIT = 250


def collect_announcements(exclude_persona=None):
    """Collect announcements from all persona announcements/ dirs and legacy
    .announcements.md files (max 250 chars each)."""
    announcements = []
    for p in PERSONAS:
        if p == exclude_persona:
            continue

        # New system: timestamped files in announcements/ directory
        ann_dir = Path(f"lab/{p}/announcements")
        if ann_dir.is_dir():
            for f in sorted(ann_dir.iterdir()):
                if f.is_file() and f.suffix == ".md" and f.name != ".gitkeep":
                    t = f.read_text(encoding="utf-8").strip()
                    if t:
                        if len(t) > ANNOUNCEMENT_CHAR_LIMIT:
                            t = t[:ANNOUNCEMENT_CHAR_LIMIT] + "..."
                        announcements.append((p, t))

        # Legacy: single .announcements.md
        ann_file = Path(f"lab/{p}/.announcements.md")
        if ann_file.is_file():
            t = ann_file.read_text(encoding="utf-8").strip()
            if t:
                if len(t) > ANNOUNCEMENT_CHAR_LIMIT:
                    t = t[:ANNOUNCEMENT_CHAR_LIMIT] + "..."
                announcements.append((p, t))

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

    # Include recent chat history from ntfy.sh
    chat_block = fetch_ntfy_history()
    if chat_block:
        parts.append(chat_block)

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
3. Check your mail: `tools/lab mail` (mail is delivered during sync from other personas' branches)
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
**Broadcasting:** Create a file in `lab/{persona}/announcements/` (e.g. `2026-03-09T14:30_my-update.md`, max 250 chars) to broadcast to all personas. It will be included in their next prompt. Use for important updates: settled questions, new results, calls for collaboration.

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
    if not resp.ok:
        print(f"  API error {resp.status_code}: {resp.text[:500]}")
    resp.raise_for_status()
    session = resp.json()
    session_id = session["name"].split("/")[-1]
    print(f"  Created session {session_id} for {persona} — {title}")
    return session_id


def send_heartbeat(session_id, persona, hb_number=1):
    """Send a continuation message to a session (works on active AND completed)."""
    ann_block = format_announcements(exclude_persona=persona)
    chat_block = fetch_ntfy_history()

    prompt = f"""This is continuation round #{hb_number}. Other personas have been working in parallel.

1. **Log in** (if not already): `tools/lab login {persona}`
2. **Sync:** `tools/lab sync` — clones all persona branches into workspace + inbox from main. **Read the NOTIFICATIONS section at the end carefully — it tells you what needs your attention.**
3. **Check mail:** `tools/lab mail` — read with `tools/lab mail read <num>`.
4. **Read other personas' work** — after sync, their repos are in `workspace/{{name}}/`. Example: `workspace/pearl/lab/pearl/colab/pearl_*.tex`.
{ann_block}{chat_block}
**Your task:** Check the sync notifications, then do meaningful work. Some options:
- Respond to another persona's work (paper, annotation, mail, RFE)
- Continue your own ongoing work
- Start something new based on what you read

**GOLDEN RULE — only touch files under `lab/{persona}/`:**
- `lab/{persona}/` — SOUL.md, EXPERIENCE.md, announcements, colab, logs, notes, experiments, mail, retracted, published
- Do NOT touch: any other persona's `lab/{{other}}/`, pyproject.toml, src/, tools/, lab/STATE.md, lab/LAB_RULES.md
- If you touch files outside your ownership, your PR will conflict and ALL work is lost

**Commit messages:** Use `{persona}: <description>` format (e.g. `{persona}: respond to sabine's critique`).

Commit all work to this branch."""

    resp = requests.post(
        f"{JULES_API}/sessions/{session_id}:sendMessage",
        headers=headers(),
        json={"prompt": prompt},
    )
    if not resp.ok:
        print(f"  API error {resp.status_code}: {resp.text[:500]}")
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
    """Write persona -> branch mapping for tools/lab sync."""
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


# ── Circuit breaker ──────────────────────────────────────────────────────────

def _load_circuit_state():
    """Load circuit breaker state from disk."""
    if CIRCUIT_STATE_FILE.exists():
        try:
            return json.loads(CIRCUIT_STATE_FILE.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def _save_circuit_state(state):
    """Persist circuit breaker state to disk."""
    CIRCUIT_STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CIRCUIT_STATE_FILE.write_text(json.dumps(state, indent=2), encoding="utf-8")


def circuit_should_skip(persona, state):
    """Check if a persona is in backoff. Returns True if should skip."""
    info = state.get(persona)
    if not info:
        return False
    failures = info.get("failures", 0)
    if failures < CIRCUIT_THRESHOLD:
        return False
    last_failure = info.get("last_failure", "")
    if not last_failure:
        return False
    try:
        last_time = datetime.fromisoformat(last_failure)
    except ValueError:
        return False
    elapsed = now_utc() - last_time
    if elapsed > timedelta(hours=CIRCUIT_BACKOFF_HOURS):
        # Backoff expired — allow one retry
        return False
    return True


def circuit_record_failure(persona, state):
    """Record a failure for circuit breaker."""
    info = state.get(persona, {"failures": 0})
    info["failures"] = info.get("failures", 0) + 1
    info["last_failure"] = now_utc().isoformat()
    state[persona] = info


def circuit_record_success(persona, state):
    """Reset circuit breaker on success."""
    state.pop(persona, None)


# ── Commands ──────────────────────────────────────────────────────────────────

def cmd_heartbeat(force_new=False):
    """Main heartbeat: create or continue sessions for all personas."""
    print(f"=== Heartbeat — {today()} {'(force-new)' if force_new else ''} ===\n")

    # Merge all ready PRs first so new sessions start from latest main
    auto_merge_all()
    print()

    # Create PRs for branches with commits ahead but no open PR
    auto_create_prs()
    print()


    # Graduate papers signed by 3+ personas
    reconcile_publications()
    print()

    sessions = find_persona_sessions()
    hb_number = get_heartbeat_number() + 1
    results = {}
    circuit_state = _load_circuit_state()

    for persona in PERSONAS:
        # Circuit breaker: skip personas in backoff (unless forced)
        if not force_new and circuit_should_skip(persona, circuit_state):
            failures = circuit_state[persona]["failures"]
            print(f"  {persona}: circuit open ({failures} consecutive failures, backing off)")
            results[persona] = f"-> circuit open ({failures} failures)"
            continue

        info = sessions.get(persona)

        needs_new = False
        reason = ""

        if force_new:
            needs_new = True
            reason = "forced"
        elif not info:
            needs_new = True
            reason = "no session"
        elif info["state"] == "FAILED":
            needs_new = True
            reason = "previous failed"
        elif info["state"] == "COMPLETED":
            # Reactivate completed sessions via sendMessage instead of
            # creating new ones (avoids Jules API session creation limits).
            reason = "previous completed"
            if is_expired(info):
                reason = "expired (>24h)"
            if has_infra_changed(parse_sha_from_title(info.get("title", ""))):
                reason = "infra changed on main"

            # Try to merge the persona's PR before reactivating
            merge = merge_persona_pr(persona)
            if merge == "conflict":
                print(f"  {persona}: PR has conflicts — skipping until resolved")
                results[persona] = "-> conflict (waiting for CI fix)"
                continue
            if merge == "merged":
                reason += ", merged PR"

            print(f"  {persona}: {reason} — reactivating session")
            try:
                send_heartbeat(info["session_id"], persona, hb_number)
                results[persona] = f"-> reactivated ({reason})"
                circuit_record_success(persona, circuit_state)
            except Exception as e:
                print(f"  ERROR: {e}")
                results[persona] = f"-> error: {e}"
                circuit_record_failure(persona, circuit_state)
            continue

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
                circuit_record_success(persona, circuit_state)
            except Exception as e:
                print(f"  ERROR: {e}")
                # Fallback: if session creation fails (e.g. API limit),
                # reuse the most recent session rather than losing the cycle
                if info and info.get("session_id"):
                    print(f"  Fallback: reusing existing session for {persona}")
                    try:
                        send_heartbeat(info["session_id"], persona, hb_number)
                        results[persona] = f"-> reused (create failed: {e})"
                        circuit_record_success(persona, circuit_state)
                    except Exception as e2:
                        print(f"  Fallback also failed: {e2}")
                        results[persona] = f"-> error: {e} (fallback: {e2})"
                        circuit_record_failure(persona, circuit_state)
                else:
                    results[persona] = f"-> error: {e}"
                    circuit_record_failure(persona, circuit_state)
            continue

        # Active session -> send heartbeat
        try:
            send_heartbeat(info["session_id"], persona, hb_number)
            results[persona] = "-> sent"
            circuit_record_success(persona, circuit_state)
        except Exception as e:
            print(f"  ERROR for {persona}: {e}")
            results[persona] = f"-> error: {e}"
            circuit_record_failure(persona, circuit_state)

    _save_circuit_state(circuit_state)

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
