# review of w194

**Verdict: DONE.** Nothing to fix now and nothing Critical. There are two Minor findings, both triaged drop.

## Commits reviewed

The branch `work/w194` is gone. The commits come from the checked-out history, between `32823806 work: w194 ready -> claimed` and `78ecb78d work: w194 claimed -> done`, leaving out `work run`'s own `work:` commits and other initiatives' commits:

- `919e4510` supervision: a kept review with no question lists nothing to fix (r121), r120 verdict step; retire the PARTIAL scenario
- `6ef3162b` supervision: measure only an initiative with a green work-item (r75), r105 steps

The implementer's result lists `e7dd7e78` and `fdeae6af`. Those are the same two commits from before `work run` rebased them onto `e8f5572a` (the r122 formulate commit). The subjects and per-file stats are the same. `git diff fdeae6af 6ef3162b` over the six fileset files differs only by e8f5572a's 23 added lines in features/supervision.feature. See Minor finding 1.

Changed files: features/supervision.feature (−9, the retired scenario), scripts/supervise.py (1 line), scripts/supervise_analysis.py (`lists_nothing`), tests/scenarios/supervision_analysis_steps.py, supervision_delegation_steps.py and supervision_done_steps.py. Every file is in the work-item's fileset.

## Removed and weakened tests

I searched the diff for removed `def` / `@given` / `@then`, for removed or loosened `assert`s, for removed scenarios and Examples rows, and for skip and xfail.

- **Deprecated @r75 scenario removed** (feature:1050, "a kept branch review that ended PARTIAL, with no question and no finding, does not list nothing to fix now, and no `measure initiative` is run (deprecated)"). It proved that a PARTIAL review with no question was not measured. It is listed in w194's `## Retires` and in the plan's "Tests the decisions break". It was removed with `features retire`, so it holds.
- **Step `reviewer_partial` removed.** Only the retired scenario used it. Its text is covered by the new parameterised `reviewer_gives_no_question`. The plan lists it (decision 7), so it holds.
- Nothing else was removed or weakened. No assertion was changed, and no skip or xfail was added.

## Allowances

- `supervision_delegation_steps.py` `session_answers` (setup): **holds.** The diff adds a guard around `asked_by_the_log(repo)` and adds or changes no assert, no expected value and no parametrize case.
- `supervision_done_steps.py` `started_with_items` (setup): **holds.** The fixed text became a regex over green or withdrawn. It writes the same files for the old text and has no assertion.

## Cannot verify

- The report's run figures: 155 passed with `--work-item w194`, 353 passed with `--whole-suite tests/scenarios/test_supervision.py tests/scripts`, and 905 passed / 8 failed at the start. I did not run the suite, because `work run` ran it before the merge.

## Findings

1. **Minor, drop.** `.shop/work/i33/runs/w194/5-implement/result.json`: `commits` names `e7dd7e78` and `fdeae6af`, but the history has `919e4510` and `6ef3162b`.
   - Why it matters: anyone following the result's SHAs reads commits that are not on the branch.
   - What I checked: the content is the same apart from the rebase onto e8f5572a, so nothing is lost or added.
   - Fix: none needed. It comes from `work run`'s rebase, not from the implementer.
2. **Minor, drop.** `scripts/supervise_analysis.py:1-3`: plan §2 says the module docstring is rewritten to state r121, but it was left unchanged. It still says "once the kept branch review lists nothing to fix now", which stays true under r121. Only the method docstring was rewritten.
   - Fix: none needed.

Risks I checked outside the diff:

- **Do r74 and r121 read the same field?** A review with findings but an empty `questions` might be measured and set done while a fix is drafted. They agree: `fix_work_item` (scripts/supervise_draft.py:65-67) drafts only from a non-empty `questions` list, and `lists_nothing` now reads only `questions`.
  - A `questions` that is a non-empty string drafts nothing and is not taken as listing nothing, the same as before this change.
- **Is there another path to `analyse` or `set_done` that skips the r75 guard?** No. `grep` finds only scripts/supervise.py:223-224, behind the new condition at :222.
- **Does r105's code path hold?** The plan's claim that `workqueue_done.holds` already requires a green work-item (w192, work-queue#r23) is consistent with the report. The new guard repeats it in front of `set_done`, with no behaviour a narrator sees.
- **Is there code that no Behaviour line asks for?** No. The `lists_nothing` change is r121 ("whatever its status"), and the guard is r75's "at least one of them is green". Neither adds behaviour beyond those lines.
- **Do the changes go against the Behaviour lines or the Purpose?** None found.

## tools check / size

- ruff: 1 error, `scripts/supervise_analysis.py:4:1 I001` (import block unsorted). This was already in the base: the imports at 32823806 are the same, and the order is deliberate (the comment says supervise_worker goes first). The commits do not touch the import block, so this is not a finding against w194.
- vulture: clean.
- import-linter: the project states no import contracts.
- size --limit 300: printed nothing. scripts/supervise.py stays within the limit.

## Commands run

- `git log --format='%H %s' -40`
- `git show --stat e7dd7e78 fdeae6af`
- `git log --stat 32823806..HEAD -- . ':!.shop'`
- `git diff 6a19ad00 6ef3162b`
- `git diff fdeae6af 6ef3162b --stat -- <fileset>`
- `git show 32823806:scripts/supervise_analysis.py`
- `grep -n "lists_nothing|.analyse()|set_done()|def items" scripts/*.py`
- `sed -n 195,230p scripts/supervise.py`
- Grep of `def fix_work_item` in scripts/
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 32823806`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
