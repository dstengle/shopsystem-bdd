# Review of w192 (work-queue r31, r32, r23)

**Verdict: DONE.** No Critical finding and none triaged fix now. The change does what r31 and r32 ask for, it follows the plan's decisions 1 to 4, and no test is removed or weakened.

## Commits reviewed

The branch `work/w192` is gone, so these are the commits between `620ec316 work: w192 ready -> claimed` and `77954d18 work: w192 claimed -> done` on HEAD, less `work run`'s own `work:` commits:

- `64c62951` work-queue r31, r32: add refuses a done or abandoned initiative; done needs a green work-item. It touches `scripts/workqueue.py` (+4), `scripts/workqueue_done.py` (1 line changed) and `tests/scenarios/work_queue_add_steps.py` (+7).

The implementer's result (3-implement) lists `678b2865` instead. That commit exists, with the same author, date and message, and `git diff 678b2865 64c62951 -- <the three files>` is empty. So `64c62951` is the same change rebased when it was merged; the hashes differ but the content does not (see finding 3). Stages 4 and 5 list no commits, which matches: by the ruling, they made no change.

## Removed and weakened tests

None. I looked at `git diff 620ec316 77954d18 -- features tests`. The only test change is one added Then step (`add_refused_for_status`). No test function was deleted, no parametrize case dropped, no assert removed or loosened, and no skip or xfail added. Nothing changed under `features/`.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree with that.

## Cannot verify

- The report's red and green runs (3 failed, then 147 passed, 1 skipped). I did not run the suite, as the brief says; `work run` ran it.
- That the 7 whole-suite failures in the first question belong only to the supervision r121, r75 and r105 scenarios of w194, as the ruling says. Their step names and assertions point that way: missing steps, and a measurement on an all-withdrawn initiative, which comes from `work run`'s measure path and not from `_holds`. I did not run them.

## Findings

1. **Observation (Minor), w192.** `scripts/workqueue.py:90-93`: `add()` refuses only when the status is `done` or `abandoned`. An `initiative.md` with no status, or a status it does not know, goes ahead, and so does an initiative with no `initiative.md` (plan decision 2, which holds under r1 and r32). This is hardening: no client writes such a status today. Reproduction: none run. The plan's §5 and the report's Open questions name it.
   - Fix if wanted: a line that says what `add` does with an unknown status.
2. **Observation (Minor), w192.** `scripts/workqueue.py:92`: `work run`'s drafting (`supervise_draft`) into an initiative that is already `done` now gets the `Refused` error, which the plan says is raised outside the round's try in `supervise.py`.
   - No client reaches this today: the fix-now work-items of a branch review are drafted before `set_done`, and a capability-proposal is drafted into an open initiative.
   - Reproduction: none run; this comes from reading `supervise_done.py:31` and the plan's §5.
   - Fix if wanted: a supervision line saying how drafting into a done initiative ends.
3. **Minor (drop), w192.** The commit hash `678b2865` in `3-implement/result.json` is not the hash on HEAD (`64c62951`); the content is identical. It is a side effect of the rebase at merge, not something the implementer did wrong.

Already present, not from these commits:
- ruff `I001` at `scripts/workqueue.py:248`. This is the function-local `import workqueue_done` that was at line 244 at the base; the four added lines moved it down.
- `tools size --limit 300` printed nothing. `scripts/workqueue.py` is at 294 lines, close to the limit.

I checked one risk. The shared `_holds` change reaches `supervise_done.py:31` (`set_done`), `workqueue.py:249` (withdraw/retry `becomes`) and `workqueue_request.py:176` (request resolve). Each of them now leaves an all-withdrawn initiative unchanged. That agrees with r23, r31 and supervision r105, and none of them contradicts a line.

## Tools

- `tools check --base 620ec316`:
  - ruff: 1 error, the `I001` at `scripts/workqueue.py:248`, which was already there before these commits.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: nothing printed.

## Commands run

- `git log --format=%H -1 --grep="^work: w192 ready -> claimed$"` gave `620ec316`. `git log work/w192` gave unknown revision: the branch is gone.
- `git log --oneline 620ec316^..HEAD`, and `git log --grep="^work: w192 claimed -> done$"`.
- `git show 64c62951` and `git show --stat 678b2865`.
- `git diff 678b2865 64c62951 --stat -- <three files>` (empty).
- `git diff 620ec316 77954d18 --stat -- features tests`.
- `grep -rn "holds|becomes" scripts/*.py` (callers of `workqueue_done`).
- `git show 620ec316:scripts/workqueue.py | grep -n import` (where the import was before the change).
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 620ec316...`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` on the three touched files.
