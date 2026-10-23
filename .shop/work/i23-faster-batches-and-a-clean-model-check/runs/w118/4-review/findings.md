# Review of w118: no w_unserved_cap while the context has no job

**Verdict: DONE.** No Critical finding, no fix-now finding. The commit makes the plan's change and nothing else. r111 holds: `w_unserved_cap` now fires only when a `job` node exists. Under r19 no job node is read today, so the warning never prints.

## Commits reviewed

The branch `work/w118` is gone (`git log ... work/w118` gave "unknown revision"). So the commits are the ones between `547bbe0 work: w118 ready -> claimed` and `2956851 work: w118 claimed -> done` on HEAD:

- `8a32a57 model check: no w_unserved_cap while the context has no job`. This is the only non-`work:` commit, and it matches the implementer's `result.json` `commits` exactly.
- `2956851` (the `work:` commit) touches only `.shop/work/...` files: the log, the run files and the work-item status.

Files: `scripts/model.lp`, `docs/design-model/grammar.md`, `tests/scenarios/design_model_check_given.py`, `tests/scenarios/design_model_check_then.py`, `tests/scripts/test_model_output.py`. All of them are in the work-item's fileset and the plan's section 2. Nothing changed under `features/`.

## Removed and weakened tests

None removed or weakened. I checked the diff of `tests/` between 547bbe0 and 2956851 for deleted `def test_`, dropped parametrize cases, removed or loosened `assert`/`assertEqual`, and added `skip`/`xfail`. It has 12 insertions and 0 deletions.

- `tests/scripts/test_model_output.py::CheckOutputTest::test_check_ends_with_the_four_counts`: its fixture changed, not the test itself. One line was added, `self.observation()`.
  - Before, it proved the last line `1 violations, 1 warnings, 1 unresolved references, 1 file problems`, and its one warning was `w_unserved_cap`.
  - After, it proves the same line, and the one warning is now `w_uncited_obs`.
  - The assertion and the expected value are unchanged, so the test is as strong as before.
  - The plan lists it under "Tests the decisions break" (section 4).

## Allowances

- `test_check_ends_with_the_four_counts`, "fixture only (plan-listed)": **holds.** The diff adds, removes and changes no `assert`, no expected value and no parametrize case. The plan lists the test in any case.

## Cannot verify

- The report says the suite at the start was "722 passed, 1 failed". I did not run the whole suite (by brief), so I cannot check that figure.

## Findings

None.

Things I checked that gave no finding:

- **Risk: the new Then's regex overlaps an existing step.** I grepped every `@then` with "the output" in `tests/scenarios`. The only near ones are `"the output does not name v_s3"` and `"the output gives w_uncited_obs ..."`. Neither matches "the output does not give w_...". No overlap.
- **Risk: the gate is never open, or opens on something other than a job.** `scripts/model_facts.py:26` lists `job` in `KINDS`. A Markdown file with an `id` and `kind: job` under the paths r19 reads would therefore make a `job` node and open the gate. That matches r111's "while the bounded context has no job" and the plan's D1. With one bounded context, "a job in the model" and "the context has a job" are the same thing.
- **No behaviour without a line.** The only behaviour change is the r111 gate. When a job exists, the rule warns as it did before. The plan names that case as open, with no scenario.
- `grammar.md:198` gets the same gate as `model.lp:276`, so the two stay in agreement as the Implementation section asks.

## Commands run

- `git log --format=%H -1 --grep="^work: w118 ready -> claimed$" work/w118`: failed, the branch is gone.
- `git log --oneline -15 --grep=w118` and `git log --oneline -8`: found 547bbe0, 8a32a57 and 2956851.
- `git show --stat 8a32a57`, `git show 8a32a57 -- . ':!.shop'` and `git show --stat 2956851`: read the commits.
- `git diff 547bbe0 2956851 --stat -- features/ tests/`: 3 test files, 12 insertions, nothing under `features/`.
- `grep` of `spec/capabilities/design-model-check.md` (r111, r19, Not yet), `sed -n 70,85p features/design-model-check.feature`, a `grep` of the step texts in `tests/scenarios`, and a `grep` of `"job"` in `scripts/model*.py`.
- `python3 -m pytest -q -n 0 "tests/scenarios/test_design_model_check.py::test_a_bounded_context_with_no_job_gets_no_unservedcapability_warning" tests/scripts/test_model_output.py`: 9 passed, 5 subtests passed.
- `python3 <Scripts>/tools check --base 547bbe0`:
  - ruff: All checks passed.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `python3 <Scripts>/tools size --limit 300`: no output, so no file is over the limit.
- `git status --short`: clean.
