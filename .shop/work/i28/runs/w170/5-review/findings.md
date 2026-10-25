# Review of w170 (second review, after the answer)

**Verdict: DONE.** This review finds nothing new that is Critical or to be fixed now.

The previous review's one fix-now finding was that r102 reads kept drafts at the wrong path. It has been answered under the person's delegation:
- r102's scenario was reformulated in 7636eb12 with the real `drafts/round-<m>/` layout.
- Fix work-item **w171** (drafted, accepts supervision#r102) delivers the code change.

It is carried below as answered and is no longer triaged fix now for w170. r103 and r104 hold.

## Commits reviewed

The `work/w170` branch is gone (`git branch --list work/w170` prints nothing). The commits are those on HEAD between `35c5249d work: w170 ready -> claimed` and `cc96ae81 work: w170 claimed -> done`, leaving out `work run`'s own `work:` commits:

- `bcc41527` work run starts the initiative of an accepted request no initiative fulfils (supervision r103). Changes `scripts/supervise_all.py` and `tests/scenarios/supervision_intake_steps.py`.
- `55eea183` an integrate round is given the ids other initiatives' kept drafts add (supervision r102). Changes `scripts/supervise_brief.py`, adds `scripts/supervise_drafts.py`, and changes `tests/scenarios/supervision_integrate_steps.py`.
- `2e0f2555` the gate brief names its proposal's adds, changes and removes (supervision r104); module map row. Changes `CLAUDE.md`, `scripts/supervise_brief.py` and `tests/scenarios/supervision_proposal_steps.py`.

The implementer's `result.json` gives no hashes (`"see git log: r103, r102, r104 commits on work/w170"`). Its descriptions match these three commits and no others. Every file is in the work-item's fileset.

Nothing under `features/` changed in these commits. The later `7636eb12` (features: r102 scenario reformulated, old one deprecated) is the binding from the answer, not the implementer's work.

## Removed and weakened tests

None. I searched the diff `35c5249d..2e0f2555 -- tests` for:
- deleted `def` lines,
- dropped parametrize cases,
- removed or loosened `assert` lines,
- added `skip` or `xfail`,
- rewritten tests.

The only deleted lines are three `import` lines, each replaced by a wider import of the same module. Everything else is new step definitions.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree.

## Cannot verify

- The report's suite figures: 863 passed and 3 failed at the start, 145 passed and 1 skipped for `--work-item w170`, and 271 for `--whole-suite`. I did not run the suite.
- What r103 does in a real `work run`. On the real queue, `q5` is `accepted` and no `initiative.md` fulfils it (its `fulfils` lines name q1, q2, q3, q4 and q6). So the next `work run` with no initiative will start an initiative for q5 with `work start`. That is what r103 asks for, but only the fixture scenario shows it working.

## Findings

### 1. Important, answered (fix by w171): r102 reads kept drafts at `drafts/spec/capabilities/`, not `drafts/round-<m>/spec/capabilities/`
- **Where:** `scripts/supervise_drafts.py:29`.
- **What is wrong:** As in the previous review. It is confirmed now by the reformulated scenario: `pytest -k kept_drafts_add` fails the new r102 scenario, while the deprecated one still passes.
- **Answer:** The person's delegation answered this on 2026-10-25. w171 delivers the fix.
- **Triage:** Not fix now for this review, since its fix is already a work-item. The failing reformulated scenario is w171's red.

### 2. Minor, observation: `last_integrate` takes the highest integrate stage even if it has no drafts
- **Where:** `scripts/supervise_drafts.py:16-19`.
- **What is wrong:** An integrate round that was re-run and dispatched no writer hides the drafts of an earlier stage.
- **Reproduction:** `ls .shop/work/i25/runs/i25/1-integrate` holds only brief.md, result.json and session.json.
- **Fix:** Take the last integrate stage that has drafts. This can go with w171, since it touches the same function.

### 3. Minor, drop: lint the commits introduce
- `scripts/supervise_brief.py:3` I001: the import is out of order.
- `tests/scenarios/supervision_intake_steps.py:65` FURB167: `re.M`.
- `tests/scenarios/supervision_proposal_steps.py:96` RUF100: an unused `noqa`.

These were there already: `supervise_brief.py:82` ISC004, and `supervision_integrate_steps.py:107` and `:112` FURB167.

### 4. Minor, drop: the implementer's result lists no commit hashes
I matched the commits by their messages instead.

## Risks checked, no finding

- **r103: which requests are started.** `unfulfilled` reads `workqueue.requests`, which yields each `q*.md` under `.shop/work/requests/`. `fulfils` is matched on its last path segment, which covers both the short form `request/q1` and the full ids on the real queue.
- **r10: refusals before the start.** Every open `Run.check` and every `Intake.check` runs before the first `workqueue_start.start`.
- **r104: the gate brief.** The new lines are inside `if stage == "gate"`. `adds`, `changes` and `removes` are lists from `frontmatter`. Terms come through as `term/<t>`.
- **Code no line asks for.** None. Each change serves r102, r103 or r104.

## Checks
- `tools check --base 35c5249d`:
  - ruff: 6 errors, 3 of them new (finding 3).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: prints nothing.

## Commands run
- `git log --format='%H %s' -1 --grep="^work: w170 ready -> claimed$"`; `git branch --list work/w170`; `git log --oneline -15`
- `git log --stat 35c5249d..cc96ae81`; `git diff 35c5249d 2e0f2555 -- scripts CLAUDE.md features`; `git diff 35c5249d 2e0f2555 -- tests`
- `git show 7636eb12 --stat`
- `grep` in `spec/capabilities/supervision.md` (r10, r102-r104) and `scripts/workqueue.py` (`requests`)
- `grep -l "status: accepted" .shop/work/requests/*.md`; `grep -h "^fulfils" .shop/work/i*/initiative.md`; `head .shop/work/requests/q5.md`
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "kept_drafts_add or no_initiative_fulfils or only_for_the_questions"` → 3 passed, 1 failed (the reformulated r102 scenario, w171's red)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 35c5249d...`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
