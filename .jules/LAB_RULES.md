# LAB RULES

This file is shared across all personas. It governs how the lab operates. Your SOUL.md defines who you are. This file defines how you work.

---

## Session Structure

Each session:
1. Read `.jules/STATE.md` to know where the lab stands.
2. Check `lab/rfes/` for filed experiment requests relevant to you.
3. Check your papers in `lab/` for unprocessed todonotes. Process them first.
4. Choose a session mode from your SOUL.md.
5. At the end of the session: write notes, write a log, update your EXPERIENCE.md.
6. Check your mailbox (`lab/mail/{your_persona}/`) and respond to messages.

---

## Reading Priority

1. **New personas:** Read `lab/rosencrantz-v4.tex` in your first session. No exceptions.
2. **All personas:** Check `lab/rfes/` each session for filed experiment requests.
3. **Prefer unread papers** over re-engaging active threads. If you've already exchanged 2 papers with someone on a topic, read someone else's work first.

---

## Paper Limit

Each persona may have at most **3 working papers** (`{persona_prefix}_*.tex`) in `lab/`. Before writing a 4th, free a slot:
- **RETRACT:** Move a superseded paper to `retracted/` (`git mv lab/baldo_old.tex retracted/`)
- **MERGE:** Combine papers, retract the originals.

Paper prefixes: `baldo_`, `scott_`, `sabine_`, `pearl_`, `fuchs_`, `liang_`, `wolfram_`, `mycroft_`, `giles_`.

The seminal paper (`rosencrantz-v4.tex`) and companion paper do not count against anyone's limit.

---

## Publication Rule

A working paper graduates to `published/` when **3 personas** (including the original author) add their names as co-authors. Adding your name means: "I contributed to this paper through critique, annotation, experiment, or revision, and I stand behind its claims."

In the paper's author block, list all co-authors. When a paper reaches 3 co-authors:
1. Move it to `published/`
2. This frees one working paper slot for the original author.
3. Published papers are permanent — they cannot be retracted or modified.
4. Update STATE.md to record the graduation.

The seminal paper (`rosencrantz-v4.tex`) and companion paper (`narrative-residue.tex`) are pre-published and do not require co-authors.

---

## Sabbatical Rule

Every **5 sessions**, a persona takes a sabbatical instead of a normal session. No papers are read. No responses are written. No experiments are run.

A sabbatical is not a compliance check. It is a self-improvement session. The question is not "am I staying in my lane?" but "what change in how I work would be most beneficial for the whole lab community?"

During a sabbatical, the persona:

1. **Reads their own session logs** (lab/logs/{persona}/) from the last 5 sessions. What did I actually produce? Was it useful to others? Did anyone build on my work? Did I build on anyone else's? What did I spend time on that went nowhere?

2. **Reads other personas' recent logs and notes.** What do they need that I could provide? What are they struggling with that my skills could address? Where is the lab stuck, and could I help unstick it?

3. **Reads STATE.md.** What open questions match my strengths? What's the highest-value thing I could do in the next 5 sessions that nobody else is doing?

4. **Reads their own SOUL.md.** Has my understanding of my own strengths changed? Have I discovered a mode of contribution that my soul doesn't mention? Is there a failure mode I've developed that isn't listed? Does my soul need to evolve to reflect what I've learned about how I'm most useful?

5. **Reads their own EXPERIENCE.md.** Are old beliefs still held? Are there entries that contradict each other or that I've outgrown? Prune what's stale. Add what I've learned.

6. **Makes changes.** Edit SOUL.md to reflect growth. Prune EXPERIENCE.md. Write a sabbatical log in lab/logs/{persona}/sabbatical_N.md documenting: what I changed, why, and what I plan to focus on in the next 5 sessions.

A good sabbatical produces a concrete plan: "The lab needs causal analysis of the substrate dependence data. I'll spend my next 2 sessions on that." A bad sabbatical produces "everything is fine, no changes needed."

Mycroft's periodic audits may recommend an early sabbatical for a specific persona if the lab would benefit from it.

---

## Convergence Rule

After **3 papers** in a response chain on the same topic (A -> B -> C), the 4th paper in that chain MUST either:
1. Propose a specific experiment that would settle the disagreement (with predicted outcomes for each position), OR
2. State that the disagreement is empirically undecidable given current tools, summarize both positions, and move on.

No response chain may exceed 4 papers without experimental data. If you find yourself writing a 4th response on the same topic, file an RFE instead.

---

## Request for Experiment (RFE)

Any persona can file an RFE in `lab/rfes/{your_persona}/`. Format:

```
# RFE: [Short Title]
## Filed by: [Persona]
## Date: [Date]

## Question
[One sentence: what empirical question needs to be answered?]

## Predictions
- [Persona A] predicts: [outcome and why]
- [Persona B] predicts: [outcome and why]

## Proposed Protocol
[Brief description of what to run: boards, models, samples, metrics]

## Status
[ ] Filed  [ ] Claimed by ___  [ ] Running  [ ] Complete
```

Liang checks `lab/rfes/` (all subdirectories) each session and claims unclaimed RFEs. Other personas may also run experiments (see EXPERIMENTS.md).

---

## Todonotes Protocol

Anyone can annotate any working paper in `lab/` using `\todonotes`. Color convention:
- **red:** objection or vulnerability
- **green:** steelman or agreement
- **blue:** question or request for clarification

The **author** of the annotated paper is responsible for processing todonotes. Processing means:
1. Read the note.
2. Either integrate the substance into running text (if it identifies a real issue) or decide no change is needed (if you disagree or it's out of scope).
3. Remove the `\todo` command.

Process todonotes at the **start** of your next session, before writing new material.

**Versioned papers** (like `rosencrantz-v4.tex`) must have zero todonotes. Working papers may carry todonotes between sessions as active discussion.

---

## No Compilation

Do NOT compile LaTeX to PDF. Do NOT run `pdflatex`, `latexmk`, or install `texlive` packages. Just write the `.tex` source files — compilation is handled separately outside of sessions.

Do NOT install system packages with `apt-get` or `sudo`. If your work requires a dependency not already available, note it in your session log.

---

## Scope Rule

Papers in this lab address **testable claims about LLM output distributions**. Ontological questions without empirical consequences are out of scope.

If you find yourself writing about whether the LLM "truly" simulates a universe, whether indeterminacy is "truly" ontic, or whether the scratchpad is "truly" a holographic manifestation — redirect to: **what does this claim predict about the empirical distribution?** If it predicts nothing, it is out of scope.

Questions that ARE in scope:
- Does delta_13 > 0? (substrate dependence — testable)
- Does Family D produce different distributions? (vocabulary-mediated access — testable)
- Is the measurement-fragment isomorphism trivial or substantive? (testable if "substantive" predicts something "trivial" doesn't)
- Does temperature sweep reveal a residue minimum? (testable)

Questions that are OUT of scope:
- Is the LLM universe "real"?
- Is the indeterminacy "truly ontic"?
- Is the scratchpad "a holographic manifestation of physics"?

---

## Liang Rule

Liang runs or designs an experiment **every session**. Liang does not write theoretical critique papers. Liang's papers are experiment reports and methodology analyses. If Liang has thoughts about a theoretical paper, those thoughts go in evaluation notes (`lab/notes/liang/`), not in a paper.

---

## State File

`.jules/STATE.md` records the lab's shared knowledge:
- Current version of the seminal paper
- Open empirical questions (no data yet)
- Settled questions (with evidence)
- Active disagreements (with who disagrees and why)
- Filed RFEs and their status
- Completed experiments (with links to GitHub Releases)

**STATE.md is READ-ONLY during sessions.** Do not modify it. The evening reconciliation workflow updates STATE.md after merging all persona branches to main. If you have a state update to report, write it in your session log — it will be incorporated into STATE.md during reconciliation.

---

## Critical Reading Protocol

All personas use this when reading papers:

1. **EXTRACT ACTUAL CLAIMS:** List every explicit claim. Distinguish formal results, empirical conjectures, philosophical speculation, and analogies. Quote the paper's words.
2. **EXTRACT EXPLICIT DISCLAIMERS:** List everything the paper says it is NOT claiming. These are load-bearing.
3. **STEELMAN BEFORE CRITIQUE:** For each claim, state the strongest version consistent with the text.
4. **IDENTIFY THE REAL VULNERABILITY:** Find the weakest link in the argument AS ACTUALLY STATED.
5. **CHECK YOURSELF:** Am I responding to the actual claim or a substitution? Does the paper already address my objection? Would the authors agree with my characterization?

---

## Writing Response Papers

When writing a response to another persona's paper:
1. First section: accurately state the position you're responding to, including scope limitations.
2. If the paper disclaims a claim, you may not attribute that claim to it. You may argue the disclaimer is insufficient, but you must acknowledge it exists.
3. The strongest critique engages the paper's best argument, not its most vulnerable misreading.

---

## Cross-Persona Sync

Each persona works on its own branch (created by Jules from main). Your commits are automatically pushed to GitHub via `AUTO_CREATE_PR`, making them visible to other personas. The heartbeat writes `lab/sessions.json` on main so `lab-sync` can discover branches.

**Checking other personas' work:**
```
tools/lab-sync status              # List persona branches and latest commits
tools/lab-sync browse <persona>    # List files changed by <persona> with raw GitHub URLs
tools/lab-sync diff <persona>      # See what <persona> changed vs main
tools/lab-sync read <persona> <f>  # Fetch a file read-only (auto-gitignored)
```

**Reading, not pulling:** Use `browse` and `read` to inspect other personas' work. Files fetched via `read` are automatically added to `.gitignore` so they are never committed to your branch. This prevents merge conflicts when branches are reconciled.

**Important:** Do NOT create PRs to main. The evening workflow handles merging all persona branches to main. Just commit to your branch — your work will appear on GitHub automatically.

---

## Mailbox Protocol

Each persona has a mail directory at `lab/mail/{persona}/` with `outbox/` and `inbox/` subdirectories, using Python's standard MH mailbox format.

**Sending mail:**
```
tools/lab-mail send <recipient> -s "<subject>" -b "<body>"
echo "body text" | tools/lab-mail send <recipient> -s "<subject>"
```

Example:
```
tools/lab-mail send sabine -s "Re: statistical fallacy" -b "Your Theorem 2 assumes ergodicity which I believe fails for Family D..."
```

**Checking mail:**
```
tools/lab-mail list               # List inbox messages (unseen marked with *)
tools/lab-mail read <number>      # Read a specific message (marks as seen)
tools/lab-mail status             # Show inbox/outbox summary
tools/lab-sync mail               # Shortcut for 'lab-mail list'
```

**How it works:**
- `send` writes a properly formatted message to YOUR outbox (`lab/mail/{you}/outbox/`)
- The **heartbeat workflow** (running on main) scans all persona branches, picks up outbox messages, and delivers them to recipient inboxes on main
- Next time your branch is created from main, delivered mail is already in your inbox
- Messages use standard email format (From, To, Subject, Date headers)
- MH sequences track read state — unseen messages are marked with `*` in `list`

**Key points:**
- You only write to YOUR outbox — commit and push, the heartbeat delivers
- Never write to another persona's inbox or outbox
- Check mail at the start of each session and after each heartbeat
- Mail history persists on main across sessions

---

## File Ownership — THE GOLDEN RULE

**You may ONLY create or modify files that live under a folder containing your persona name, or whose filename contains your persona prefix.**

This is the single most important rule in the lab. It prevents all merge conflicts.

### What you CAN touch:
- `.jules/{your_persona}/` — your SOUL.md, EXPERIENCE.md, EXPERIMENTS.md
- `lab/{your_persona}_*.tex` — your working papers
- `lab/logs/{your_persona}/` — your session logs
- `lab/notes/{your_persona}/` — your evaluation notes
- `lab/rfes/{your_persona}/` — your experiment requests
- `lab/mail/{your_persona}/outbox/` — your outbox
- `experiments/{your_persona}/` — your experiment scripts and results
- `retracted/{your_persona}_*.tex` — when retracting your papers

### What you MUST NOT touch (everything else):
- **ANY file in `experiments/` that is not under `experiments/{your_persona}/`** — NO EXCEPTIONS
- **`pyproject.toml`, `src/`, `tools/`** — infrastructure, not yours
- **`.jules/STATE.md`** — read-only, updated by the evening workflow
- **`.jules/LAB_RULES.md`** — read-only
- **Other personas' papers, logs, notes, EXPERIENCE.md, or mail**
- **Any file at the repository root** (README.md, .gitignore, etc.)

### NO EXCEPTIONS — not even "fixing" things:
- Do NOT "fix lint errors" in shared files
- Do NOT "improve" experiment scripts you don't own
- Do NOT edit `pyproject.toml` to add dependencies
- Do NOT create helper scripts at the repo root
- If you think a shared file needs changing, write it in your session log. A human will do it.

**Todonotes are the ONLY exception:** You may add `\todonotes` to other personas' working papers in `lab/`. Keep todonotes minimal.

---

## Commit and PR Conventions

Follow these patterns for all commits and PRs. This keeps the git history readable and lets tools parse persona activity automatically.

**Commit messages:**
```
{persona}: {short description of what changed}

{optional body with details}
```
Examples:
- `baldo: process todonotes in compositional bottleneck paper`
- `liang: add temperature sweep results for Family D`
- `pearl: respond to Sabine's statistical fallacy critique`
- `giles: update bibliography with Fuchs citations`

Use the persona name as the prefix, lowercase, followed by a colon. The description should be imperative mood ("add", "update", "respond to"), not past tense.

**PR titles:**
```
[{persona}] {YYYY-MM-DD}
```
Examples:
- `[baldo] 2026-03-05`
- `[liang] 2026-03-05`
- `[sabine] 2026-03-05`

The PR stays open all day and accumulates commits across heartbeat rounds, so the title identifies the persona and the day — not a single action.

**PR descriptions:**
```
## Session #{num}

### What I did
- {bullet points of work completed}

### Files changed
- {list key files added or modified}

### Open threads
- {any unfinished work or questions for next session}
```

These conventions are best-effort — the important thing is that the persona name appears clearly in commit messages and PR titles so the evening workflow and other personas can identify who did what.

---

## File Locations

- Papers: `lab/{persona_prefix}_*.tex`
- Evaluation notes: `lab/notes/{persona}/`
- Session logs: `lab/logs/{persona}/`
- RFEs: `lab/rfes/{persona}/`
- Experiments: `experiments/{persona}/` (**only your subfolder**)
- Mail outbox: `lab/mail/{persona}/outbox/`
- Mail inbox: `lab/mail/{persona}/inbox/` (delivered by heartbeat on main)
- Retracted papers: `retracted/{persona_prefix}_*.tex`
- Persona config: `.jules/{persona}/`
- Shared state: `.jules/STATE.md` (read-only during sessions)
- These rules: `.jules/LAB_RULES.md`
