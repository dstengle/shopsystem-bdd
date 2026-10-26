# Review of w197 (requests r7, r23, r24)

**Verdict: DONE.** No Critical finding, none triaged fix now. One Minor observation.

## Commits reviewed

The branch `work/w197` is gone. The claim commit is `b6815a57` (`work: w197 ready -> claimed`) and the done commit is `5575df89` (`work: w197 claimed -> done`). Between them is one commit:

- `9237a0f9` requests: accepted keeps the upstream's turn (r23), resolve passes it to the asker (r24), r7 narrowed; retire deprecated r7
  - features/requests.feature: -13
  - scripts/workqueue_request.py: +4 -1
  - tests/scenarios/requests_steps.py: +5 -1

This matches the implementer's `result.json` (`commits: ["9237a0f9 ..."]`) and the report's `## Commits`. Every file is in the work-item's fileset. `5575df89` holds only `work run`'s run records and the status change in w197.md.

## Removed and weakened tests

I looked for deleted test functions, removed scenarios or Examples rows, changed `assert`s, and added skip or xfail. I found two:

1. **The deprecated r7 Scenario Outline "turn passes the request's turn from the <side> to the <other side> (deprecated)"** was removed from `features/requests.feature`, with both Examples (`upstream-asker`, `asker-upstream`). Its generated tests `test_turn_passes_..._deprecated[...]` go with it.
   - Before, it proved that `work turn` hands the turn to the other side, whatever the status.
   - The work-item lists it under Retires, and the plan lists it under "Tests the decisions break" (decision 5).
   - The other change under `features/` is nil: the hunk is only this removal.
2. **`status_is` in `tests/scenarios/requests_steps.py:69-75`.** It used to assert only `status_of == status`. Now the words "not accepted" assert `!= "accepted"`, and every other word still asserts equality.
   - It passes on more than it did only for the literal "not accepted". The only scenario using that wording is the new r7 one, at features/requests.feature:126. Before the change it could never pass, because no status is the string "not accepted".
   - The plan lists it under "Tests the decisions break" (decision 4).

No skip or xfail was added and no other assert changed.

## Allowances

The report's `## Tests changed under an allowance` is "none". Both test changes above are listed in the plan, so no allowance is needed.

## Cannot verify

- The report's suite figures: "924 passed, 4 failed" at the start and "148 passed, 1 skipped" with `--work-item w197`. I did not run the whole suite, by instruction; `work run` ran it before merging.

## Findings

### 1. Minor: docstrings of `turn` and `resolve` not updated (observation)

- **Where:** scripts/workqueue_request.py:149-150 and :167-168.
- **What is wrong:** `turn`'s docstring still says "Pass the turn to the other side (r7) ... To the asker, the upstream ending its turn with every line settled sets the status (r8, r9)". It does not say that the end that sets `accepted` keeps the turn (r23). `resolve`'s docstring does not mention the asker's turn (r24). The plan (§2) said "Both docstrings name r23 / r24". Only inline comments do (`# r23: ...`, `# r24`).
- **Why it matters:** the docstring now misdescribes the accepted case to a reader. Behaviour is not affected.
- **Fix:** add r23 to `turn`'s docstring and r24 to `resolve`'s.
- **Reproduction:** `sed -n 148,151p scripts/workqueue_request.py` shows the old wording.

### Checked and found sound

- **r23:** the new early `return text` at :158-159 runs only in the upstream's turn: the asker's case returned at :153. It runs only when the request is not `delivered` and every line is settled with at least one accepted, which is r8's condition. Upstream ends that set `refused`, `awaiting-asker`, or end on a `delivered` request still pass the turn to the asker. That is r7 narrowed, r9 and r17.
- **r24:** `resolve` sets `turn: asker` in the same edit as `delivered`, so the one commit of r12 holds both.
- **Code no line asks for:** none. Each behavioural change maps to r23 or r24.
- **Risk checked:** I looked for other code that expects the asker's turn after an accepted `work turn`. `grep` for `work turn` and `turn` found `supervise_intake.py`, `supervise_worker.py` and `model_requests.py`. None assumes the turn after acceptance. Intake's WAITING set is a plan open case, already named.
- **`tools check`:** ruff: all checks passed. vulture: clean. import-linter: the project states no import contracts.
- **`tools size --limit 300`:** printed nothing.
- The focused scenarios for r7 (both Examples), r23 and r24 pass.

## Plan open cases, carried

These were named by the plan and the report and are not findings of this work:
- After acceptance, `work outcome` and `work ask` remain open to the upstream, and the effect of an outcome changed on an accepted request is unspecified.
- Intake does not rerun an accepted request left in the upstream's turn.
- `work request` accepts a request with no lines (notes D1).

## Commands run

- `git log --format=%H -1 --grep="^work: w197 ready -> claimed$"` gave b6815a57.
- `git log --format=%H -1 --grep="^work: w197 claimed -> done$"` gave 5575df89. `git log --oneline b6815a57..HEAD` listed the commits in between.
- `git show --stat 9237a0f9`, `git show 9237a0f9 -- scripts tests features`, `git show --stat 5575df89`.
- `sed -n 140,185p scripts/workqueue_request.py`, plus `grep` over features/, tests/ and scripts/ for "not accepted", `@r7/@r23/@r24` and `turn`.
- `python3 <Scripts>/tools check --base b6815a57...`: ruff passed, vulture clean, no import contracts.
- `python3 <Scripts>/tools size --limit 300`: no output.
- `python3 -m pytest -q tests/scenarios/test_requests.py -k "accepted or delivered or turn" -rA`: 4 passed (r23, r24, r7 ×2).
