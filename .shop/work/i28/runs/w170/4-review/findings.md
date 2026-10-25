# Review of w170

**Verdict: DONE_WITH_CONCERNS.** r103 and r104 hold. r102 does not hold where it counts: `supervise_drafts.added_by_others` looks for kept drafts at `<k>-integrate/drafts/spec/capabilities/*.md`. The integrate rounds in this repository actually keep them at `<k>-integrate/drafts/round-<n>/spec/capabilities/*.md`. So on the real queue the integrate brief gives "none" for exactly the collision r102 was written for: i25's and i26's drafts both add supervision r98. Graded Important, triaged fix now.

## Commits reviewed

The `work/w170` branch is gone. The commits are the ones on HEAD between `35c5249d work: w170 ready -> claimed` and `cc96ae81 work: w170 claimed -> done`:

- `bcc41527` work run starts the initiative of an accepted request no initiative fulfils (supervision r103)
- `55eea183` an integrate round is given the ids other initiatives' kept drafts add (supervision r102)
- `2e0f2555` the gate brief names its proposal's adds, changes and removes (supervision r104); module map row

The implementer's `result.json` lists no hashes (`"commits": ["see git log: r103, r102, r104 commits on work/w170"]`). Its three descriptions match the three commits above. No other commit is there. Every file touched is in the work-item's fileset. Nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff for:
- deleted `def` lines in `tests/`,
- dropped parametrize cases,
- removed or loosened `assert` lines,
- `skip` or `xfail` added.

The only deleted lines in `tests/` are three import lines, each replaced by a wider import. Every other test change adds new step definitions.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test's assertions changed.

## Cannot verify

- The report's full-suite figures ("863 passed, 3 failed" at start; "145 passed, 1 skipped" for `--work-item w170`; 271 for the `--whole-suite` run). I did not run the suite; `work run` runs it. I ran only the three scenarios of this work-item: 3 passed.
- What r103 does in a real `work run` (a real `work start` commit, then the push in `push_unpushed`). Only the fixture scenario shows it.

## Findings

### 1. Important, fix now: r102 misses the drafts integrate rounds really keep
- **Where:** `scripts/supervise_drafts.py:29`, the glob `stage.glob("drafts/spec/capabilities/*.md")`.
- **What is wrong:** The real kept drafts sit one level deeper, under `drafts/round-<n>/`. For example:
  - `.shop/work/i25/runs/i25/2-integrate/drafts/round-1/spec/capabilities/supervision.md`
  - `.shop/work/i26/runs/i26/2-integrate/drafts/round-1/spec/capabilities/supervision.md`

  The glob finds neither, so `added_by_others` returns `[]`. i1's integrate brief then says "none", although both drafts hold `[r98]` and `spec/capabilities/supervision.md` does not (`grep -c "\[r98\]"` gives 0). The scenario passes only because its Given writes the drafts at the shallower path the code reads. This is a wrong answer for supervision#r102, and it is the collision the ledger names (observation 2026-10-25-loop-collisions).
- **Fix:**
  - Read every `drafts/**/spec/capabilities/*.md` under the last integrate stage, or the last `round-<n>` under `drafts/`.
  - Make the scenario's Given in `tests/scenarios/supervision_integrate_steps.py` (`other_initiative`) write the `round-<n>/` layout the rounds produce, so it fails on today's code.

### 2. Minor, observation: an integrate stage with no drafts hides an earlier one's drafts
- **Where:** `scripts/supervise_drafts.py:16-19`, `last_integrate`.
- **What is wrong:** It takes the highest-numbered `<k>-integrate` directory whether or not that directory has drafts. An initiative whose integrate round was re-run and dispatched no writer has drafts only in an earlier stage. The ledger records such re-runs for i27 and i28, which were bootstrapped by hand. For that initiative, `added_by_others` gives no ids.
- **Reproduction:** `ls .shop/work/i25/runs/i25/1-integrate` lists only brief.md, result.json and session.json. So the order of stages matters to the result.
- **Fix:** Take the last integrate stage that has drafts.

### 3. Minor, drop: lint the commits introduce
`tools check --base 35c5249d` reports these, all new in these commits:
- `scripts/supervise_brief.py:3` I001: `import supervise_drafts` is placed after `import workqueue`.
- `tests/scenarios/supervision_intake_steps.py:65` FURB167: `re.M`.
- `tests/scenarios/supervision_proposal_steps.py:96` RUF100: an unused `# noqa: E731`.

These were there before the commits:
- `scripts/supervise_brief.py:82` ISC004 (it was line 74 at the base).
- `tests/scenarios/supervision_integrate_steps.py:107` and `:112` FURB167.

### 4. Minor, drop: the implementer's result lists no commit hashes
- **Where:** `.shop/work/i28/runs/w170/3-implement/result.json`
- **What is wrong:** `commits` is `["see git log: ..."]` rather than hashes. I matched the commits by their messages instead.

## Risks checked, with no finding

- **Lists in the gate brief (r104).** If `frontmatter` returned strings, `", ".join(data.get(kind))` would split each id into letters. `model_parse.frontmatter` parses `[a, b]` into lists, so the join is correct.
- **Which requests r103 starts.** `unfulfilled` reads `workqueue.requests`, the same source `supervise_intake.intakes` uses for the requests this context is the upstream of. `fulfils` is matched on its last path segment, as in `supervise_rounds`. Requests are written as `request/<context>/<q>` (`workqueue_request.py:88`).
- **Refusals before the start (r10).** In `run_all`, every open run's `Run.check` and every unfulfilled request's `Intake.check` (worker marker, detached HEAD, loose `.shop/work/`) run before the first `workqueue_start.start`.
- **Code no line asks for.** None. Each change serves r102, r103 or r104.

## Checks
- `tools check --base 35c5249d`:
  - ruff: 6 errors, 3 of them new (finding 3).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: prints nothing. The largest file touched is `tests/scenarios/supervision_integrate_steps.py`, at 170 lines.

## Commands run
- `git log --format='%H %s' -1 --grep="^work: w170 ready -> claimed$"` (and the same for `claimed -> done`); `git log --format='%h %s' -15`
- `git log --stat 35c5249d..cc96ae81`; `git diff 35c5249d 2e0f2555`
- `grep` in `scripts/workqueue.py`, `scripts/supervise_intake.py`, `scripts/workqueue_start.py`, `scripts/supervise_brief.py`, `scripts/model_parse.py`, `scripts/workqueue_request.py`
- `ls -R .shop/work/i25/runs/i25/2-integrate`; `ls -d .shop/work/i*/runs/i*/*-integrate`
- `grep -o "^- \[r9[0-9]\]..."` on i25's and i26's draft `supervision.md`; `grep -c "\[r98\]" spec/capabilities/supervision.md` → 0
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 35c5249d`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` on the touched files
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "kept_drafts_add or no_initiative_fulfils or only_for_the_questions"` → 3 passed
