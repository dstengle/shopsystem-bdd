---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-20-i8-work-run-test-log
kind: measurement
about: capability/missingmass.io/shopsystem/shopsystem-bdd/supervision
date: 2026-10-20
---

# Test log: i8 through work run, the plugin delivering its own work-item (stopped)

The first real use of the new delivery: initiative i8-model-in-consumers of this repository, work-item `migrate-run`
(accepts migration-tools#r1-r11; features/migration-tools.feature, 10 scenarios, red and unbound), delivered by
`delivering-an-initiative` and `scripts/work run` of this repository's own plugin, on branch release-0.21.0 at
be1171b. The session was a Claude Code agent (opus) playing the session's part and watching; budget $25 or 90 min.

**Outcome: stopped after research, both work-items `awaiting-ruling`, exit 3.** A defect of work run, found and
fixed (015eb88). Running `work run` again cannot move them: `awaiting-ruling` is not movable and `work rule`
(design-decision/work-item-lifecycle-as-run's `awaiting-ruling -> planned`) does not exist yet, so the run is not
repeated without a person's ruling or a hand edit, which this run may not make.

## The session's part

- Preconditions: checkout clean; initiative.md there; `work --help` lists `run`. **No capability-proposal of i8 is
  `formulated`** (all three are `merged`), so the skill as written would stop here. The run went on because the
  work-item was already drafted (by hand, earlier) and the brief said to deliver it; nothing was drafted, and no
  draft commit made.
- Started `python3 scripts/work --root <repo> run i8-model-in-consumers` in the background at 18:29:14Z; it exited
  at ~18:33:05Z (about 3 min 50 s) with code 3. The session read no worker output while it ran (it watched only
  `git log` for work run's commits).

What it printed:

```
kb-trial awaiting-ruling
  - code-scout gave no result file (/home/vscode/shopsystem-bdd/.shop/worktrees/kb-trial-1-research/.shop/scratch/1-research/result.json)
migrate-decisions withdrawn
migrate-deprecated withdrawn
migrate-layout withdrawn
migrate-plan withdrawn
migrate-run awaiting-ruling
  - code-scout gave no result file (/home/vscode/shopsystem-bdd/.shop/worktrees/migrate-run-1-research/.shop/scratch/1-research/result.json)
migrate-status-and-ids withdrawn
migration-skill withdrawn
```

## Stages, sessions, cost, time

| work-item | stage | agent | session | time | turns | cost | ended |
|---|---|---|---|---|---|---|---|
| kb-trial | research | code-scout (haiku) | 8d0d61b8-09cc-4d6f-a688-9563eb36dd97 | 20 s | 9 | $0.005 | no result file |
| migrate-run | research | code-scout (haiku) | 433b82fe-3c31-41c4-9d28-274fb7209583 | 201 s | 51 | $0.085 | no result file |

Workers $0.09 in all; the session's probes (4 haiku `claude -p`) a few cents more. Two moves, each its own commit by
work run: fa7eb99 (kb-trial drafted -> awaiting-ruling), 83d676d (migrate-run drafted -> awaiting-ruling).

## The defect and the fix

1. **Every write in a worktree was refused as "a sensitive file".** Both researchers' Writes (notes, probes,
   result.json) were refused: "Claude requested permissions to edit … which is a sensitive file", and `mkdir` was
   refused too. Cause, probed in a scratch repository: claude refuses every write under a `--plugin-dir`. work run
   gives each worker `--plugin-dir <its plugin root>` (r11), and here the repository *is* the plugin root, so
   `.shop/worktrees/` lies inside it. The same write in the same nested worktree succeeds with no `--plugin-dir`,
   fails with `--plugin-dir` the repository, and succeeds in a worktree under /tmp with that `--plugin-dir`. The
   fixture runs never met it: their plugin was a separate worktree (`ids/plugins/D`). **Fix 015eb88**
   (`scripts/supervise.py`): when the repository is the plugin's directory or inside it, the worktrees go in a
   temporary directory outside it, removed when the run ends; otherwise `.shop/worktrees/` as before.
   `python3 -m pytest -q`: 546 passed, 1 skipped. No scenario pins the new case (the r11 and worktree steps run in
   a tmp repository outside the plugin); it is not re-run on real workers, since nothing can move.
   An edit of `scripts/supervise.py` by a Bash heredoc was refused by the session's own auto-mode classifier
   (self-modification); the Edit tool was allowed.

## What this real use showed beyond the fixture runs

- **The plugin cannot deliver its own work without the fix**: the fixture layout (plugin outside the repository)
  hid the sensitive-path rule.
- **There is no way back from awaiting-ruling.** A run stopped by a defect of work run leaves its items where
  only `work rule` (not built) or a hand edit can move them. Re-running after a plugin fix, as the brief imagined,
  is not possible with today's `work`.
- **work run takes every drafted item, `blocked_by` ignored.** kb-trial (no `accepts:`, `blocked_by` a withdrawn
  item, a `check:` that clones GitHub) was started first. Its researcher rightly gave NEEDS_CONTEXT ("no accepts:
  line"), but would have had nothing to stop it from going further. The guards between work-items are in
  supervision's Not yet.
- **The skill's precondition does not fit an item drafted earlier**: with every proposal `merged`, the skill stops,
  though a drafted work-item waits.
- **The researcher's real findings were lost to the person**: migrate-run's researcher found, read-only, that
  `features deprecate` leaves `@holding` in place (so `model check` still flags it after migrate run), and that r9
  ("a decision file's id name is its stem") disagrees with the r2/r5/r9 scenarios (`0007-a.md` gives `a`). Both are
  in its session.json result only; the work-item's question is just "no result file". The base commit in the brief
  was 31e9ed3 (the commit that added initiative.md), not the head; the worktree itself was at the head.
- The narrowed tools held: neither researcher worked around the refusals with a shell write, and both said so.

## log.jsonl lines of this run

```
{"time": "2026-10-20T18:29:18+00:00", "work-item": "kb-trial", "stage": "research", "agent": "code-scout", "session": "8d0d61b8-09cc-4d6f-a688-9563eb36dd97", "event": "start"}
{"time": "2026-10-20T18:29:38+00:00", "work-item": "kb-trial", "stage": "research", "agent": "code-scout", "session": "8d0d61b8-09cc-4d6f-a688-9563eb36dd97", "event": "end"}
{"time": "2026-10-20T18:29:38+00:00", "work-item": "kb-trial", "before": "drafted", "after": "awaiting-ruling", "by": "work run"}
{"time": "2026-10-20T18:29:38+00:00", "work-item": "migrate-run", "stage": "research", "agent": "code-scout", "session": "433b82fe-3c31-41c4-9d28-274fb7209583", "event": "start"}
{"time": "2026-10-20T18:32:59+00:00", "work-item": "migrate-run", "stage": "research", "agent": "code-scout", "session": "433b82fe-3c31-41c4-9d28-274fb7209583", "event": "end"}
{"time": "2026-10-20T18:32:59+00:00", "work-item": "migrate-run", "before": "drafted", "after": "awaiting-ruling", "by": "work run"}
```

# Run 2: through every stage, stopped at review (awaiting-ruling, exit 3)

Same work-item, `migrate-run` (migration-tools#r1-r11, 10 scenarios red), on release-0.21.0 at 8f5d556, after the
worktree fix (015eb88, scenario 8f5d556), migration-tools r3 and r9 corrected from run 1's researcher (24a6c8f), run
1's moves reverted (0290645, bba0277) and kb-trial withdrawn (7d84722). The session was a Claude Code agent (opus)
playing the session's part; budget $25 or 90 min.

**Outcome: research, plan, implementation and review all ran; the review left five Important findings, so
`migrate-run` is `awaiting-ruling`, exit 3.** All 10 scenarios green and the suite green (557 passed) on the
implementer's commits; the reviewer's probes found defects the scenarios do not reach, and one question only the
person can answer. Not repeated: fix work-items and re-reviews are in supervision's Not yet, and one finding is a
meaning question on migration-tools r6, which the brief says to stop on. No plugin fix in this run.

## The session's part

- Preconditions: checkout clean; initiative.md there; `work --help` lists `run`; every proposal of i8 `merged`, not
  `formulated` (the known gap); went on as briefed. Nothing drafted: migrate-run was already drafted.
- Started `python3 scripts/work --root <repo> run i8-model-in-consumers` in the background at 18:46:05Z; exited
  19:11:45Z, 25 min 40 s, code 3. The session watched only `git log` while it ran.
- Another session committed to the branch mid-run (2ea9b66, i15 proposed) and left uncommitted changes in the
  checkout (.shop/work/README.md, i15's initiative.md); work run's commits went on undisturbed. This test log is
  committed with a pathspec naming only itself.

What it printed:

```
kb-trial withdrawn
migrate-decisions withdrawn
migrate-deprecated withdrawn
migrate-layout withdrawn
migrate-plan withdrawn
migrate-run awaiting-ruling
  - Important, scripts/migrate:63-85,213-219: a ledger heading that is not in the <nnnn>-<slug> form is merged into the entry before it or lost, and spec/decisions.md is removed with exit 0 (r11 says to remove it only once every entry is replaced); Important, scripts/migrate:217,122,291: a ledger entry's new decision file overwrites a decision file moved from decisions/ or already tracked at that path, and its content is lost; Important, scripts/migrate:266-283: an untracked file at a move's destination passes the check, then git mv fails during the writes and leaves earlier moves staged with a traceback (r7: change no file); Important, tests/scenarios/test_migration_tools.py:336-340: r6 is green only because the fixture's old records already carry about:. migrate writes none, so model check reports v10b on a real old-system repository (the person decides: migrate writes about, or r6 is narrowed); Important, scripts/migrate:88-91: summary and by are written unquoted, so model reads a first paragraph with ' #' or a leading '[' wrongly (r2)
migrate-status-and-ids withdrawn
migration-skill withdrawn
```

## Stages, sessions, cost, time

| stage | agent (model) | session | time | turns | cost | result |
|---|---|---|---|---|---|---|
| research | code-scout (haiku) | d24ef257-ecc3-4707-90d3-1be5753a293d | 345 s | 44 | $0.15 | DONE |
| plan | bdd-planner (opus) | 9ecafea5-2d21-404a-83e4-32332b866450 | 186 s | 26 | $0.76 | DONE |
| (suite at claim) | work run | - | 116 s | - | - | 547 passed at 2a56b96 |
| implement | bdd-implementer (sonnet) | a06f66fe-782d-460b-a1fb-29bab3de5112 | 573 s | 119 | $1.34 | DONE, 10 commits c8eb7d6..bf3a278, suite 557 passed |
| (suite after) | work run | - | ~118 s | - | - | green |
| review | bdd-task-reviewer (opus) | 4190b973-23e3-495f-a19c-19390c98515b | 198 s | 29 | $1.01 | DONE_WITH_CONCERNS: 5 Important fix now, 1 Important + 1 Minor observation, 2 Minor drop |

Workers $3.25 in all; the session's own cost is not measured here. Moves by work run, each its own commit: 7b86cc0
(drafted -> researched), c7a9832 (-> planned), 72d8600 (-> ready), 2a56b96 (-> claimed), 565e14e (-> done),
c9f5569 (done -> awaiting-ruling). The implementer's code: scripts/migrate (new), tests/scenarios/test_migration_tools.py
(366 lines), tests/scripts/test_bound.py; 693 lines added, all in the fileset. The temporary worktrees were removed
at the end (`git worktree list` shows only the checkout).

## Fixes

None. The stop is supervision r5 working as written (a result other than DONE -> awaiting-ruling); there is no fix
round (Not yet), so nothing in work run or a worker definition is at fault.

## Questions for the person

- **r6 (meaning):** old-system records carry no `about:`, so a really migrated repository fails `model check` (v10b);
  the fixture hides it by giving its records `about:` in advance. Either migrate writes `about` (from what?), or r6
  is narrowed. The implementer's report names the same gap and a second one: no `initiative.md` for `work/`.
- **r8 against r9 (meaning, Minor):** r8's scenario says a moved plan keeps its content; r9 gives a plain plan an id,
  which changes it. The fixture avoids it with ids put in advance. For the formulator.
- **Four fix-now defects** (F1 ledger split loses entries and still removes the ledger, against r11; F2 a new
  decision file overwrites a moved one; F3 a git mv refused mid-write leaves a half move, against r7; F5 unquoted
  summary/by misread, r2) need a fix work-item, which `work` cannot make yet; and `work rule` does not exist to move
  the item on.

## What this real use showed beyond the fixture runs

- **The whole pipeline runs on the plugin's own repository** once worktrees sit outside the plugin dir: four fresh
  workers, four result files, six moves, a green suite, in under half an hour and about $3.
- **Green scenarios were not enough; the review was worth its dollar.** The reviewer's probes found data loss and a
  broken r7 promise that all 10 scenarios pass over, and that r6 is green only by the fixture's construction. The
  fixture runs' items were small enough that review came back clean or Minor.
- **awaiting-ruling after review has no way forward**: no fix work-item, no re-review, no `work rule`. The review's
  findings are the work that remains, and only a person or a hand edit can start it.
- **The question line is long**: work run joins the reviewer's questions into one line under the item, so the five
  findings read as one paragraph in the printout.
- **The implementer could not `chmod +x`** (narrowed tools), so scripts/migrate is 100644 unlike its siblings.
- **The suite runs twice around implementation** (116 s before, ~118 s after): 4 of the 26 minutes.
- **The branch is shared**: another session committed and left changes in the checkout during the run; work run's
  pathspec commits were unaffected, but the skill's clean-checkout precondition holds only at the start.

## log.jsonl lines of this run

```
{"time": "2026-10-20T18:46:05+00:00", "work-item": "migrate-run", "stage": "research", "agent": "code-scout", "session": "d24ef257-ecc3-4707-90d3-1be5753a293d", "event": "start"}
{"time": "2026-10-20T18:51:51+00:00", "work-item": "migrate-run", "stage": "research", "agent": "code-scout", "session": "d24ef257-ecc3-4707-90d3-1be5753a293d", "event": "end"}
{"time": "2026-10-20T18:51:51+00:00", "work-item": "migrate-run", "before": "drafted", "after": "researched", "by": "work run"}
{"time": "2026-10-20T18:51:51+00:00", "work-item": "migrate-run", "stage": "plan", "agent": "bdd-planner", "session": "9ecafea5-2d21-404a-83e4-32332b866450", "event": "start"}
{"time": "2026-10-20T18:54:58+00:00", "work-item": "migrate-run", "stage": "plan", "agent": "bdd-planner", "session": "9ecafea5-2d21-404a-83e4-32332b866450", "event": "end"}
{"time": "2026-10-20T18:54:58+00:00", "work-item": "migrate-run", "before": "researched", "after": "planned", "by": "work run"}
{"time": "2026-10-20T18:54:58+00:00", "work-item": "migrate-run", "before": "planned", "after": "ready", "by": "work run"}
{"time": "2026-10-20T18:54:58+00:00", "work-item": "migrate-run", "before": "ready", "after": "claimed", "by": "work run"}
{"time": "2026-10-20T18:56:54+00:00", "work-item": "migrate-run", "stage": "implement", "event": "suite", "record": "Suite: 547 passed, 0 failed at 2a56b96 in 116 s"}
{"time": "2026-10-20T18:56:54+00:00", "work-item": "migrate-run", "stage": "implement", "agent": "bdd-implementer", "session": "a06f66fe-782d-460b-a1fb-29bab3de5112", "event": "start"}
{"time": "2026-10-20T19:06:28+00:00", "work-item": "migrate-run", "stage": "implement", "agent": "bdd-implementer", "session": "a06f66fe-782d-460b-a1fb-29bab3de5112", "event": "end"}
{"time": "2026-10-20T19:08:26+00:00", "work-item": "migrate-run", "before": "claimed", "after": "done", "by": "work run"}
{"time": "2026-10-20T19:08:26+00:00", "work-item": "migrate-run", "stage": "review", "agent": "bdd-task-reviewer", "session": "4190b973-23e3-495f-a19c-19390c98515b", "event": "start"}
{"time": "2026-10-20T19:11:45+00:00", "work-item": "migrate-run", "stage": "review", "agent": "bdd-task-reviewer", "session": "4190b973-23e3-495f-a19c-19390c98515b", "event": "end"}
{"time": "2026-10-20T19:11:45+00:00", "work-item": "migrate-run", "before": "done", "after": "awaiting-ruling", "by": "work run"}
```
