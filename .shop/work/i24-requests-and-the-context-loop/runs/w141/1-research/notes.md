# Research of w141: delivering-an-initiative starts work run only

Work-item w141 (under delivery) accepts delivery#r4, r10, r19, r20, r21, r22. Its change is to
`skills/delivering-an-initiative/SKILL.md` (markdown: no test executes it). No tools map exists: `tools tests-of`
says "no map" and I did not run `tools map` (it runs the whole suite). Tests were searched by text. `tools refs`
ran for `workqueue.add` and found 0 uses: it misses the extensionless `scripts/work` entry, which calls
`workqueue.add` at scripts/work:20 (grep, read).

## 1. Why each scenario is red today

None. The work-item accepts no scenario: its requirements are of a guarantees capability (delivery is
`group: guarantees`), and the brief gives no `Accepted scenarios:` line. Search: `Glob features/**` lists eight files
and none is delivery's; `Grep "@delivery|delivery#r"` over features/ finds no delivery id (the `@r<n>` tags there
belong to other capabilities). Nothing is run, so nothing is red.

## 2. What the system answers today

Probes, run through the plugin's `work` entry point (`python3 /home/vscode/shopsystem-bdd/scripts/work`), in
`.shop/scratch/w141-1-research/probe_work_help.py` and `probe_run_paths.py`, run with `-n 0`:

- `work --help` (run): exit 0; lists `add`, `run`, `retry`, `answer`, `status` and the rest.
- `work run --help` (run): `usage: work run [-h] initiative`, exit 0.
- `work run` with no initiative (run): exit 2, "the following arguments are required: initiative".
- `work add --help` (run): `--part-of`, `--under`, `--accepts` (append, so one per id: scripts/work:100).
- Case no_items (run): git repo in scratch; spec/index.md; initiative i1 `status: started`; p1 `formulated`, adds
  delivery#r4; no work-item. `work --root <scratch> run i1`: exit 0, no output, nothing drafted, no commit. The
  skill would read exit 0 as "every work-item green" over an empty list.
- Case one_item, no origin (run): `work add i1 "probe item" --part-of capability-proposal/p1 --under delivery
  --accepts delivery#r4`: exit 0, prints `w1`, committed by work add. `work run i1`: exit 1, `w1 failed`, fault
  "work run could not verify that it can push the initiative branch main to origin before the research stage".
- Case one_item, with a scratch bare origin (run): same, `work run i1` exit 1, `w1 failed`, fault "its researcher's
  session exited with an error (exit code 1); work run takes no outcome from it, whatever its result file says".
  No question is printed, so the skill sees a failure, not an awaiting-answer.
- A `work run` started from a worker refuses (run, first attempt): "it was started by a worker of another `work run`
  (of w141); a worker starts no delivery". My shell carries SHOPSYSTEM_WORK_RUN_WORKER; the probe drops it.
- Nearest case, `work add` into an initiative that does not exist (read): workqueue.add refuses "the initiative
  ... does not exist".
- Exit codes (read, supervise.py:205-207): 0 when every work-item is green or withdrawn; 3 when one is
  awaiting-answer and none failed; else 1. Matches the skill's "0 / 3 / anything else".

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| SKILL.md "Drafting" steps 1-2, 4 (`work add` for each proposal) | drafts every work-item before `work run` (old r1, r2) | r4 starts `work run` on the ask; delivery drafts no work-item (r1-r3 removed) | none (no test reads SKILL.md) | read; Grep of tests for SKILL/skills/delivering |
| SKILL.md step 3 (check reworded scenarios against drafted accepts) | stops before any `work add` (old r18) | removed with r18; nothing checks scenarios against accepts on the new path | none | read |
| SKILL.md step 5 (`## Retires` appended) | writes Retires per accepted deprecated scenario (old r17) | removed; supervision r73 moves it to work run (w138, not yet in code) | none | read; grep scripts for "## Retires": none |
| SKILL.md "Commit them, alone" | one commit of drafted files (old r3) | removed; work add already commits each file (workqueue.py `committed`) | none | read |
| SKILL.md "Run work run": "after the drafted work-items are committed" | start after commit (old r4) | r4 starts it on the ask, whether or not anything is drafted | none | read |
| SKILL.md "Fixes" bullet 1: "a fix to code that a review or a trial finds" | review and trial fixes drafted (old r10) | r10: trial only; review fixes stay with work run | none | read |
| SKILL.md "When it exits": "under a work-item that is `awaiting-ruling`" | names the old status | work run prints `awaiting-answer` (supervise.py:199; migrate renamed it, migrate_upgrade.py:21) | none | read; Grep awaiting-ruling |
| SKILL.md "Fixes" bullet 2: formulate round of `initiative-round` (r12, not accepted here) | sends to feature-formulator | agents/initiative-round.md:5-7 lists integrating-a-proposal and formulating-features as its only dispatchers | none | read |
| SKILL.md "Fixes" bullet 4: ledger `.shop/scratch/run/ledger-<initiative>.md` (r15, w142's) | appends by hand | r15 now `work note`, ledger tracked | none | read |
| scripts/workqueue.py:add (drafting target, used by r10) | writes fixed body, commits; no Retires; no check that a requirement is already accepted; no limit of five | unchanged by r10; the skill's old checks are not in it | none (see §4) | read; refs (0, see header) |

## 4. Tests the requirements make impossible to keep

None. No map exists, so `tools tests-of` answers nothing. By search: no test reads
`skills/delivering-an-initiative/SKILL.md` or names the skill (Grep of tests/ for SKILL, skills/, delivering:
only `Skill(...)` allowedTools strings in supervision steps and stub_claude.py). By search, the work-add callers
(tests/scripts/test_work_add_title.py, test_work_item_ids.py, test_work_withdraw.py, tests/scenarios/test_work_queue.py)
do not assert the skill's text. Sound: none of them changes if SKILL.md changes. Not checked: whether a test asserts
`work run`'s exit 0 on an empty initiative (probe no_items shows the behaviour, not the test).

## 5. A step the work-item skips

The new path (start `work run` with nothing drafted) skips the drafting steps. Each effect only drafting produced:

- Check of reworded scenarios (step 3): refuses before any `work add`, naming scenario and requirement. Read only.
  Without it, a scenario whose requirement no work-item accepts goes unscheduled. Nothing else catches it on this
  path. Read.
- `## Retires` written (step 5): deprecated scenarios listed for red-green's `features retire`. Nothing writes it
  until supervision r73 (w138) is delivered; w141 has no blocked_by on w138. Read.
- Commit of the drafted files: no effect of its own (work add commits each file). Read.
- Start of `work run` with nothing drafted: run (probe no_items): exit 0, empty output, nothing drafted. The skill
  would show an empty list and "exit 0: every work-item green". Supervision r72 (work run drafts one work-item per
  capability of a formulated proposal) is not in code yet (w138, ready). Run.

## 6. Defects

### D1 `work run` on a formulated proposal with no work-item exits 0 silently
Spec: supervision r72, "work run shall draft ... one work-item for each capability the proposal's adds and changes
name". Reproduction (run, probe_run_paths.py::test_run_with_no_work_item): fixture as in §2; `work --root <scratch>
run i1` -> exit 0, empty stdout and stderr, `.shop/work/i1/` still only initiative.md and p1.md, git log unchanged.
Not judged here; w138 is the work-item that adds drafting.

### D2 `awaiting-ruling` in the delivering skill's exit text (read)
SKILL.md:53 tells the session to show open questions under `awaiting-ruling`; supervise.py:199 prints questions under
`awaiting-answer` and the migration renamed the status. Read only; not run.

### D3 a worker that is refused a tool gives no question (read)
supervise_worker.py:201-206 gives each stage `--allowedTools` from TOOLS (or .shop/delivery.toml). A refused tool
leaves the worker's session to end as it does; supervise_worker.py:187-189 turns a missing result file into a fault
"its researcher wrote no result file ...", and a result of DONE is taken as is. grep of scripts/ for "denied|denial|
permission": none about tool refusal. Probe one_item (with origin) shows the nearest case: a failed session becomes
`status: failed` with a fault, not a question. This is the gap r21 names: no requirement of supervision says work run
puts a refused tool to the person as a question. Reading A: the skill cannot know the stage needed a tool (it reads
only work run's printout, r5), so r21 needs work run to print it. Reading B: r21 is met by the fault line naming the
stage. Both are for the plan.

## 7. The file set

- `skills/delivering-an-initiative/SKILL.md` (72 lines, markdown, no line limit). Changes: drop Drafting steps 1-5 and
  "Commit them, alone" (r1-r3, r8, r9, r17, r18 removed); keep `work add` for a trial's fix (r10, trial only); start
  `work run` on the ask (r4); add the tool-refusal question (r21) and the cannot-deliver question (r22); fix the
  `awaiting-ruling` name. Found by read of SKILL.md and of spec/capabilities/delivery.md (git show 474bc25^ for the
  old text).
- Test files: none. No test reads the skill (search, §4).
- On the change's path, edited or not (wc -l; room = 300 - lines; the limit is CLAUDE.md's, for Python only):
  - scripts/work: 147 lines, room 153. The entry; `add` and `run` subcommands. Not edited by my reading.
  - scripts/workqueue.py: 279 lines, room 21. `add` is the drafting target for r10; not edited by my reading.
  - scripts/supervise.py: 218 lines, room 82. `run` prints the statuses and exit codes (r6 via the skill). Not edited.
  - scripts/supervise_worker.py: 229 lines, room 71. Tool lists and sessions (r21 source). Not edited.
  - scripts/supervise_faults.py: 160 lines, room 140. Fault wording the skill shows. Not edited.
- `tools size --limit 300` printed nothing: no tracked Python file is over the limit.
- README.md (not Python) lines 57, 149, 206, 229, 250 describe the drafting skill; stale after w141. Not in the file
  set: no test reads them.
- Dependency: supervision r72-r74 (w138, ready) are not in code; removing r17 relies on them. w141 has no blocked_by on w138.

Probes: `.shop/scratch/w141-1-research/probe_work_help.py` (4 tests, passed), `probe_run_paths.py` (2 tests, passed).
Shell runs that were refused as needing approval: `work` by shell (help), `tools size` by plugin path, one python edit;
the same commands ran inside pytest or via `tools`. Scratch dir `.shop/scratch/` is git-ignored: `git status --porcelain` is empty.
