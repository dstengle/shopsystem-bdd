# Review of w216 (supervision r154-r157)

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now. The r156 commit attribution names capability-proposals as work-items. Nothing Critical, and nothing under `features/` changed.

## Commits reviewed

- `76403ad30cd6fe943358bb88231e13267d621dea`: "work run makes the branch review's runs first and gives the reviewer them, its commits and its files to read (r154-r157)". It is the commit given in the brief's `Commits:` line.
- The implementer's result lists `c8d0bb31` with the same subject, whose parent is `f75e428d` (`work: w216 ready -> claimed`). `76403ad3` is that commit rebased by the merge onto `d4ac1c25` (`work: w215 done -> green`). `git diff c8d0bb31 76403ad3 -- scripts tests CLAUDE.md agents` is empty, so the change is the same. This difference is not a finding.
- Suite, from the brief's record: 1030 passed, 0 failed at 76403ad3 in 34 s. The expected failures are all `test_requests.py` scenarios of the parked w212.

## Removed and weakened tests

None. I searched the diff for deleted `def test_`/step functions, dropped parametrize cases, removed or loosened `assert`s, and added `skip`/`xfail`. The three changed test helpers only widen what they can do, and their defaults behave as before:

- `tests/scenarios/supervision_given.py:66`: `under` falls back to `context["unders"]` before `"thing"`. Without that context key it is unchanged.
- `tests/scenarios/supervision_world.py:90`: `item_text` gains an optional `check=`. When it is not given the text is unchanged.
- `tests/scripts/stub_claude.py:220`: `elsewhere` is filtered by `work_item`, which defaults to the worker's own. When it is not given the behaviour is unchanged.

## Allowances

The report's `## Tests changed under an allowance` says "none". There are no rows to verify, and none was needed (see above).

## Cannot verify

- The report says the w216 module takes about 4.7 s and that each existing branch-review scenario now does the r154 runs. The plan asked for the suite's wall time before and after, and the report does not give it. The suite record says 34 s at 76403ad3, against 29 s at w215's merge (1b92df68).
- The report's targeted runs (`--work-item w20` 1 passed, `--work-item w134` 5 passed). I did not re-run them; the whole-suite record covers them.

## Findings

### 1. Important, fix now: capability-proposal transitions are attributed as work-items (r156)

- **Work-item:** w216.
- **Where:** `scripts/supervise_review_read.py:11` and `:41`.
- **What is wrong:** `TRANSITION = re.compile(r"^work: (\S+) \S+ -> \S+$")` matches any `work: <name> <a> -> <b>` subject. That includes capability-proposal transitions, and `commits_text` then gives the group as the commit's work-item. On this initiative's own range (`ebbf1bea..76403ad3`), the brief would give:
  - `d37e4da9 work: supervision awaiting-answer -> formulated` as belonging to work-item `supervision`;
  - `f6519d70 work: supervision approved -> awaiting-answer` and `0f219eca work: supervision awaiting-answer -> approved` the same way;
  - `a166380e work: review awaiting-answer -> formulated`, `05b9cc81` and `b234ec4d` as belonging to work-item `review`.

  None of these is a work-item. r156 asks for "each with the work-item it belongs to or none".
- **Why it matters:** this is a wrong answer in the brief. The branch reviewer is told to take attribution from the brief, and that a commit belonging to no work-item is a finding. So it is misled on every initiative that went through an apply or formulate round. The r156 scenario has no proposal transition in its range, so the suite does not catch this.
- **Fix:** take the transition's name only when it is a work-item of the initiative (`name in [n for n, _ in self.items()]`), and give `none` otherwise. Add a check (a scenario row or a `tests/scripts` test) with a `work: <proposal> approved -> awaiting-answer` commit in the range that expects `none`.

### 2. Minor, observation: the new code introduces ruff errors

- **Where:** `tests/scenarios/supervision_branch_steps.py:31,37,88,89,106,129,137` (FURB167 `re.M`), `:147` (PLC0206) and `:148` (PIE810). Also `tests/scenarios/test_supervision.py:27` (I001): the new `supervision_branch_steps` import is placed before `supervision_answers_steps`, which is out of order.
- **What is wrong:** these are new lint errors in the commit's own lines. The `stub_claude.py:196-197` FURB167 errors were already there at f75e428d (at its lines 195-196), so they are not w216's.
- **Fix:** `ruff check --fix` on the two files, and use `.items()` and a tuple `startswith` at lines 147-148.
- **Reproduction:** `python3 <Scripts>/tools check --base f75e428d…` reports 14 ruff errors, 12 of them from this commit's lines.

### 3. Minor, observation: `Ran at:` is read from the checkout, not from the worktree the runs ran in

- **Where:** `scripts/supervise_review.py:62` and `:67`.
- **What is wrong:** the worktree is created at the checkout's `HEAD` under `self.lock` (line 62). `head` is read from `self.root` afterwards, outside the lock (line 67). If another initiative's `Run` on the same checkout commits in between, `Ran at:` and `Head:` name a commit other than the one the runs ran at. The `Head:` line already had this race before w216, but r155 now names the commit the runs ran at.
- **Fix:** `git(tree, "rev-parse", "HEAD")`.
- **Reproduction:** none run. Found by reading `supervise_worker.worktree` (147-159) against lines 62 and 67.

### 4. Minor, drop: `tools size` is run with its default limit

- **Where:** `scripts/supervise_branch_runs.py:33`.
- **What is wrong:** `tools size` is run bare (default 300), not with the limit `CLAUDE.md` gives. Here the two agree. In a project with another limit, the run measures the wrong bound. r154 names `tools size` bare, and the report names this as an open case.

### Note (not w216's)

`agents/bdd-branch-reviewer.md:25` treats every commit belonging to no work-item as a finding. Under r156, `work run`'s own round and request commits (`work note`, `work answer`, `spec: apply …`, `features: … formulated`) are given as `none`, so every review will report them. That is the review capability's concern, not this work-item's.

## Code no line asks for

None found:
- The `OSError` guard (`supervise_branch_runs.py:41`) gives a run that cannot start as a run (r155).
- "The initiative has no base." (`supervise_review_read.py:37`) gives the r156 range when it is empty.

Both are mechanisms serving a line.

## Check results

- **tools check (`--base f75e428d`):**
  - ruff: 14 errors (finding 2).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- **tools size (`--limit 300`):** no output, so no file is over the limit.
- **features/:** untouched (no path under `features/` in the diff).

## Commands run

- `git show --stat 76403ad3`, `git show 76403ad3 -- <files>` and `git log --oneline -5 76403ad3`
- `git show --stat --format='%H %P %s' c8d0bb31` and `git diff c8d0bb31 76403ad3 -- scripts tests CLAUDE.md agents --stat`
- `git log --format='%h %s' ebbf1bea..76403ad3` (finding 1)
- `grep -n '"merged"' .shop/work/i43/log.jsonl`: the merged lines hold full SHAs, so the merged attribution matches `git log %H`
- `git show f75e428d:tests/scripts/stub_claude.py | grep -n re.M` and `git show f75e428d:tests/scenarios/test_supervision.py`
- `python3 <Scripts>/tools check --base f75e428d2aec0b663f3c74c46e1709303166a50f`
- `python3 <Scripts>/tools size --limit 300`
- `head -8 spec/capabilities/supervision.md` and `grep` of `agents/bdd-branch-reviewer.md`
