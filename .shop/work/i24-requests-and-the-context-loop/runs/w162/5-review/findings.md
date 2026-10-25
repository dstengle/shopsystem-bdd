# Review of w162: DONE

Verdict: no Critical finding, none to fix now. The commit does what the @r79 scenario e3fbf0b asks, and only that. Two observations follow.

## Commits reviewed

The branch `work/w162` is gone, so the commits are those on HEAD between `01ba96d work: w162 ready -> claimed` and `4ff04ce work: w162 claimed -> done`, leaving out `work run`'s own `work:` commits:

- `3a307c0 supervise: a proposed initiative whose fulfils names a request the queue does not hold is given no integrate round (r79)`: `scripts/supervise_rounds.py` +6/-1, `tests/scenarios/supervision_rounds_steps.py` +6.

The implementer's result lists `c47a088` with the same subject. The hash differs because `work run` rebased the branch onto the initiative branch, which holds e3fbf0b. Subject and files match the report's "Files changed". No difference that matters.

`e3fbf0b` (the feature scenario) comes before the claim and was made by the formulation the coordinator ruled. It is not the implementer's. The implementer's commit touches nothing under `features/`.

## Removed and weakened tests

None. I searched the diff `01ba96d..4ff04ce` under `tests/` for removed lines (`-` lines), `def test`, `parametrize`, `assert`, `skip` and `xfail`. The only change under `tests/` is one new Given step, `proposed_fulfilling_missing`. No line was removed or changed.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commits agree: no existing test changed.

## Cannot verify

- The report's red run, made with the scenario copied in uncommitted: 1 failed, with i1 `started` and "there is no request q9" on stderr. The commits cannot show it. What I can see: the code before the commit moved the initiative in `round()` before reading the request, which agrees with the research probe P-a.
- The report's suite record ("848 passed at 4cbd265"). I did not run the suite.

## Findings

### O1. A request that is held but not UTF-8 is skipped in silence, as if missing. Minor, observation.
- Where: `scripts/supervise_rounds.py:34-38`.
- What is wrong: the new `except Refused: pass` catches every `Refused` that `accepted_lines` raises. That includes `workqueue.read`'s "… is not UTF-8 text" (`scripts/workqueue.py:50-55`), not only `path_of`'s "there is no request". Such a request is held, but the initiative gets no integrate round, stays `proposed`, and the person is told nothing.
- Why it matters: no client writes a request that is not UTF-8 today, so this is hardening.
- Reproduction: by reading only, with no probe run. `accepted_lines` → `workqueue.read` → `Refused`, which `due()` swallows.
- Fix: catch only the missing request, for example by checking `path_of`'s condition first and letting other refusals propagate. Or have the scenario's line say which refusals mean "no round".

### O2. A `fulfils` naming a missing request is never reported to the person. Minor, observation.
- Where: `scripts/supervise_rounds.py:34-38`.
- What is wrong: the plan's Decision 1 (refuse under r10, saying why) was dropped. The implementer's reason holds: the scenario's "the second `work run` was not refused" step (`supervision_rounds_steps.py:144-147`) asserts exit 0 and no `work:` on stderr. The code now matches the scenario. The cost is that a mistyped `fulfils` leaves the initiative `proposed` with no word, until model's `w_stale_intake` warns after 90 days.
- Why it matters: the behaviour is what the scenario pins, so this is not a defect of these commits. The report lists it as an open question.
- Fix: if the person wants a word, write a line through integrating-a-proposal, for example a warning on stderr that does not start with `work:`.

### Carried from the plan (not in these commits)
The plan's Open cases are still open and unchanged, and the report names them:
- D2: a held request with no accepted line still gets an integrate round with no lines.
- D3: a DONE integrate round leaves its stage directory uncommitted.

## Risks checked
- Do `due()` and the brief take the same request id? Yes. Both use `str(fulfils).rsplit("/", 1)[-1]` (`supervise_brief.py:68`), so a full-id `fulfils` (P-d) still finds its request.
- Does the check run before anything moves? Yes. `due()` runs before `round()`, so `start_initiative` and the round branch are never reached on a missing request.
- Behaviour no line asks for: none. A missing request now gives no round and nothing moves, which is what the r79 scenario pins.

## Commands run
- `git log --format='%H %s' -1 --grep="^work: w162 ready -> claimed$"` → 01ba96d. The same for `claimed -> done` → 4ff04ce.
- `git log --oneline -15`, `git show 3a307c0`, `git show e3fbf0b`, `git diff 01ba96d 4ff04ce --stat`
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k fulfils` → 3 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 01ba96d`:
  - ruff: All checks passed
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → printed nothing. `supervise_rounds.py` is 102 lines, `supervision_rounds_steps.py` is 242.
- `git status --short` → clean.
