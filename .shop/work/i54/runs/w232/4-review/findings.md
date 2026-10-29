# Review of w232 (work-queue#r59, #r60, #r61)

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now: `work show <request>` leaves out every line of the request that has no line outcome yet, so a request still waiting on outcomes is shown with none of its lines. No change under `features/`, and no test was removed or weakened outside the plan's list.

## Commits reviewed
- a5d6b59bd3a1bd818ca314a4bd9cb91f20e6bc2b "work show of a request prints its turn, line outcomes, questions, answers and resolution (r59)". It changes scripts/workqueue_list.py (+20), scripts/workqueue_request.py (+7), tests/scenarios/requests_flow_steps.py (1 line) and tests/scenarios/work_queue_list_steps.py (+56/-2).
- This matches the brief's `Commits:` and the implementer's result (`a5d6b59b`). `git log 7b1e1e12..a5d6b59b`, from the `ready -> claimed` commit, shows only this commit. Every file it touches is in the work-item's fileset.
- Suite (from the brief's record): 1070 passed, 0 failed at a5d6b59b. The expected failures are all requests.feature scenarios outside this work-item.

## Removed and weakened tests
What I searched for: deleted `def test_`/step functions, changed asserts, parametrize cases, skip or xfail, and changed step patterns in the diff.
- `tests/scenarios/requests_flow_steps.py:show_prints` (l.99) is loosened.
  - Before, it asserted that the whole stdout of `work show <request>`, split into words, was `<name> delivered asker`.
  - Now it checks only the first line.
  - **The plan lists it** under "Tests the decisions break" (part 4), with this same rewrite. It holds.
- `tests/scenarios/work_queue_list_steps.py:prints_question` (l.56): the pattern changed from `parsers.parse('it prints the question "{question}"')` to an anchored regex with `[^"]*`.
  - Before, it could match feature line 218 ("... and the answer ...") by swallowing the quotes.
  - Now that line goes to the new `prints_question_answer`, which asserts more: the question and the answer, each on its own line.
  - Line 204, its other use, still matches the same assertion.
  - Not weakened: what it matches is narrower and its assert is unchanged.
- Nothing else was removed or weakened. No skip or xfail was added.

## Allowances
The report's `## Tests changed under an allowance` says "none", and none is needed: `show_prints` is in the plan's list, and `prints_question` is not weakened. Nothing to verify.

## Cannot verify
- The report's red run before the code (`AssertionError: q1 delivered asker` at "it prints that it is the asker's turn"). The commit holds steps and code together, so the red state is not in the history.
- `work show` on this repository's real requests. Running `python3 scripts/work` needs approval in this session, so I did not run it. Instead I read `.shop/work/requests/q9.md` and checked that its sections have the `<n>. <text>` form that `sections` parses.

## Findings

### 1. Important, fix now: lines with no line outcome are not printed (w232)
- **Where:** scripts/workqueue_list.py:85-88, in `request_parts`.
- **What is wrong:** `outcome = parts["Outcomes"].get(number); if outcome is not None: print(...)` prints a line only when it has an outcome.
  - A request whose lines do not all have outcomes yet is shown with only some of its lines.
  - A request with no outcomes at all is shown with none.
  - requests#r17 names this state: a turn passed to the asker "with a line that has no line outcome" (`awaiting-asker`). So does every request before the upstream writes its outcomes.
- **Why it matters:** work-queue#r59 says `work show <request>` "shall print ... its lines with their line outcomes". `show` is how a session finds out where a request stands, and here it gives a wrong answer: a request with lines appears to have none. The report gives this as an open case it decided ("Line with no outcome (not printed)"). The plan left that case to be named, not chosen.
- **Fix:** print every line under `## Lines`, with its outcome where it has one and a stated "no line outcome" where it has none (for example `line 2: (no outcome) - <text>`). Add a test with a line that has no outcome.
- **Reproduction (by reading):** take a request file with `## Lines` 1. and 2. and `## Outcomes` holding only `1. accepted`. `request_parts` iterates the Lines, finds `parts["Outcomes"].get("2")` is None, and prints nothing for line 2.

### 2. Minor, drop: docstrings not updated (w232)
- tests/scenarios/work_queue_list_steps.py:1 still names "(r34-r39)". The plan (part 2) asked for it to name r59.
- scripts/workqueue_list.py `show`'s docstring still says "an initiative or a work-item", though it now prints a request's parts.
- The fix is a cheap doc edit, but nothing behaves differently.

### 3. Minor, observation: a request with no `turn:` field prints "it is the None's turn" (w232)
- **Where:** scripts/workqueue_list.py:83.
- Every request in this repository has a `turn:` field (`grep -h "^turn:"`: 18 asker, 23 upstream, none missing). So this input reaches no client today.
- **Reproduction (by reading):** `workqueue.requests` yields `data.get("turn")`, which is None when the field is missing. `"it is the %s's turn" % None` then prints "it is the None's turn".

### Behaviour and unrequested code
- Every new output serves r59: whose turn it is, the lines with their outcomes, the questions and answers, and the resolution. Leaving `--json` as it is (D4) adds nothing.
- r60 and r61 are unchanged and green, per the suite record.
- No code is unrequested.

## Checks
- `tools check --base 7b1e1e12`:
  - ruff: 1 error, tests/scenarios/work_queue_list_steps.py:134 RUF015. `git blame` gives commit a033c4608 (2026-10-27), so the error was there before w232 and is not this work-item's.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: no output. No file is over the limit.

## Commands run
- `git show --stat a5d6b59b`, `git show a5d6b59b`
- `git log --format=%H -1 --grep="^work: w232 ready -> claimed$"` (gives 7b1e1e12), `git log --oneline 7b1e1e12..a5d6b59b`
- `git blame -L 130,136 a5d6b59b -- tests/scenarios/work_queue_list_steps.py`
- reads of the work-item, the capability (work-queue.md), the feature's r59 scenario, the research notes, the plan, the report and its result, scripts/workqueue_request.py, scripts/workqueue.py:requests and .shop/work/requests/q9.md
- greps over .shop/work/requests (statuses, turns, empty Outcomes) and spec/capabilities/requests.md (r17)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 7b1e1e12...`, `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 scripts/work show q9`: refused (needs approval), so not run
