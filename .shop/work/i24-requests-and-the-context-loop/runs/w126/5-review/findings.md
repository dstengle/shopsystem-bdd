# Review of w126 (second review, after the person's answer): work request, requests r1-r5

**Verdict: DONE.** No finding is Critical, and none is still to be fixed now. This review covers the same single
implementer commit as the first review (4-review). The one fix-now finding of that review, a missing `--lines` file
ending on a traceback, was answered on 2026-10-24: accept as it stands, and deliver it later through a work-queue#r7
examples row and its own fix work-item. So it is not raised again as fix now. The Minor observations remain.

## Commits reviewed

The branch `work/w126` is gone (`git log -1 work/w126`: unknown revision). So the commits are those between `b1c11fe`
(`work: w126 ready -> claimed`) and `f348285` (`work: w126 claimed -> done`) on HEAD, less `work run`'s own `work:` commits:

- `97a0cec` work request: take in a request, refusing a line not in strict form or one with no origin (requests r1-r5).
  It touches CLAUDE.md (+1/-1), scripts/work (+12/-1), scripts/workqueue_request.py (+29),
  tests/scenarios/requests_write_steps.py (new, 108 lines) and tests/scenarios/test_requests.py (+1).

After done, the commits on w126 are only `28ea4a7` (done -> awaiting-answer) and `4fb3c0b` (work answer). No code changed
for w126 after the first review. The later code commits `4e5c8de` and `d23a6a4` belong to other work-items (requests
r13/r14, and model's reading of requests).

The implementer's result.json gives `"commits": ["see git log"]`, not the hash. The one commit matches the report's
`## Changed` (Minor, finding 6).

No change under `features/`: `git diff b1c11fe f348285 --stat -- features` gives nothing.

## Removed and weakened tests

None. I searched the commit's diff of `tests/` for deleted test functions, dropped parametrize or Examples cases,
removed or loosened asserts, and added skip or xfail. The diff only adds the new module `requests_write_steps.py` and one
import line in `test_requests.py`. No existing test file changes in any other way.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds, because no existing test changed.
`requests_write_steps.py` is outside the fileset. The plan allows it (the steps may be split as `requests_*_steps.py`), and
the report names it under "Outside the file set".

## Cannot verify

- The report's "`pytest -q -n 0 --work-item w126` -> 152 passed, 1 skipped". I did not rerun it, because the whole suite is
  out of scope for this review. `tests/scenarios/test_requests.py` gives 10 passed.
- I did not run `work request` on a scratch upstream. A run of `scripts/work` is outside the allowed commands, so the
  behaviour notes below come from reading the code, backed by the scenarios passing.

## Findings

### 1. Important, answered (was fix now): a missing `--lines` file crashes instead of being refused
`scripts/workqueue_request.py:67` reads the file through `workqueue.read`, which catches only `UnicodeDecodeError`.
`scripts/work:128` catches only `Refused`. So a `--lines` path that does not exist ends on a `FileNotFoundError`
traceback. This goes against work-queue#r7. The person answered on 2026-10-24: accept the work-item as it stands, and
deliver the fix through an examples row of work-queue#r7 and its own fix work-item. Nothing is left to do in this
work-item. The fix work-item is still to be drafted after that formulate round.

### 2. Minor, observation: the origin step ignores the origins the scenario names, and fails `tools check`
In `tests/scenarios/requests_write_steps.py:61-67`, `names_origin` takes `named` and then asserts the fixed `o1, o2` / `t1`.
So a changed Examples row would still pass against the old values. vulture reports
`requests_write_steps.py:62: unused variable 'named' (100% confidence)`, so `tools check` exits 1.
**Fix:** derive the expected `source: [...]` / `part_of: ...` from `named`.
Reproduction: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base b1c11fe` gives the vulture line above.

### 3. Minor, observation: `--source` together with `--thread` drops the sources without a word
At `scripts/workqueue_request.py:73`, when a thread is given only `part_of` is written. No line covers this case (plan,
open case 1). Found by reading the code.

### 4. Minor, observation: an empty or all-blank lines file writes a request with no lines
At `scripts/workqueue_request.py:67-70`, blank lines are filtered out, and an empty list passes the strict-form loop. No line
covers this case (plan, open case 3). Found by reading the code.

### 5. Minor, observation: a newline in the title, `--from`, `--source` or `--thread` goes into the frontmatter unchecked
`scripts/workqueue_request.py:74-76`. `work add` refuses such values for its own fields. No line covers this case (plan,
open case 4). Found by reading the code.

### 6. Minor, drop: the result lists no commit hash, and the request is committed against plan decision 2
`3-implement/result.json` gives "see git log" where the hash `97a0cec` belongs. The commit `work request` makes serves
requests#r12, and w128 already commits the other request commands. So this is not code that no line asks for. It
departs from the plan's decision 2, and the report says so.

## Behaviour against the lines and decisions

- r1: writes `q<n>` with `status: open`, `turn: upstream`, the asker, and `source: [...]` or `part_of`, numbers the lines
  under `## Lines`, and prints `q<n>`. This holds.
- r2: a line is refused unless both of `model_parse.ears`'s flags pass. The first failing line is named "line N", before
  any write. This holds.
- r3: a request with neither `--source` nor `--thread` is refused before any read or write. This holds.
- r4/r5: only `request` writes the lines. outcome, turn and resolve are unchanged. This holds.
- Purpose and decision 0067: the request is written only through `work`, and lines are not judged beyond r2. This holds.
  Decision 0055: refusals exit with an error through `Refused`, apart from finding 1.
- Code that no line asks for: none found.

## Checks

- `tools check --base b1c11fe`:
  - ruff: one hit, `tests/scenarios/test_design_model_check.py:7` I001. The w126 commit does not touch that file (a
    later commit on HEAD does), so it is not this work-item's.
  - vulture: one hit (finding 2).
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: no file is over the limit.

## Commands run

- `git log --format='%h %s' --grep=w126 HEAD` (claim `b1c11fe`, done `f348285`, then answer `4fb3c0b`)
- `git log -1 work/w126`: unknown revision (the branch is gone)
- `git log --format='%h %s' b1c11fe..f348285`
- `git log --format='%h %s' f348285..HEAD -- scripts tests features CLAUDE.md`
- `git show --stat 97a0cec`, `git show 97a0cec`
- `git diff b1c11fe f348285 --stat -- features`: empty
- `grep` of the r1 scenario in `features/requests.feature`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base b1c11fe`: exit 1 (ruff hit in another file, vulture hit)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output
- `python3 -m pytest -q -n 0 tests/scenarios/test_requests.py`: 10 passed
- `cat spec/decisions/0055-*.md spec/decisions/0067-*.md`
