# Review of w175 (requests#r22, an empty delegation refused)

**Verdict: DONE.** No Critical finding, none triaged fix now. The change does what r22 and the person's answer
(reading B) ask, and nothing more.

## Commits reviewed

The branch `work/w175` is gone. The claim commit is `a39bb7a0` ("work: w175 ready -> claimed"), and the done commit
is `c2ea4a21` ("work: w175 claimed -> done"), both on HEAD. Between them, the only commit that is w175's is:

- `959cba20` work request refuses an empty delegation (requests r22): `scripts/workqueue_request.py` +2,
  `tests/scenarios/requests_write_steps.py` +5.

The other commits in that range are other work-items' or `work run`'s own (w179, w181, i26/i27/i28 branch reviews,
the i30/i31 spec applies, `work note`).

The implementer's results list `eef9320a` (4-implement) and `72bd6f14` (5-implement), not `959cba20`. All three
commits have the same message, author and date, and their diffs are identical, with the same blob ids
(`aaf59622..61aff1bb`, `dea17e9a..c00f7c6c`). They are the same change re-created when the branch was rebased or
merged again. See finding M1.

## Removed and weakened tests

None. The diff adds one step definition (`refused_empty_delegation`) and removes or changes nothing in `tests/`.
I looked for removed `def`/`assert` lines, parametrize changes, and skip/xfail marks in `git show 959cba20`: there are
none. Nothing under `features/` changed.

## Allowances

Both reports list "Tests changed under an allowance: none". The commits agree: no existing test was touched.

## Cannot verify

- The whitespace-only case (`--delegation "   "`) is not run by any scenario. The scenario at
  features/requests.feature:33 uses `""`. Reading the code, it is covered: `not delegation.strip()` refuses both.
  The plan's D-c says so too. I could not run a probe of it: a probe needs a scratch git repository, and this shell
  does not allow `git init`.
- The implementer's suite figures (867/868 passed, 6 failures in test_supervision.py, r105-r109). The brief's answer
  says these failures are w181's, and `work run` reran the suite before merging.

## Findings

### M1. Minor (drop): the commits in the result differ from the commit that landed
- Where: `.shop/work/i29/runs/w175/4-implement/result.json` (`eef9320a`), `5-implement/result.json` (`72bd6f14`);
  the commit that landed is `959cba20`.
- What: none of the hashes in the results is the commit on HEAD.
- Why it matters: little. The content is byte-identical (same blob ids), so the difference comes from the branch being
  re-created, not from a different change.
- Fix: none needed. `work run` could record the commit that lands after the merge.

### M2. Minor (observation): the refusal order with several faults is not pinned
- Where: `scripts/workqueue_request.py:93`.
- What: the empty-delegation check runs before the origin check (r3) and the line check (r2). A run that has both an
  empty delegation and no `--source`/`--thread` is refused naming only the delegation.
- Why it matters: no line names an order, and either refusal changes nothing, so the behaviour is not wrong. The plan
  left this open (§5) and the report names it.
- Reproduction (from the code): `work request T --from a --lines l.md --delegation ""` with no `--source` is refused
  with "the delegation is empty".
- Fix: none now.

No Important finding. Checks against the rules and decisions:
- r22: the refusal comes before any write, commit or q-number, so "change nothing" holds.
- Decision 0055: `Refused` exits with an error, like the other refusals.
- Decision 0067: the refusal is in `workqueue_request.request()`, the library behind `work`.
- r19: a delegation with text is written as given. An absent `--delegation` (argparse default `None`, scripts/work:139)
  is not checked, so a request with no delegation still works.
- The code has no behaviour that no line asks for. The words of the message are mechanism.

## Checks
- `tools check --base a39bb7a0`:
  - ruff: 2 SIM115 errors, both in `.shop/work/i31/runs/supervision/2-apply/apply.py`. That file is not in w175's
    commits; it belongs to i31's apply round.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing (no file over the limit).

## Commands run
- `git log --format=%H -1 --grep="^work: w175 ready -> claimed$"` gave `a39bb7a0`.
- `git log --oneline a39bb7a0..HEAD` and `git log --grep="^work: w175 " HEAD`.
- `git show 959cba20`, `git diff 72bd6f14^!`, `git diff eef9320a^!`, `git show --stat` of each.
- `grep` of r22 in `spec/capabilities/requests.md`, of the delegation scenarios in `features/requests.feature`, and of
  the `delegation` callers in `scripts/`.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base a39bb7a0…`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q tests/scenarios/test_requests.py -k delegation` gave 1 passed.
