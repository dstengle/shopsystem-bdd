# Review of w184 (supervision r110, r117, r19)

**Verdict: DONE.** Nothing is Critical and nothing is to be fixed now. The commits do what r19, r117 and r110 ask, the only change under `features/` is the retirement the work-item lists, and every changed test is listed in the plan or is a setup allowance that holds. There is one Minor observation.

## Commits reviewed

The branch `work/w184` is gone. The commits are those between `85065878 work: w184 ready -> claimed` and `6df21f90 work: w184 claimed -> done` on HEAD, less `work run`'s `work:` commits (`1f4a0731` is w186's):

- cd134f29 researcher gets 80 turns (r19); retire the 40-turn scenario
- d40c0d26 a gate with no question asks for the approval of the lines (r117)
- b1b8562c a fix's green is followed by the next branch review (r110)

The implementer's result lists 87cdf5a2, 8d0d6bbe and 3d9bca9e, which have the same subjects. These are the same commits before `work run` merged them with new hashes: `git diff 3d9bca9e b1b8562c -- <the 8 files>` is empty, and both ranges give the same diffstat (8 files, +51 −20). There is no difference in content.

## Removed and weakened tests

I looked for deleted test functions, dropped parametrize cases, removed or loosened asserts, an added skip or xfail, and narrowed or changed step patterns.

- `features/supervision.feature:393`, the 40-turn scenario (@r19 @deprecated). It is removed by `features retire`, as the work-item's Retires section lists. It proved `--max-turns 40`. The plan lists it in §4. Its step binding (`supervision_then_workers.py:215`, `limit of {turns:d} turns`) stays, because the 80-turn scenario still uses it.
- `tests/scenarios/supervision_proposal_steps.py` `reviewer_lists` (the Given of the r74 scenario). Before, every bdd-branch-reviewer session gave the two findings. Now the first gives the findings and later sessions list nothing. No assert changed. The r74 Then still asserts exactly one fix work-item, part of p1, naming the first review's findings.md. The plan lists it in §4.
- `tests/scenarios/supervision_rounds_steps.py` `questions_hold`: the pattern is narrowed from `holds (?P<text>.+)$` to `holds (?P<text>\".+)$`. The assertion is unchanged. Every step it bound before begins with a quote (feature:1231, :1257; :690 is the `w1's` step), so it still binds them all. The plan lists it in §4 and decision 4.
- `tests/scenarios/test_supervision.py` `is_green`: the pattern is narrowed from `parse("{name} is green")` to `re("(?P<name>w\d+) is green$")`. The assertion is unchanged. The Then steps it bound before were `w1 is green` at feature:869 and :1301, and both still match. The plan does not list it, but it is covered by the report's allowance (below).

Nothing else was removed or weakened.

## Allowances

- `supervision_proposal_steps.py` `reviewer_lists`, setup: **holds**. The diff changes only the stand-in's plan data and adds no `assert` or expected value.
- `test_supervision.py` `is_green`, setup/matching: **holds**. Only the decorator's pattern changed. There is no `assert`, expected value or parametrize change, and every step it bound before still binds.

## Cannot verify

- The report's red runs before the code (r19 `--max-turns 40`, r117 IndexError, r110 `len(review)==2`) and "suite at start: 858 passed, 3 failed". These are not visible in the commits.
- The green figures: work-item 145 passed, 1 skipped. I did not run the whole suite; `work run` ran it before the merge.

## Findings

1. **Minor, observation (w184).** `tests/scenarios/test_supervision.py:100` is edited, but it is outside the work-item's `fileset:` (design-decision the-file-set-is-the-claim). The edit is one pattern narrowed so that the new r110 Then is not swallowed by `{name} is green`. The report names it under "Outside the file set". It matters because another work-item claiming that file in parallel could conflict at merge. The merge succeeded and the change is test-matching only. Fix: none needed now. A future plan that adds a Then ending in "is green" should list test_supervision.py in its file set.

### Risks checked, no finding

- **Stand-in session order** (`stub_claude.py:186`). `record(start)` runs before `started_agents().count(agent)`, so the first session gets index 0 and later ones are capped at the last result. Correct.
- **r117 on a gate that did not end DONE** (`supervise_rounds.py:91`). A non-DONE gate raises `Refused` before the approval question is built, so the question is only written on a DONE gate with no questions, as r117 says.
- **r110 loop** (`supervise.py:210-216`). After a fix, push and pull. A fix that is not green breaks the loop with no review, and analysis is not reached, because the kept review still lists findings. Otherwise `branch_review()` runs again, and a review that lists nothing goes to analyse and set_done (r75, r76, r105). This matches r110, r74 and r111. There is no bound on a reviewer that never lists nothing; no line names one, and the plan and report name it as an open case.
- **The approval question's words** ("Are the lines of pN approved as drafted? Readings: approve pN as drafted (recommended), or change its lines.") serve r117. This is not code that no line asks for.

## Tools

- `tools check --base 85065878`:
  - ruff: 4 items: `supervision_proposal_steps.py:118` RUF100, `test_supervision.py:14` I001, `stub_claude.py:189/190` FURB167.
  - vulture: 1 item, `supervision_proposal_steps.py:73` `base`.
  - import-linter: the project states no contracts.
  - None of these is on a line the commits added or changed. Each is a context line of the diff, already there before.
- `tools size --limit 300`: printed nothing.

## Commands run

- `git log --format='%h %H %s' -25`
- `git show --stat 87cdf5a2 8d0d6bbe 3d9bca9e`
- `git diff --stat 1f4a0731 b1b8562c`
- `git diff --stat 87cdf5a2^ 3d9bca9e`
- `git diff 1f4a0731 b1b8562c`
- `git diff 3d9bca9e b1b8562c -- <files>`
- `grep -n started_agents tests/scripts/stub_claude.py`
- `sed -n 80,125p scripts/supervise_rounds.py`
- `grep` of supervision.md for r19, r74, r75, r110, r111, r117
- Grep of features for `is green$`, `## Questions holds`, `limit of .* turns`
- `python3 <Scripts>/tools check --base 85065878…`
- `python3 <Scripts>/tools size --limit 300`
