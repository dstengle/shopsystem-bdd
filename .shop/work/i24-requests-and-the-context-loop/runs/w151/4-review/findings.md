# Review of w151: DONE (no Critical finding, nothing to fix now)

The commits deliver r79 and r84 as the plan's D1-D6 put them. No test is removed or weakened, nothing under `features/` changed, and every touched file is under the 300-line limit. There are two observations (hardening) and one Minor note.

## Commits reviewed

- Claim commit: `059c158 work: w151 ready -> claimed`. The branch `work/w151` is gone, so the commits are those between the claim commit and `7eb0af6 work: w151 claimed -> done` on the checked-out HEAD, less `work:` commits and w153's commit `7999ff2`:
  - `c79de72 work run starts the integrate round of a proposed initiative and marks it started` (7 files, +78/-14, all in the work-item's fileset).
- The implementer's result lists `3c2e538`, whose parent is the claim commit. `git diff 3c2e538 c79de72 -- scripts tests` shows only w153's `supervise_analysis.py` and `supervision_analysis_steps.py`, so c79de72 is 3c2e538 rebased onto w153 by the merge. Same change, different hash (Minor M1).

## Removed and weakened tests

None. What I checked:
- The only test file changed is `tests/scenarios/supervision_rounds_steps.py`.
- `rounds(repo, kind)` became `rounds(repo, kind, name="p1")`. The default keeps every existing gate, apply and formulate caller matching `# <kind> of p1`, as before.
- The diff deletes no `assert`, no parametrize case and no step, and adds no skip or xfail. The rest of the diff only adds lines: one Given and two Thens.
- No file under `features/` was touched.
- The plan's "Tests the decisions break" is "none", which matches.

## Allowances

The report's `## Tests changed under an allowance` is "none". Nothing to verify.

## Cannot verify

- The report's run results: red with 2 failed, green with 144 passed and 1 skipped, and `--whole-suite` on test_supervision and test_work_queue with 203 passed, 9 xfailed and 8 xpassed. Under my instructions I did not run the suite.
- The plan's §4 says the gate scenarios r68, r69 and r85 were not verified by the notes. Their steps are unchanged apart from `rounds`' default, and `due` offers integrate only on a `proposed` i1, while every Background writes `started`. I checked this by reading the code, not by running them.

## Findings

### O1. A missing request or an absent `fulfils:` leaves the initiative `started` with no integrate round run (Minor; observation)
- Work-item: w151. Where: `scripts/supervise_rounds.py:48-50` with `scripts/supervise_brief.py:66-70` and `scripts/workqueue_request.py:18-21`.
- What is wrong: `round` commits and pushes `proposed -> started` (`start_initiative`) before it writes the brief. The integrate brief calls `workqueue_request.accepted_lines`, and `path_of` raises `Refused("there is no request ...")` when the request file is missing, or when `fulfils:` is absent (the id is then `""`). That `Refused` is not a `Fault` or a `GitFailed`, so the round's `except` does not catch it. `work run` stops with the refusal, but the initiative is already committed as `started`. The next `work run` never offers it the integrate round again.
- Why it matters: an initiative passes to `started` without its integration. No line names this input today. The plan's §5 lists it as an open case, and no client writes a proposed initiative without a request.
- Reproduction (by reading, not by a run): `grep -n "start_initiative\|label, _ = self.run_dir" scripts/supervise_rounds.py` shows the transition on line 49, before the worktree and the worker on lines 53-58. `grep -n -A4 "^def path_of" scripts/workqueue_request.py` shows the refusal on an absent file.
- Fix: check that the request can be read, and read its accepted lines, before `start_initiative`. That needs a line first, through integrating-a-proposal: what `work run` does with a proposed initiative whose request it cannot read.

### O2. The initiative's transition is logged under the key `work-item` (Minor; observation)
- Work-item: w151. Where: `scripts/supervise_rounds.py:80`.
- What is wrong: `measure_build.work_items_of` (`scripts/measure_build.py:91-102`) turns every row with `before` and `after` into a work-item entry, so `measure initiative` will list `i1` as a work-item with one transition. Capability-proposals are already logged and measured the same way. `workqueue.agrees` and `last_logged` look up rows by a work-item's name, so an `i1` row interferes only with a work-item named `i1`.
- Why it matters: the measure record's work-item count includes the initiative. Plan §5 left this open.
- Fix: none now. Choose it when a measure line names what a work-item row is.

### M1. The result's commit hash is not the merged hash (Minor; drop)
- Work-item: w151. The result lists `3c2e538`; the merged commit is `c79de72`, the same change rebased (see "Commits reviewed"). This is how `work run` merges, not a defect of the work.

### Risks checked, no finding
- Whether the initiative is offered integrate again after the round: no. `due` reads `initiative.md`'s status, which `start_initiative` has already written as `started`.
- A faulted integrate round: `before = after = started`, so the refusal text "keeps its status started" is accurate.
- Code no line asks for: `held`, `brief` and `commit` resolve `initiative.md` for the initiative's own name. These changes serve r79 (the brief) and r84 (the commit, r7 and r46). The `Initiative:` label and `Kind: integrate` are brief mechanism. `mark(status=)` keeps `done` as its default, so `work withdraw` and `work resolve` are unchanged.
- Behaviour against Purpose: Purpose says `work run` "starts ... the `integrate` round of a `proposed` initiative", which matches. The Implementation note says the integrate round is an `initiative-round` session; `round` uses agent `initiative-round` (line 58).
- `accepted_lines` keeps a line only when its outcome is exactly `accepted`, ordered by number, and drops any line without an outcome. This matches r79's "the accepted lines".

## Checks

- `tools check --base 059c158`:
  - ruff: 1 error, `scripts/supervise_analysis.py:4:1 I001` (import order). That file is w153's change in `7999ff2`, not w151's, so it is no finding here.
  - vulture: clean.
  - import-linter: no contracts stated.
- `tools size --limit 300`: no output; no tracked file is over the limit. Touched files: supervise_rounds 92, supervise 237, supervise_brief 129, supervise_worker 242, workqueue_request 142, workqueue_done 67, supervision_rounds_steps 158.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w151 ready -> claimed$"` (and the same for `claimed -> done`), and `git log --oneline -15`
- `git log --format='%H %s' 059c158..7eb0af6`, `git show --stat c79de72`, `git show c79de72`
- `git log --format='%H %P %s' -1 3c2e538`, `git diff 3c2e538 c79de72 --stat -- scripts tests`
- `grep` of r79, r84 and integrate in `spec/capabilities/supervision.md` and `features/supervision.feature`; `sed` of the Implementation section
- `grep` of `scripts/supervise_rounds.py`, `scripts/measure_read.py`, `scripts/measure_build.py` and `scripts/workqueue.py` (`agrees`, `last_logged`, `read`), and of `path_of` in `scripts/workqueue_request.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 059c158...`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the 7 touched files
