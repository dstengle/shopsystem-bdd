# Plan of w195: supervision#r122, whole-suite expected red for capability-proposals

Planned from `.shop/work/i34/runs/w195/1-research/notes.md`. Where the notes did not settle a decision, I also read `scripts/work_items.py` (lines 50-100), `tests/scenarios/supervision_proposal_steps.py` (the proposal Givens) and `tests/scenarios/supervision_tests_steps.py` (`counted_as`).

## 1. What goes green

**supervision#r122**: Scenario Outline "when the whole suite is run <run>, a failing scenario whose requirement a capability-proposal that is <status> adds or changes is counted as <counted>" (`features/supervision.feature:813`, 10 rows).

Why it is red today (notes §1, run): 9 rows fail, 1 passes.
- Six rows (worktree/approved, worktree/withdrawn, merge/awaiting-answer, merge/merged, merge/withdrawn, merge/approved-r3) stop at an undefined Given at line 817. A Given exists for `formulated` and for `drafted`, but none for `approved`, `withdrawn`, `awaiting-answer` or `merged`.
- Three rows (worktree/drafted-r2, worktree/formulated-r2, worktree/drafted-r3) stop at an undefined Then at line 820. No step reads the suite record of the run in the implementer's worktree (stage `implement`).
- Behind the steps: `acceptors` and `expect_red` in `scripts/work_items.py` read work-items only. Probe 1 (notes §2) shows every proposal case counted as not expected today.
- merge/formulated-changes-r2 passes today only because no work-item accepts `thing#r2`. It must still pass afterwards.

The work-item retires no deprecated scenarios. It has no `## Retires` section.

## 2. Where the change lands

- `scripts/work_items.py`
  - `acceptors`, or a sibling function beside it, also reads `kind: capability-proposal` files: their `status:` and the requirement ids in their `adds:` and `changes:`.
  - `expect_red` marks a scenario as xfail when such a proposal, neither `formulated` nor `withdrawn`, names one of its requirements. The xfail reason names the proposal.
  - The module docstring and the `expect_red` docstring name proposals.
- `tests/scenarios/supervision_proposal_steps.py`: a Given "i1's capability-proposal p1 is <status>, its adds|changes naming <id>" for the statuses `approved`, `withdrawn`, `awaiting-answer` and `merged`.
- `tests/scenarios/supervision_tests_steps.py`: a Then for "the whole suite `work run` ran in the implementer's worktree before the implementer started counted … as …". It reads the `suite` log line of stage `implement` for w1. It shares the record check with `counted_as`, whose behaviour stays the same.
- `scripts/supervise_merge.py`: the comment at lines 17-19 also names r122. This is text only and needs no code change: the implement and merge runs share one command (notes §3).

These are the researcher's three files plus the one comment. Not in the set: `README.md` (wording, optional), `tests/scripts/test_work_items.py` (unit cases are optional; the scenarios cover the rule) and `tests/scenarios/test_supervision.py` (it only needs editing if the new steps go in a new module, and they do not). No file passes 300 lines: the room left is 169, 147 and 92 lines.

## 3. Decisions

1. **The proposal source has no exclusion by name.** A work-item's own name excludes it under r43, but a capability-proposal is never "the one being merged". Every proposal that is neither `formulated` nor `withdrawn` counts. Rests on supervision#r122 (its text has no such exclusion) and supervision#r43 (the exclusion applies to work-items only).
2. **`merged` counts as expected.** r122 says "neither `formulated` nor `withdrawn`", and the accepted outline row (before w1's merge, merged, changes thing#r2) says expected. `model_work.py`'s `SETTLED` set is not used and not changed here; it serves a different check (retired ids in the design model). This settles the researcher's question 1 with the requirement's text and its accepted scenario, so it is not a question to the person. Rests on supervision#r122.
3. **Only `adds:` and `changes:` count, not `removes:`.** Entries that are not requirement ids, such as `term/<name>` in `adds:`, are ignored. Rests on supervision#r122 ("adds or changes").
4. **The scope is every initiative under `.shop/work/`.** `acceptors` already reads every initiative for r43's work-items. r122 names no initiative, so a proposal counts wherever it is filed. This settles the researcher's question 3 with the requirement's unqualified text and the reach r43 already has; it does not narrow r122. Rests on supervision#r122 and supervision#r43.
5. **Both whole-suite runs get the rule through one change.** The implement-stage run (r24) and the merge-stage run (r43) use the same `--whole-suite` command. Rests on the supervision Implementation note "r122: the checks are the whole-suite runs of r24 and r43" and on the commands note (`--whole-suite` marks as xfail what is counted as expected).
6. **The status a proposal has at each run is the status in that run's checkout.** For the implement run that is the claim-time head; for the merge run it is the rebased head. No extra reading of proposal state is added. Rests on supervision#r24 and supervision#r43 (each run checks its own tree).
7. **The new Given covers only the four statuses that have no step today.** That way it does not overlap the existing `formulated` and `drafted` Givens, and no step text matches twice. This decision concerns the test steps only; it rests on the accepted scenario text at line 817.

Not taken, and outside this work: the researcher's question 2, `--whole-suite` with an unknown work-item (D2). r122 adds nothing to the whole-suite path's handling of an unknown name, and no accepted scenario of this work-item drives it. The behaviour stays as it is today (the suite runs). It is left for its own request (see §5).

## 4. Tests the decisions break

None. The notes (§4) checked by search, since there is no coverage map:
- The r43 outline (`supervision.feature:793-810`) and the scenarios at :104, :484, :494, :504, :536-545 and :655-658 have no capability-proposal in their Givens, so decisions 1-6 leave their counts unchanged.
- `tests/scripts/test_work_items.py` never passes `--whole-suite`.
- The `formulated` and `withdrawn` rows, which are not expected, stay not expected under decision 2.

I also checked that the existing `formulated` and `drafted_with` Givens in `supervision_proposal_steps.py` stay as they are under decision 7. Their scenarios therefore keep their steps.

## 5. Open cases

For the implementer to name, not to choose:
- A capability-proposal with no `status:` line, or with a status r122 does not list.
- A proposal's `adds:` or `changes:` naming a range (`thing#r2-r4`), and whether the id parsing `accepts:` uses applies to it.
- A scenario whose requirement both a closed work-item (green) and an open proposal name: r122 alone makes it expected.
- A file under `.shop/work/` that is neither a work-item nor a capability-proposal but carries `adds:`.
- D2 (notes §6): `--whole-suite --work-item <unknown>` runs instead of refusing. D1: on the scenario path, the refusal surfaces as `mainloop: caught unexpected SystemExit!`. Neither is judged here.
