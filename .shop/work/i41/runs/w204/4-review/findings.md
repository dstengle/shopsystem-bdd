# Review of w204 (supervision r140-r148)

**Verdict: DONE_WITH_CONCERNS.** There is one Important finding triaged fix now (F1). If a redraft's integrate round faults, or ends with no change list, the next `work run` starts an apply round for the proposal, not the integrate round again. Nothing under `features/` changed beyond the three retirements the work-item lists, and no test was removed or weakened.

## Commits reviewed

The branch `work/w204` is gone. The commits are those between `be28c607` (`work: w204 ready -> claimed`) and `9a7de712` (`work: w204 claimed -> done`) on HEAD:

- `d076baa8` supervision: an apply round that applies nothing sends its proposal back to integration (r140-r148)

This matches the one commit the implementer's `result.json` lists. Files: agents/initiative-round.md, features/supervision.feature (-28), scripts/supervise.py, supervise_brief.py, supervise_change.py, supervise_rounds.py, tests/scenarios/supervision_formulate_steps.py, supervision_reintegrate_steps.py (new, 138 lines), supervision_rounds_steps.py, test_supervision.py.

`features/`: the only change is the removal of the deprecated @r80, @r114 and @r71 scenarios. These are the three that the work-item's Retires section lists under r144, r145 and r146. Not a finding.

## Removed and weakened tests

None. What I searched: every `-` line of `git diff be28c607 d076baa8 -- tests`. There are only two, and both are step regexes that were widened, with no `assert`, test function, parametrize case, skip or xfail removed:

- `supervision_formulate_steps.py:36` `apply_change_list`: adds the optional `(?:applies p1's drafts and )?`.
- `supervision_rounds_steps.py:21` `answered_proposal`: adds the optional `(?:, for thing,)?`.

Every text the old regexes matched still matches, and the step bodies are unchanged. This is setup only.

## Allowances

The report's `## Tests changed under an allowance` says "none", and adds a note on the `answered_proposal` regex as setup. That note holds: the diff adds, removes and changes no assert, expected value or case. The `apply_change_list` widening is the same kind of change, but the report does not mention it (Minor, part of F5).

## Cannot verify

- The report's run figures: `--work-item w204` all pass, 261 passed / 1 xfailed for the supervision suite, 143 passed for tests/scripts. I did not run the suite; `work run` ran it before the merge.
- The red-before-green history the report gives, including r148 passing vacuously at first. The commits are squashed into one, so I cannot check it.
- Whether a real `initiative-round` agent gives `nothing_applied` as the new bullet in agents/initiative-round.md says. Only the stand-in gives it.

## Findings

### F1. Important, fix now: a faulted redraft integrate round is followed by an apply round, not by the integrate round again
- Where: `scripts/supervise_rounds.py:73-81` (`applied_nothing`) and `:64-66` (`route`), at d076baa8. Work-item w204.
- What is wrong: `applied_nothing` looks only at the proposal's latest stage directory under `runs/p1/`. Suppose the integrate round started for p1 under r140:
  - ends in a fault or at its turn limit (r86), or
  - ends with no change list or one that cannot be read (r96, `refuse_integrate`, which goes through `keep_round`).

  Then its directory `runs/p1/<k>-integrate` is the latest, and p1 is still awaiting-answer (r143/D5). On the next `work run`, `applied_nothing` returns False and `route` falls through to `AFTER["awaiting-answer"]`, so an **apply** round runs again on the drafts the earlier apply already found did not hold the answers. `keep_round`'s own docstring (`:218-219`) says the next `work run` "starts the round again". This route starts a different round.
- Why it matters: the round started is the wrong one. In the best case another apply gives `nothing_applied` and the loop recovers after one wasted serial round. In the worst case, apply applies drafts the person's answers had already made stale. The report's own open question says the stand-in's integrate for p1 under "every other round ends" gives no change list (an r96 error). So this path is reached in the scenarios, not just in theory.
- Fix: when deciding whether to route to integrate, skip trailing `-integrate` stage directories of the proposal. Equivalently: route an awaiting-answer proposal to integrate when its latest stage is an apply that applied nothing, or an integrate that did not move it to drafted. Add a scenario for the retry, worded through a line first if no line covers it (r86/r140).

### F2. Important, observation: a redraft naming a second capability rewrites that capability's existing proposal in place without setting it drafted
- Where: `scripts/supervise_change.py:90-99` (`write_proposals`, the `held` branch). Work-item w204.
- What is wrong: `proposal_for` is called for every capability in the change list, not only the one the redrafted proposal argues. Suppose a proposal for another capability, p2, already exists, at any status (approved, formulated). Then p2's `adds`/`changes`/`removes` and its drafts sentence are replaced and its status is left as it was. Only `name` is moved, at `supervise_rounds.py:193-194`. This contradicts r92: "write a `drafted` capability-proposal for each capability the change list names". The result is, for example, a `formulated` proposal whose lists name ids that were never applied.
- Reproduction (from the code, no run): the change list of p1's integrate round is `[{capability: thing}, {capability: other}]`, and the initiative has `p2.md` with `argues: [other]`, `status: formulated`. After the round, `p2.md` is still `formulated` with the new lists, and only p1 is drafted.
- Why it is an observation: the integrate bullet this commit adds tells the agent to give "one entry for its capability", and the report lists this case as open. No client sends it today.
- Fix: rewrite in place only the proposal `name` that the round was started for. Treat any other capability as r92 does, or refuse it.

### F3. Minor, observation: the proposal's integrate brief labels the proposal "Initiative:"
- Where: `scripts/supervise_brief.py:44` (`label = "Initiative" if stage == "integrate" ...`), reached for a proposal at `:52-59`.
- What is wrong: for p1 the brief reads `Initiative: .shop/work/<i>/p1.md`. The new integrate bullet in `agents/initiative-round.md:30` begins "When your brief names a capability-proposal…". The brief never says "Capability-proposal", so the agent has to infer it from the file.
- Fix: use `Capability-proposal` as the label when `name != self.initiative`.

### F4. Minor, drop: ruff findings in the files the commit touched
`tools check --base be28c607`:
- `scripts/supervise_change.py:96` B023: the lambda reads the loop variable `said`. It is a false positive, because `re.sub` calls the lambda straight away.
- `tests/scenarios/supervision_reintegrate_steps.py:13` F401: unused import `git`.
- `:137` FURB167: `re.M`.
- `tests/scenarios/test_supervision.py:14` I001: import order. `supervision_reintegrate_steps` comes after `supervision_review_steps`.

These are cheap to fix with `ruff --fix` plus `lambda _, s=said: s`, but they change no behaviour.

### F5. Minor, drop: inaccuracies in the report
- `## Budget` says "Touched (11)" but lists 10 files.
- `## Tests changed under an allowance` mentions only one of the two widened step regexes.

## Code no line asks for

None found:
- `nothing_applied` is the mechanism for r147/r140 that the plan's D1 names.
- The `Ledger:` and `Earlier drafts path (read only):` lines serve r141/r142.
- `move(..., also=)` serves r142's single commit.
- The in-place rewrite serves r148. Its reach beyond p1's own capability is F2.

## Commands run

- `git log --format=%H -1 --grep="^work: w204 ready -> claimed$"` → be28c607
- `git log be28c607..work/w204`: unknown revision (the branch is gone)
- `git log --format='%h %s' be28c607..HEAD`; `git log --grep="^work: w204 claimed -> done$"` → 9a7de712
- `git show --stat d076baa8`; `git diff be28c607 d076baa8 -- scripts agents tests`; `git diff be28c607 d076baa8 -- features`
- `git diff be28c607 d076baa8 -- tests | grep -E '^-'`
- `git show d076baa8:scripts/supervise_rounds.py` (lines 30-215); `git show d076baa8:scripts/supervise_brief.py`
- `grep -nE "r(140|...)" spec/capabilities/supervision.md`; `grep -n "def run_dir|def keep_round" scripts/supervise*.py`
- `python3 <Scripts>/tools check --base be28c607…`
  - ruff: 4 errors (F4)
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 <Scripts>/tools size --limit 300`: nothing printed (no file over)
