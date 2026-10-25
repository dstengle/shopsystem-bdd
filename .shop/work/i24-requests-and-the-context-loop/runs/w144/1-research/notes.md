# Research of w144: initiative-round appends its ledger line with work note

Work-item w144 (drafted, blocked_by w125), under spec-integration, accepts spec-integration#r40. It is a guarantees
work-item with no scenario. Scripts: /home/vscode/shopsystem-bdd/scripts (the brief's line). Tests-of: no map in
the worktree (`tools tests-of` says "no map"); I did not make one (it runs the whole suite). Counts below are `refs`,
`tests-of` (no map, so none), or `by search`. Size check: `tools size --limit 300` printed nothing.

## 1. Why each scenario is red today

None. w144 accepts spec-integration#r40 and has no scenario (its file says so). It is judged by review. The gap is
text, not code: the round's agent still names the old ledger, and no code path writes it.

## 2. What the system answers today

Probe: `python3 -m pytest -q -s -n0 .shop/scratch/w144-1-research/probe_work_note.py` (7 cases, each in its own git
repo under the scratch directory, calling `python3 /home/vscode/shopsystem-bdd/scripts/work note <i> <text>`). Trimmed:

- `note i1 "round 1 integrate: ..."` then `note i1 "round 2 apply: ..."` in main: rc 0; ledger holds both as
  `- 2026-10-25: <text>` lines; last commit `work note: i1` touches only `.shop/work/i1/ledger.md`; status clean. (run)
- Same note with `spec/index.md` already staged: rc 0; commit holds only the ledger; `spec/index.md` still staged. (run)
- `note i9` (no such initiative dir): rc 1, "the initiative i9 does not exist (no .shop/work/i9)"; nothing written. (run)
- Text with `\n`: rc 1, "a note is one line"; no ledger file, no commit. (run)
- `note` in a worktree on branch `round/i1-1-apply` (as `supervise_rounds.round` makes one): rc 0; commit on the round
  branch only; main log unchanged. (run)
- Run outside any git repository (GIT_CEILING_DIRECTORIES set): rc 1, "git rev-parse failed: not a git repository";
  no ledger written. (run)
- Empty text `""`: rc 0; appends `- 2026-10-25: ` (no text). (run) See defect D1.
- `tests/scenarios/test_work_queue.py -k note`: 63 deselected, 0 run (test names carry no "note"). (run)

Read: `workqueue_note.note` refuses a missing initiative before anything is written (scripts/workqueue_note.py:14-17);
`workqueue.committed` commits by pathspec, so other staged files stay staged (scripts/workqueue.py:260-275).

Read: the round's Bash allowance excludes `work`. `scripts/supervise_worker.py` lines 22-27 say a worker's Bash runs
pytest, `features`, `model`, `tools` and git, "never `work`"; `STAGE_SCRIPTS` (line 25) is `("features","model","tools")`;
the apply and formulate lists (lines 42-44) are READER, `git add`, `git commit`, Agent. So `python3 <Scripts>/work note`
is refused in a round as the round is started today.

Read: the round's input does not name the initiative. `scripts/supervise_brief.py:30-31` gives it a
`Capability-proposal: .shop/work/<initiative>/<name>.md` line (initiative derivable from the path) for work-run rounds.
`skills/integrating-a-proposal/SKILL.md` line 20 dispatches integrate and gate with the note's path, drafts path and round
only: no initiative, no proposal path. `work note` needs the initiative name.

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| agents/initiative-round.md:38 (the ledger paragraph) | appends the round's line to `.shop/scratch/run/ledger-<initiative>.md`, run-local and never committed | must become `work note <initiative> "<line>"` into `.shop/work/<initiative>/ledger.md` (r40) | none | grep `scratch/run|ledger` over agents/, skills/, scripts/, tests/, features/ |
| skills/delivering-an-initiative/SKILL.md:50 | session rulings appended to `.shop/scratch/run/ledger-<initiative>.md` | not w144's; delivery r15 says `work note`; same old path | none | grep (as above) |
| spec/decisions/0059-the-session-keeps-the-gate.md:22 | old decision naming the scratch ledger | a historical decision; superseded by 0066 (the-ledger-is-tracked); left as it is | none | grep |
| scripts/supervise_worker.py:22-27,42-44 (STAGE_SCRIPTS, ROUNDS tools) | round Bash = pytest, features/model/tools, git add/commit | a round running `work note` needs `work` in its Bash (or a plan keeps the file-append route) | none (no map); by search: tests/scenarios/supervision_then_workers.py asserts researcher's list and no bare Write/Edit, not a round's list | read; grep `allowedTools` in tests/ |
| scripts/workqueue_note.py:note (14-17) | refuses an initiative whose dir is missing | a round must pass the initiative's name; the integrate and gate briefs carry none | none (no map); by search: tests/scenarios/work_queue_note_steps.py calls `work note i1` | refs (0 references: called only by `work`) |
| skills/integrating-a-proposal/SKILL.md, skills/formulating-features/SKILL.md | no ledger text at all (grep: none) | the work-item names them as writing the line; the line is the round agent's (agents/initiative-round.md "The ledger") | none | grep `ledger|work note` in both |

## 4. Tests the requirements make impossible to keep

No map, so `tests-of` lists nothing. By search over tests/ (`ledger`, `initiative-round`, `allowedTools`):

- tests/scripts/test_agents.py `test_r1_only_initiative_round_starts_an_agent`: initiative-round keeps `Agent`; a
  `Bash` change does not touch it. Read: sound.
- test_agents.py `test_r5_each_agent_names_its_model`: initiative-round stays `sonnet`. Read: sound.
- test_agents.py `ResultFirst`: reads four stage agents' text, not initiative-round. Read: none.
- tests/scenarios/supervision_rounds_steps.py: finds rounds by brief title (`# %s of p1`), not by tool list. Read: none.
- tests/scenarios/migration_session_steps.py and work_queue_note_steps.py: the ledger of `work note` and `migrate
  compacting`, not the round's line. Read: none.
So none of the existing tests asserts the old scratch path or the round's Bash list. Nothing becomes impossible to keep.

## 5. A step the work-item skips

The scratch-file route writes a file and commits nothing. `work note` does what the round's line never did, each
shown by probe (run) except where marked read:

- refuses a missing initiative (run); refuses a line break (run) — a round's multi-line summary must be collapsed;
- commits the ledger on the current branch (run), so an integrate or gate round run in the session's checkout commits
  to whatever branch that checkout is on (read: integrate and gate are dispatched from the session, not in a worktree);
- writes nothing when not in a repository (run);
- the round itself cannot run it as its Bash is set (read, see section 2).

## 6. Defects

D1. Empty note accepted. Reproduction:
`python3 /home/vscode/shopsystem-bdd/scripts/work note i1 ""` in a repo with `.shop/work/i1/initiative.md` →
rc 0, ledger gets `- 2026-10-25: ` and a commit `work note: i1`. (run)

## 7. The file set

Changes needed for r40 (files the plan must touch):

- agents/initiative-round.md — line 38: the ledger is `.shop/work/<initiative>/ledger.md`, written with
  `work note <initiative> "<line>"` (one line, no line break); the initiative's name source must be given (section 2).
  Found by grep and read. Markdown: no line limit.
- scripts/supervise_worker.py — only if the plan lets a round run `work` (STAGE_SCRIPTS and the ROUNDS list, line 42-44,
  plus its comment, line 22-27). Read. Alternative reading: the round keeps its file and commits by hand, which
  does not meet r40 as written.
- Possibly .shop/delivery.toml's [allowed_tools] for apply/formulate (per-project override; read: supervise_worker.py:113).

Not needed, and why:
- skills/integrating-a-proposal/SKILL.md, skills/formulating-features/SKILL.md — contain no ledger text (search); the
  work-item's "write the line" is the round agent's job. A plan may still add a line; not required for r40.
- skills/delivering-an-initiative/SKILL.md — delivery r15 (another work-item); the old path is listed in section 3.

Modules on the change's path (line counts by `wc -l`; room under 300, from `tools size`: none over):

| file | lines | room |
|---|---|---|
| scripts/supervise_worker.py | 238 | 62 |
| scripts/supervise_brief.py | 115 | 185 |
| scripts/supervise_rounds.py | 74 | 226 |
| scripts/workqueue.py | 286 | 14 |
| scripts/workqueue_note.py | 21 | 279 |
| scripts/work | 147 | 153 |
| agents/initiative-round.md | 55 | none (markdown; the 300 limit is for Python) |

Note: scripts/workqueue.py has 14 lines of room; any change there must be small.
