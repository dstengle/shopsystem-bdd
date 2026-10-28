# Review of w225 (third review, 8-review)

**Verdict: DONE.** No finding is Critical and none is fix now.

The commit makes the change the person's delegated answer asked for. `glossary_only_done` now skips `ledger.md`, as `model_work.py:142` and `workqueue_status.py:41` do. The r161 Given now writes a ledger line, so the scenario covers the real case and has stopped passing vacuously. The commit also removes the unused `noqa` that the 6-review flagged as finding 4. Nothing changed under `features/`. No test was removed or weakened.

## Commits reviewed
- 8322c119 `work run: glossary-only done skips ledger.md (r161)`. Its parent is 760741c5 `work: w225 ready -> claimed`.

This is the commit the brief's `Commits:` gives and the one the implementer's result (7-implement) lists. The suite result comes from the brief's suite record: 1070 passed, 0 failed at 8322c119. The expected failures are w212's parked requests scenarios.

The diff touches three files:
- `scripts/supervise_glossary.py` (+2/−1);
- `tests/scenarios/supervision_done_steps.py` (+1);
- `tests/scenarios/supervision_proposal_steps.py` (one line changed).

All three are in the work-item's fileset.

## Removed and weakened tests
None.

What I searched for in the diff: deleted `def`s, dropped parametrize cases, removed or changed `assert`s and expected values, added skip or xfail, and rewritten Then steps.
- **`started_glossary_only`:** one `write` of `.shop/work/i1/ledger.md` was added. This makes the Given stricter, not weaker.
- **`glossary_drafted`:** only the `# noqa: E731` comment was removed.

## Allowances
- **`supervision_done_steps.py` `started_glossary_only`, "setup only": holds.** The diff adds one fixture write and no `assert`, expected value or parametrize case.
- **`supervision_proposal_steps.py` `glossary_drafted`, "comment only": holds.** The only change is the removed `noqa` comment, and the code is identical.

## Cannot verify
- That the r161 scenario was red after the Given changed and before the code fix. The report says 1 failed, 188 passed, and I did not reproduce that run. It is consistent with the 6-review's probe (`with ledger.md: False`), and the scenario is green now (my focused run, below).

## Findings
None from this commit.

Still open from the 6-review, not in this commit and not re-raised:
- finding 2: undelivered raised requests are not checked for a glossary-only initiative;
- finding 3: an abandoned initiative can be set done.

Both stay observations.

## Checks
`tools check --base 8322c119~1`:
- **ruff:** 2 errors, `supervision_proposal_steps.py:102` and `:137` RUF100. Both are already there, on lines this commit did not touch. The commit removed the third such `noqa`, the one at `:172`.
- **vulture:** `supervision_proposal_steps.py:66` reports an unused variable `base`. It dates from e0ba9852 (`git log -L`), not from this commit.
- **import-linter:** the project states no import contracts.

`tools size --limit 300` printed nothing, so no file is over the limit.

## Commands run
- `git show 8322c119`
- `git log --format='%h %s' -4 8322c119`
- `git log --format='%h %s' -L66,66:tests/scenarios/supervision_proposal_steps.py 8322c119`
- `grep -rn "ledger.md\|glossary_only_done" scripts/`
  - The risk checked: whether other readers skip `ledger.md` the same way, and who calls `glossary_only_done`. The skip matches `model_work.py:142` and `workqueue_status.py:41`, and the one caller is `supervise_done.py:32`.
- `python3 -m pytest -q -n0 -p no:cacheprovider tests/scenarios -k "glossary and done"`: 1 passed (the r161 scenario).
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 8322c119~1`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
