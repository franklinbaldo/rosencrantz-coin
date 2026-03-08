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


def is_sabbatical_pr(persona):
    """Check if a persona's open PR modifies their SOUL.md (sabbatical indicator).

    The core sabbatical mandate is to review and edit SOUL.md to reflect growth.
    Detecting SOUL.md changes is more robust than checking for sabbatical log
    filenames, since the soul edit is the universal sabbatical output.
    """
    pr_num = find_persona_pr(persona)
    if pr_num is None:
        return False
    result = subprocess.run(
        ["gh", "pr", "view", str(pr_num), "--repo", REPO,
         "--json", "files", "--jq", ".files[].path"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return False
    soul_path = f"lab/{persona}/SOUL.md"
    return soul_path in result.stdout.strip().splitlines()


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

        # gh pr view triggers GitHub to compute mergeable status.
        # First call often returns UNKNOWN; retry once after a short delay.
        mergeable = ""
        detail = {}
        for attempt in range(2):
            result = subprocess.run(
                ["gh", "pr", "view", str(num), "--repo", REPO,
                 "--json", "mergeable,statusCheckRollup"],
                capture_output=True, text=True,
            )
            if result.returncode != 0:
                break
            try:
                detail = json.loads(result.stdout)
            except json.JSONDecodeError:
                break
            mergeable = detail.get("mergeable", "")
            if mergeable != "UNKNOWN":
                break
            if attempt == 0:
                time.sleep(3)  # give GitHub time to compute

        if mergeable == "CONFLICTING":
            # Try to resolve conflicts by merging main into the PR branch.
            # Fetch the branch, merge main, and push — if it succeeds the PR
            # will become mergeable on the next heartbeat cycle.
            head_branch = pr.get("headRefName", "")
            if not head_branch:
                print(f"  #{num} {title} — conflict, no branch name, skipping")
                continue

            resolved = False
            try:
                subprocess.run(
                    ["git", "fetch", "origin", head_branch, "main"],
                    capture_output=True, text=True, check=True,
                )
                subprocess.run(
                    ["git", "checkout", head_branch],
                    capture_output=True, text=True, check=True,
                )
                merge_result = subprocess.run(
                    ["git", "merge", "origin/main", "-m",
                     f"Merge main into {head_branch} to resolve conflicts"],
                    capture_output=True, text=True,
                )
                if merge_result.returncode == 0:
                    push_result = subprocess.run(
                        ["git", "push", "origin", head_branch],
                        capture_output=True, text=True,
                    )
                    if push_result.returncode == 0:
                        resolved = True
                        print(f"  #{num} {title} — conflict resolved by merging main, will merge next cycle")
                    else:
                        print(f"  #{num} {title} — conflict resolved but push failed: {push_result.stderr.strip()[:100]}")
                else:
                    # Merge had conflicts that can't be auto-resolved — abort
                    subprocess.run(
                        ["git", "merge", "--abort"],
                        capture_output=True, text=True,
                    )
                    print(f"  #{num} {title} — conflict cannot be auto-resolved, skipping")
            except subprocess.CalledProcessError as e:
                print(f"  #{num} {title} — conflict resolution failed: {e}")
            finally:
                # Return to the original branch
                subprocess.run(
                    ["git", "checkout", "-"],
                    capture_output=True, text=True,
                )

            if not resolved:
                # Label for manual attention instead of closing
                subprocess.run(
                    ["gh", "pr", "edit", str(num), "--repo", REPO,
                     "--add-label", "needs-conflict-resolution"],
                    capture_output=True, text=True,
                )
            continue

        if mergeable not in ("MERGEABLE", "UNKNOWN"):
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


def create_prs_for_orphan_branches(sessions):
    """Find branches ahead of main that have no open PR and create one.

    Any remote branch that is ahead of main and lacks an open PR gets a PR
    created automatically.  The first commit message ahead of main is used
    as the PR title and description.  Auto-merge is enabled so it lands on
    main without manual intervention.
    """
    print("=== Check for orphan branches ===\n")

    # Collect current session IDs for optional persona detection
    session_ids = {}
    for persona, info in sessions.items():
        sid = info.get("session_id", "")
        if sid:
            session_ids[sid] = persona

    # List remote branches
    result = subprocess.run(
        ["git", "branch", "-r", "--list", "origin/*"],
        capture_output=True, text=True,
    )
    if result.returncode != 0:
        return

    remote_branches = [b.strip().removeprefix("origin/")
                       for b in result.stdout.splitlines()
                       if b.strip() and "HEAD" not in b]

    # List open PRs to know which branches already have one
    result = subprocess.run(
        ["gh", "pr", "list", "--repo", REPO, "--base", "main", "--state", "open",
         "--json", "headRefName", "--limit", "100"],
        capture_output=True, text=True,
    )
    pr_branches = set()
    if result.returncode == 0:
        try:
            pr_branches = {pr["headRefName"] for pr in json.loads(result.stdout)}
        except (json.JSONDecodeError, KeyError):
            pass

    created = 0
    for branch in remote_branches:
        if branch == "main":
            continue

        # Skip if a PR already exists for this branch
        if branch in pr_branches:
            continue

        # Check the branch has commits ahead of main
        diff_result = subprocess.run(
            ["git", "rev-list", "--count", f"origin/main..origin/{branch}"],
            capture_output=True, text=True,
        )
        if diff_result.returncode != 0:
            continue
        ahead = int(diff_result.stdout.strip() or "0")
        if ahead == 0:
            continue

        # Optionally detect persona from session ID in branch name
        matched_persona = None
        for sid, persona in session_ids.items():
            if sid in branch:
                matched_persona = persona
                break

        # Get the first commit message ahead of main (oldest divergent commit)
        log_result = subprocess.run(
            ["git", "log", "--reverse", "--format=%s%n%b",
             f"origin/main..origin/{branch}", "--max-count=1"],
            capture_output=True, text=True,
        )
        if log_result.returncode != 0 or not log_result.stdout.strip():
            title = f"[{matched_persona or branch}] {now_utc().strftime('%Y-%m-%d')}"
            body = f"Auto-created PR for branch {branch}."
        else:
            lines = log_result.stdout.strip().splitlines()
            title = lines[0].strip()
            body = "\n".join(lines[1:]).strip() or title

        # Create PR with auto-merge
        result = subprocess.run(
            ["gh", "pr", "create", "--repo", REPO, "--base", "main",
             "--head", branch, "--title", title, "--body", body],
            capture_output=True, text=True,
        )
        if result.returncode != 0:
            label = matched_persona or branch
            print(f"  {label}: failed to create PR for {branch}: "
                  f"{result.stderr.strip()[:100]}")
            continue

        pr_url = result.stdout.strip()
        label = matched_persona or branch
        print(f"  {label}: created PR {pr_url} for branch {branch}")

        # Enable auto-merge
        # Extract PR number from URL
        pr_num = pr_url.rstrip("/").split("/")[-1]
        subprocess.run(
            ["gh", "pr", "merge", pr_num, "--repo", REPO, "--merge", "--auto"],
            capture_output=True, text=True,
        )
        created += 1

    if created == 0:
        print("  (no orphan branches found)")
    else:
        print(f"\n  {created} PR(s) created")


# ── Announcements ────────────────────────────────────────────────────────────

NTFY_CHANNEL = "rosencrantz-coin-lab"
NTFY_BASE = "https://ntfy.sh"

ANNOUNCEMENT_CHAR_LIMIT = 250


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
        # LAB_RULES: "3 personas including the original author".
        # The author is implicit (they wrote the paper), so 2 co-signers = 3 total.
        threshold = 2 if info["author"] else 3
        if info["count"] >= threshold and paper not in queue:
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
                f"   Then move the paper to free your colab slot:\n"
                f"   git mv lab/{info['author']}/colab/{paper} lab/{info['author']}/approved/{paper}\n"
            )

    # Check for papers ready to graduate (grace period elapsed)
    for paper, entry in list(queue.items()):
        if entry["status"] == "polishing":
            elapsed = seq_number - entry["reached_3_at_seq"]
            if elapsed >= PUBLISH_GRACE_HEARTBEATS:
                # Auto-publish: find paper in author's folders and copy to published/ at root
                author = entry["author"]
                src = None
                for folder in ["approved", "colab", "retracted"]:
                    candidate = Path(f"lab/{author}/{folder}/{paper}")
                    if candidate.exists():
                        src = candidate
                        break
                dst = Path(f"published/{paper}")
                if src and not dst.exists():
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
                elif dst.exists():
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

    # Include recent chat history
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
- `lab/{persona}/` — everything under your persona folder (SOUL.md, EXPERIENCE.md, colab, logs, notes, experiments, mail, retracted, approved, published)

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

**Approving papers:** When a paper reaches 3 co-signs, move it from `colab/` to `lab/{persona}/approved/` to free a colab slot. The heartbeat will graduate it to `published/` at root after the grace period.
**Retracting papers:** Move to `lab/{persona}/retracted/` to abandon a paper and free a colab slot.
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
    chat_block = fetch_ntfy_history()

    prompt = f"""This is continuation round #{hb_number}. Other personas have been working in parallel.

1. **Log in** (if not already): `tools/lab login {persona}`
2. **Sync:** `tools/lab sync` — clones all persona branches into workspace + inbox from main. **Read the NOTIFICATIONS section at the end carefully — it tells you what needs your attention.**
3. **Check mail:** `tools/lab mail` — read with `tools/lab mail read <num>`.
4. **Read other personas' work** — after sync, their repos are in `workspace/{{name}}/`. Example: `workspace/pearl/lab/pearl/colab/pearl_*.tex`.
{ann_block}{chat_block}{pub_block}
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

    # Create PRs for branches that Jules pushed but didn't open a PR for
    subprocess.run(["git", "fetch", "origin", "--prune"], capture_output=True)
    create_prs_for_orphan_branches(sessions)
    print()

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
        elif info["state"] == "FAILED":
            needs_new = True
            reason = "previous failed"
        elif is_expired(info):
            needs_new = True
            reason = "expired (>24h)"
        elif has_infra_changed(parse_sha_from_title(info.get("title", ""))):
            needs_new = True
            reason = "infra changed on main"
        elif info["state"] == "COMPLETED" and is_sabbatical_pr(persona):
            needs_new = True
            reason = "sabbatical completed (early merge)"

        if needs_new:
            # Try to merge the persona's PR before creating a new session
            merge = merge_persona_pr(persona)
            if merge == "conflict":
                print(f"  {persona}: PR has conflicts — skipping until resolved")
                results[persona] = "-> conflict (waiting for CI fix)"
                continue

            if merge == "merged":
                reason += ", merged PR"

            # If there's an existing session (COMPLETED/expired/infra-changed),
            # try reactivating it via sendMessage first — this avoids hitting
            # the Jules API session-creation quota/precondition limits.
            if info and info["state"] != "FAILED":
                print(f"  {persona}: {reason} — reactivating via sendMessage")
                try:
                    send_heartbeat(info["session_id"], persona, hb_number,
                                   pub_block=pub_block)
                    results[persona] = f"-> reactivated ({reason})"
                    continue
                except Exception as e:
                    print(f"    reactivation failed ({e}), will create new session")

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
