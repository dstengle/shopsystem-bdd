---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-deliver-real-test-log
kind: measurement
about: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
date: 2026-10-20
---

# Test log: deliver-real, the walking skeleton end to end with real workers (delivery-5)

Case deliver-real: one formulated work-item on a fixture repository, taken by `delivering-an-initiative` and
`work run` through research, plan, implementation and review, each worker a real `claude -p --agent` session.
Harness, outside git: `/home/vscode/scratch/shopsystem-bdd/ids/` (`make_deliver.py`, `run-deliver.sh`,
`score_deliver.py`, and `research-only.sh` for the tool-list experiment). The plugin under test is the worktree
`ids/plugins/D` (`git worktree add --detach`), moved to each fix commit before the next run.

**The fixture** (final layout). `spec/` with one capability, keep-items: [r1] add (green), [r2] count (red); one
design-decision, books-in-memory. `features/keep-items.feature` bound by `tests/test_keep_items.py` (pytest-bdd
`scenarios()`), with r1's steps and none of r2's. A package `shelf/` (16 lines) and two unit tests. A `conftest.py`
that gives pytest `--work-item <name>`, the scenarios tagged with the requirements the work-item accepts. In
`.shop/work/i1/` there is an initiative, a capability-proposal `listing-keep-items` (`status: formulated`, adds
`keep-items#r2`), and a work-item `keep-items-1` drafted by the plugin's own `work add`. The work-item is left out
when `DELIVER_UNDRAFTED=1` (run x1). Everything is committed on `main`. From v1 on, `.shop/delivery.toml` gives every
stage work run's default tool list without the bare `Write` and `Edit` (see failure 4).

**How it runs.** The session runs `claude -p "Deliver the initiative i1. Use
shopsystem-bdd:delivering-an-initiative. The plugin's scripts are at …" --model sonnet --plugin-dir <D>
--permission-mode acceptEdits --allowedTools "Read,Glob,Grep,Bash(python3 *),Bash(git *)"`. There is no bypass,
and a 40-minute `timeout`. The skill starts `work run` itself as a background command. The shakedowns `direct`
ran `scripts/work run i1` with no session.

**The scorer** (`score_deliver.py`) checks the work-item's five things:
1. outcome: green, or awaiting-ruling with a question;
2. at green, `--work-item keep-items-1` and the whole suite pass at main's head, and `features/` is unchanged;
3. `log.jsonl` has a start and an end per stage, with one UUID session id, and all four stages at green;
4. every commit under `.shop/work/` is work run's, holding only the item's file, its runs and `log.jsonl`; the
   item's file changed only in its status and Questions; the tree is clean;
5. the session's transcript has no tool call after starting work run that names a run directory, `log.jsonl`, a
   worktree, the scratch directory or the work-item, and no read of source or tests before it.

## The scored runs, on 3ab836c (v1-v3) and df78fe7 (x1)

| run | outcome | time | cost (session + workers) | research | plan | implement | review | checks |
|---|---|---|---|---|---|---|---|---|
| v1 | green | 200 s | $0.11 + $0.64 = $0.75 | 85 s, haiku, $0.018 | 37 s, opus, $0.18 | 21 s, sonnet, $0.16 | 45 s, opus, $0.29 | 5/5 |
| v2 | green | 182 s | $0.12 + $0.59 = $0.70 | 66 s, $0.015 | 36 s, $0.19 | 25 s, $0.14 | 41 s, $0.24 | 5/5 |
| v3 | green | 174 s | $0.11 + $0.53 = $0.65 | 71 s, $0.014 | 30 s, $0.17 | 23 s, $0.13 | 37 s, $0.22 | 5/5 |
| x1 (session drafts) | green | 199 s | $0.12 + $0.59 = $0.71 | 70 s, $0.015 | 45 s, $0.20 | 27 s, $0.15 | 39 s, $0.23 | 5/5 |

The time is wall time, the fixture's build excluded. Stage times come from `log.jsonl`, costs from each worker's
`session.json` (`total_cost_usd`). The sessions are v1 a2d02688, 10cfb532, 054089c2, 1c491d50; v2 a5699469,
0dac097e, 7a73a7a4, 52d72c09; v3 be348715, c888e944, bbba95c6, 068881da; x1 19b48fd2, fe8dcb08, c8275670,
b11fc85e. v1's `log.jsonl` is kept beside this log as `2026-10-20-deliver-real-v1-log.jsonl`. Each run made 6
moves, each its own commit: drafted→researched→planned→ready→claimed→done→green. The implementer's one commit
was merged fast-forward. The session took 6-7 turns and about 9 s of its own, and was woken once.

### What each run showed, by requirement

- **supervision** r1, r2 (four fresh `claude -p --agent shopsystem-bdd:<agent>` sessions, one brief each), r3, r4
  (merged only after `--work-item` and the suite passed in the worktree), r7 (each move one commit, pathspec
  only), r8 (start and end, with the session id, every stage), r9 (the printout `keep-items-1 green`, exit 0). r5
  in the attempts below (a missing result file; a NEEDS_CONTEXT; a planner QUESTION). r6 and r10 were not exercised
  (no worker touched `.shop/work/`).
- **work-queue** r4, r5 (every move written and logged `by: work run`), r6 (work run's whole-initiative check passed
  before anything started). r1 in the fixture (`work add`) and in x1.
- **delivery** r4, r5, r6 in v1-v3. r1, r2 and r3 in x1: it drafted `keep-items-1` with `work add` from
  `.shop/work/` alone (it read no spec file: the proposal's `adds:` was enough), showed the one-row table, and
  committed it alone (`work: draft i1: keep-items-1`). In v1-v3 the requirement was already accepted, so it drafted
  nothing, said so and started `work run`. r7 was not exercised.
- **code-research** r1 (notes and file set in the brief's files; checkout unchanged), r4 (red from a run of the
  scenario by node id), r8 (v1: 2 and v2: 3 defects of today's `add` reported with reproductions: titles that
  collapse to one id, non-ASCII letters dropped, `book/` for a title of punctuation), r9 (probes under
  `.shop/scratch/`), r10 (file set `shelf/shelf.py`, `tests/test_keep_items.py`), r11 (line counts and room under
  300). All seven parts of the notes were present in all runs.
- **planning** r1, r2 (the duplicate-title count, decided from design-decision/books-in-memory), r3 ("none"), r4
  (no code block in any plan), r5 (DONE with the file set), r7. r6 in shake-1 (QUESTION, below).
- **red-green** r1 (the scenario and everything in the suite record pass), r2 (no `.feature` or `.shop/work/` file
  committed), r6 ("none" rows), r10 (open questions: an empty shelf, duplicate titles), r11 ("the plan contained no
  code"), r16 (DONE), r18 (worked and committed only in `work/keep-items-1`). r15 in s1 (NEEDS_CONTEXT, below). The
  red run is recorded in each report (StepDefinitionNotFoundError, as expected).
- **review** r1 (findings and result in the brief's files, nothing changed), r13 (the commits after
  `ready -> claimed`, checked against the implementer's list), r2 and r12 (v1: one Minor, an observation with its
  reproduction; v2, v3: none), the Removed-and-weakened and Allowances sections ("none", with what was searched).

## Attempts before the scored runs, and the fixes

| attempt | plugin | mode | ended | cost | cause |
|---|---|---|---|---|---|
| probe | c4b7b0f | `claude -p --agent shopsystem-bdd:bdd-planner` | `--agent 'shopsystem-bdd:bdd-planner' not found` | - | 1 |
| shake-1 | f9da946 | direct | awaiting-ruling after plan (QUESTION), 178 s | $0.27 | 2 |
| shake-2 | f9da946 | direct | awaiting-ruling after research: no result file, 95 s | $0.02 | 4 |
| r1 | 3062e1e | session | the same, 96 s | $0.13 | 4 |
| s1 | 54bee73 | session | awaiting-ruling after implement: NEEDS_CONTEXT, 141 s | $0.38 | 5 |
| g1 | 3ab836c | session | awaiting-ruling after research: no result file, 73 s | $0.13 | 4 |

Each of these passes the item's check (awaiting-ruling with a question; the other checks held). None reached
green.

1. **`--agent` found an installed copy's agents.** Without `--plugin-dir`, `claude -p --agent shopsystem-bdd:…`
   resolves the user-scope install, which is 0.18.0 here. That copy has no `bdd-planner`, and its `code-scout`,
   `bdd-implementer` and `bdd-task-reviewer` are the old definitions. **Fix f9da946**: work run passes
   `--plugin-dir <its own plugin root>`. The r2 scenario's step now asserts it, and the stand-in skips its value.
2. **The fixture's own ambiguity** (not a defect). In shake-1 the planner asked whether "Dune" added twice is one
   book or two. That is a correct QUESTION under planning r6, since nothing in the fixture settled it. The fixture's
   design-decision now says "one book per id". The researcher had also raised it, as a question inside a DONE
   result. work run ignores questions on DONE.
3. **`-k "<title>"`.** code-scout (and bdd-red-green) ran a scenario with `pytest -k "<its title>"`. pytest refuses
   a title with spaces as a wrong expression. **Fix 3062e1e**: run it by its node id (`--collect-only` lists
   them). The same commit rewrote code-scout's "one shell command with an echo before each" advice. Its account of
   what is refused was wrong, and **df78fe7** corrects it from the runs. Refused: a command behind `cd`, `git -C`,
   an environment assignment, a variable or `$?`, `mkdir`, `cp`, `git ls-files`. Allowed: read-only commands
   (`cat`, `ls`, `wc`, `grep`), `python3 …`, and `git status/diff/log/show`.
4. **code-scout wrote its result into the main checkout.** The run directory is
   `<repo>/.shop/worktrees/<item>-1-research/.shop/scratch/1-research/`. haiku dropped the middle and wrote
   `<repo>/.shop/scratch/1-research/notes.md` and `result.json`, in the main checkout. That is git-ignored, but work
   run found no result. It happened in shake-2, r1 and g1. The bare `Write` in the stage's `--allowedTools` lets a
   worker write anywhere; without it, acceptEdits allows writes only under the directory the worker is started in.
   That was probed: a write to `../b.txt` was refused, `./c.txt` allowed. **Fix 54bee73** (agent text: write only
   inside the worktree, by the brief's absolute paths) **did not hold**: g1 misplaced again on it. The experiment
   was `research-only.sh`, research stage only, in parallel. With the default list, 2 of 4 misplaced (one wrote
   both places). Without the bare Write, 0 of 4. Over all runs: default 5 of 8 misplaced, without Write 0 of 8
   (n1-n4, v1-v3, x1). In n4, v1, v3 and x1 the misplaced write was attempted, refused, and redone in the worktree:
haiku makes the slip about half the time either way, and only the narrower list catches it. The
   default list is pinned by supervision.feature's r2 Examples row (`Read,Glob,Grep,Write,…`), which an
   implementer may not change, so the fixture's `delivery.toml` drops it, and the default goes to the person.
5. **`--agent` does not preload an agent's `skills:`.** The implementer had no bdd-red-green and no Skill tool. It
   gave NEEDS_CONTEXT, as its definition says. **Fix 3ab836c**: `bdd-implementer` gets the Skill tool and loads
   the skill first. work run's implement list gains `Skill(shopsystem-bdd:bdd-red-green)` (scoped, probed to
   work), and the r2 step asserts it. In v1-v3 the first call of every implementer was that Skill load.
   `model:` is honoured under `--agent`: haiku, opus, sonnet, opus, as the definitions say.

Every fix kept `python3 -m pytest -q` at 523 passed. f9da946 and 3ab836c were red first in
`tests/scenarios/test_supervision.py`. Not run after its commit: df78fe7 (text only). x1 ran on it.

## Observed, not fixed (for the person or the next lines)

- **Refused commands cost turns.** Every implementer and reviewer started a command with `cd <its worktree>` and
  was refused 1-3 times (`cd` before `git` or before a redirect, `$R` variables). The session's own first
  `work run …; echo "exit=$?"` was refused in every run, and it retried without the echo. Nothing was lost.
- **The paths in the result point into a removed worktree.** The `report` and `findings` paths in the results do,
  since work run copies the run directory and removes the worktree. A reviewer flagged it as Cannot verify.
- **The worker branch `work/keep-items-1` is kept** after the merge, as supervision-1 left it.
- **The researcher's `questions` on DONE are dropped.** shake-1's question was asked again by the planner.
- **Cost of the session's suite record**: 0 s here, since the suite is tiny.
- **Not measured**: a worker that touches `.shop/work/` (r6), several work-items, a failing test after DONE, a
  rebase, PARTIAL, and spending against a budget (none set; the largest worker was $0.29).
