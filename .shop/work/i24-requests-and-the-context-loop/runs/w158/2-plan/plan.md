# Plan of w158: a proposed initiative that fulfils no request gets no integrate round (supervision#r79)

## 1. What goes green

supervision#r79, two scenarios (features/supervision.feature:848-867):

- "a proposed initiative is given to an integrate round with the accepted lines of the request it fulfils". It passes today (notes, section 1). It has to stay green.
- "a proposed initiative that fulfils no request is given no integrate round, stays proposed and leaves nothing behind". It is red today for two reasons:
  - Undefined steps. The Given "i1 is proposed and fulfils no request" has no definition. Neither do the Thens "no round of the kind integrate was started for i1", "i1 is proposed", "no branch is made for a round" and "nothing under .shop/work/ is left uncommitted". The notes found this by search. I found that two more steps have no definition either: the When "the person runs `work run i1` a second time" (the When `the person runs \`work {args}\`` in test_supervision.py:55 cannot match it, because that text ends in "time", not in a backtick) and the Then "the second `work run` was not refused".
  - Behaviour. `Rounds.due` (scripts/supervise_rounds.py:32-33) makes every `proposed` initiative due an integrate round. `Rounds.round` then moves it to `started` and makes branch `round/i1-1-integrate`. The brief refuses because there is no request. The next run is refused because log.jsonl is uncommitted (notes, defect D1, probe case A).

The work-item retires no deprecated scenario.

## 2. Where the change lands

- `scripts/supervise_rounds.py`: `Rounds.due` stops making an initiative due `integrate` when its frontmatter has no `fulfils`. Such an initiative falls through to the proposals check as any other initiative does. Nothing else in the module changes. `round` and `start_initiative` are never reached on this path.
- `tests/scenarios/supervision_rounds_steps.py` (201 lines, 99 free):
  - the Given: i1 is written `proposed`, with no `fulfils` and no request, then committed, in the same form as `proposed_fulfilling`;
  - the Thens: no integrate round for i1 (the `rounds` helper finds none); i1's `initiative.md` says `status: proposed`; the repository has no `round/` branch; `git status --porcelain -- .shop/work` prints nothing;
  - the second-run When: it keeps the first run's result and runs `work run i1` again through the existing `run_work`;
  - the Then that the second run was not refused: exit 0, and no `work:` refusal on stderr.
- `tests/scenarios/test_supervision.py`: binds the scenarios with `scenarios()`. Nothing changes unless the second-run When is put here, next to `run_work` (252 lines, 48 free). Either file is fine.

The notes list four more files that are only needed for one choice or another: `scripts/supervise_brief.py`, `scripts/supervise.py`, `scripts/supervise_review.py` and `scripts/workqueue.py`. Decision 2 below takes none of those choices, so I have taken all four out. `scripts/workqueue_request.py` is not edited either; the notes list it as read-only.

## 3. Decisions

1. A `proposed` initiative with no `fulfils` gets no integrate round and is not moved to `started`. It rests on supervision#r79: the round is given "the accepted lines of the request it fulfils", and with no request there are no lines to give. It also rests on the work-item's ruling of 2026-10-25: the first run has nothing to do for r79. r84 does not apply, because it holds only when an integrate round is started.
2. The check goes in `Rounds.due`, not in `Briefs.integrate_lines` or `Rounds.round`. That way nothing is written, logged, branched or pushed before the decision is taken, which is what r10 asks for. It rests on supervision#r10 and on the scenario's Thens "i1 is proposed" and "no branch is made for a round".
3. The run's exit is the one r9, r32 and r52 give. The work-item's ruling says so. The initiative has no work-items, so `show` prints none and the run exits 0. That is what "the second `work run` was not refused" asserts, and the first run is expected to exit the same way.
4. "Fulfils no request" means no `fulfils` field, which is the scenario's Given. Two nearby cases are left as they behave today, with neither reading chosen (section 5): a `fulfils` that names a request that is not kept (probe case B), and a request with no accepted lines (probe case C).

## 4. Tests the decisions break

None. The notes searched `tests/scenarios/` and `tests/scripts/` for `integrate|proposed` and found no test that gives an integrate round to an initiative with no `fulfils`. `proposed_fulfilling` gives `fulfils: q1`, so both its scenario and the r84 scenario (features/supervision.feature:1043) still reach the integrate round. `another_session_commits` (supervision_given.py:171) proposes i2 while the run takes i1, so it does not touch `due` for i2. I also checked that the one existing Then of the form "<name> is <status>" (`awaiting`, test_supervision.py:131) matches only `awaiting-answer`. The new "i1 is proposed" Then therefore clashes with no existing step.

## 5. Open cases

These are for the implementer to name in the report, not to settle:

- **`fulfils` names a request that is not kept (probe case B).** Today the run moves the initiative to `started` before it refuses. Doing so breaks r10's "change nothing". Neither scenario covers this case, and decision 4 leaves it as it is.
- **The request has no accepted lines (probe case C).** The scenarios say nothing about it; it is left as it is.
- **A branch review over an initiative with no work-items (notes, D3).** `pull_through` (supervise.py:205) counts zero work-items as all green. `unread` finds i1's own commit, so the first run may start a `bdd-branch-reviewer` session, commit "branch review 1 of i1" and go on to analysis. That review works in a detached worktree and commits its directory, so the Thens "no branch is made for a round" and "nothing … left uncommitted" should still hold. Scenario 1 goes the same way today and passes. r27 and r75 do not say whether zero work-items count as "every work-item green", and this plan does not guard it. If the review or the analysis makes either run of scenario 2 fail, report it as this case rather than adding a guard.
- **A faulted integrate round leaves the initiative `started` (notes, D2).** r84 and r86 read differently on this. It is out of r79's scope and not touched.
- **A proposed initiative with no `fulfils` that also holds capability-proposals.** `due` now goes on to the proposals check for it. The scenarios do not cover this.
- **`work run` with no initiative over such an initiative (`supervise_all.run_all`).** It reaches the same `due`. No scenario runs it.
