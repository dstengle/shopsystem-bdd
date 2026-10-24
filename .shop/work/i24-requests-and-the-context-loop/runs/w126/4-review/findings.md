# Review of w126: work request (requests r1-r5)

**Verdict: DONE_WITH_CONCERNS.** The change does what r1-r5 ask, and its 10 scenarios pass. Nothing is Critical, and no
test is removed or weakened. One finding is triaged fix now: `work request` with a `--lines` file that does not exist
crashes with a Python traceback where a refusal belongs (work-queue r7).

## Commits reviewed

The branch `work/w126` is gone, so the commits are those between `b1c11fe` (`work: w126 ready -> claimed`) and
`f348285` (`work: w126 claimed -> done`) on HEAD, less `work run`'s own `work:` commits:

- `97a0cec` work request: take in a request, refusing a line not in strict form or one with no origin (requests r1-r5)
  - CLAUDE.md (1 row), scripts/work (+13/-1), scripts/workqueue_request.py (+29), tests/scenarios/requests_write_steps.py
    (new, 108 lines), tests/scenarios/test_requests.py (+1 import).

The implementer's result.json lists `"commits": ["see git log"]` and not the commits themselves. The git log shows one
implementer commit, and it matches the report's `## Changed`. Nothing differs between them, but the result lists no
hashes (Minor, below).

No change under `features/` (`git diff b1c11fe f348285 --stat -- features`: empty).

## Removed and weakened tests

None. What I searched for: the commit's diff of `tests/`. It adds one new module (`requests_write_steps.py`) and one
import line in `test_requests.py`. It deletes no test function and drops no parametrize case. It removes or loosens no
assertion and adds no skip or xfail. No other test file changes.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commit changes no existing test, so that holds.
`requests_write_steps.py` is new and outside the work-item's fileset. The plan allows it ("If it nears the 300 line
limit, split by concern … each `requests_*_steps.py`"), and the report names it under "Outside the file set".

## Cannot verify

- The report's "Final: `pytest -q -n 0 --work-item w126` -> 152 passed, 1 skipped". I did not rerun it (no whole-suite
  runs). I ran only `tests/scenarios/test_requests.py`: 10 passed.
- I could not run `work request` itself on a scratch upstream (`scripts/work` by path, and `git init` for a scratch
  repository, were both refused in this session). So the probes in findings 1, 3, 4 and 5 are verified by reading the
  code, not by a run.

## Findings

### 1. Important, fix now: a missing lines file crashes instead of being refused
`scripts/workqueue_request.py:67` reads the lines file through `workqueue.read`
(`scripts/workqueue.py:48-53`). That function catches only `UnicodeDecodeError`. `scripts/work:128` catches only
`workqueue.Refused`. So `work request t --from a --lines no-such-file --source o1` ends on an uncaught
`FileNotFoundError` traceback (and a directory raises `IsADirectoryError`). Nothing is written, because the read comes
before every write. But work-queue#r7 asks that `work` "exit with an error, say why, and change nothing" when it cannot
do what it was asked. Every other refusal of `work` goes through `Refused`, and a mistyped `--lines` path is an ordinary
input from an asker.
**Fix:** in `request`, refuse a `--lines` path that is not a readable file (`Refused("the lines file %s is missing" …)`),
or catch `OSError` in `workqueue.read` and raise `Refused`.
Verified by reading. The probe run was refused (see Cannot verify).

### 2. Minor, observation: the origin step ignores the origins the scenario names
`tests/scenarios/requests_write_steps.py:61-67`: `names_origin` takes `named` from the scenario's Examples but asserts the
fixed `o1, o2` / `t1`. vulture flags it: `requests_write_steps.py:62: unused variable 'named' (100% confidence)`, which
fails `tools check`. Today the step is right, because the Examples name exactly those values. A changed Examples row
would still pass on the old values, though.
**Fix:** derive the expected `source: [...]` / `part_of: ...` from `named`.
Reproduction: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base b1c11fe…` -> the vulture line above, exit 1.

### 3. Minor, observation: `--source` and `--thread` together silently drop the sources
`scripts/workqueue_request.py:73`: when `thread` is given, `origin` is `part_of: <thread>` and the `--source` values are
discarded with no warning. No line names this case (the plan's open case 1). It loses input the asker gave, so it is
worth a line (refuse, or keep both).
Verified by reading.

### 4. Minor, observation: an empty or all-blank lines file writes a request with no lines
`scripts/workqueue_request.py:67-70`: blank lines are filtered out and an empty list passes the strict-form loop. The
result is a request `q<n>` with an empty `## Lines`. No line names this (the plan's open case 3).
Verified by reading.

### 5. Minor, observation: a newline in the title, `--from`, `--source` or `--thread` is written into the frontmatter
`scripts/workqueue_request.py:74-76` formats the values into the frontmatter and heading unchecked. A newline adds
frontmatter keys or sections. `work add` refuses such values for its own fields. No line names this (the plan's open
case 4).
Verified by reading.

### 6. Minor, drop: the plan said no commit, and the code commits
Plan decision 2 says `work request` does not commit in w126. The code commits through `workqueue.committed`. The commit
serves requests#r12, a line of the capability, and w128, which adds the commit to the other request commands, is
already done. The report says so ("commits it (as the other request commands do)"). This is consistent with the
capability, so it is not code no line asks for. I note it only as a departure from the plan.

### 7. Minor, drop: the implementer's result lists no commits
`3-implement/result.json`: `"commits": ["see git log"]` instead of the commit hash (`97a0cec`).

## Behaviour against the lines

- r1: writes `q<n>` with `status: open`, `turn: upstream`, `asker`, and `source: [...]` or `part_of`, the lines
  numbered under `## Lines`, and prints `q<n>`. Holds.
- r2: `model_parse.ears` both flags, first failing line named "line N". Holds. Every check runs before any write.
- r3: no `--source` and no `--thread` is refused before reading anything. Holds.
- r4/r5: the asker's lines are written only by `request`, and outcome/turn/resolve (w128) are unchanged. Holds.
- Purpose: `work` does not judge lines beyond the strict-form check r2 asks for. Holds.
- No code without a line: none found (the commit serves r12).

## Checks

- `tools check --base b1c11fe`: ruff, all checks passed. vulture, one hit (finding 2). import-linter, the project
  states no import contracts.
- `tools size --limit 300`: no file over the limit (no output).

## Commands run

- `git log --format=%H -1 --grep="^work: w126 ready -> claimed$"` -> b1c11fe
- `git log --stat b1c11fe..work/w126` -> unknown revision (branch gone)
- `git log --format='%H %s' -1 --grep="^work: w126 claimed -> done$"`, `git log --format='%H %s' b1c11fe..HEAD`
- `git show --stat 97a0cec`, `git show 97a0cec -- scripts CLAUDE.md`, `git show 97a0cec -- tests`
- `git diff b1c11fe f348285 --stat -- features` -> empty
- `grep` of `scripts/workqueue.py` (read, committed, context_path) and `scripts/work` (except handlers)
- `python3 -m pytest -q -n 0 tests/scenarios/test_requests.py` -> 10 passed, 13 deselected
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base b1c11fe…` -> vulture 1 hit, exit 1
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` -> nothing over
- Refused: `python3 scripts/work --root … request … --lines missing.md` and `/home/vscode/shopsystem-bdd/scripts/work …`
