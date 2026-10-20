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
