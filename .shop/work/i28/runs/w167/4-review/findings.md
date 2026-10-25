# Review of w167 (supervision#r92)

**Verdict: DONE.** The change does what the plan says and serves r92 and r72. No Critical finding and nothing to fix now. There is one Minor lint finding.

## Commits reviewed

- The branch `work/w167` is gone, so I read the commits on HEAD between `23423e61 work: w167 ready -> claimed` and `5d8a406b work: w167 claimed -> done`.
- The only w167 commit in that range is `12f0b295` ("Capability-proposals from a change list carry the initiative's name in their id (supervision r92)"). The other commits in the range belong to w168 and w169.
- The implementer's result lists `5fc3ed37`. That is the same commit before the merge rebased it: it has the same message and the same four files with the same stat, and `git diff 5fc3ed37 12f0b295 -- scripts tests` is empty. They match.
- Files changed: `scripts/supervise_change.py`, `scripts/supervise_draft.py`, `tests/scenarios/supervision_integrate_steps.py` and `tests/scripts/stub_claude.py`. All four are in the work-item's fileset. Nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff of `tests/` and `features/` for removed or changed `def test`, `assert`, `parametrize`, `skip` and `xfail` lines. Every match is an added line, and they all belong to the new Thens `each_has_thing` and `different_ids`. No step or assertion was removed or loosened. The stub's `kind` regex now also captures the name, and the `round:<kind>` key keeps its meaning.

## Allowances

The report says "none", and the commits agree: no existing test changed.

## Cannot verify

- The full suite (the report gives 860 passed and 1 failed at start, then green). I did not run it because `work run` already ran it. I ran the two r92 scenarios: 2 passed.

## Risks checked

- **Duplicate drafting under the new id (r72).** `draft_proposals` matches the last segment of `part_of` (`i1-thing`) against the last segment of the proposal's id, falling back to the file stem when there is no id. `nodes()` is scoped to one initiative (`self.dir.glob("*.md")`), so the match cannot collide across initiatives. Fixture proposals such as `p1`, whose id ends in their stem, behave as before.
- **Stand-in precedence.** In `stub_claude.py:189`, `round:<kind>:<name>` is spread after `round:<kind>`, so it takes precedence as the docstring says.
- **Id form.** `capability-proposal/<context>/<initiative>-<capability>` is a valid `<name>` under decision 0027.

## Findings

1. **Minor, drop.** `tests/scenarios/supervision_integrate_steps.py:107`: new code uses `re.M`, which ruff flags as FURB167; it wants `re.MULTILINE`. This repeats a pattern already in the file (line 112, `listed`) and in `stub_claude.py:186-187`, so those flags are not new. It changes nothing a test proves, and `ruff --fix` corrects it.

The plan's open cases are not findings of this work-item, because the commits did not introduce them. They were already defects before w167, as the research notes (D1, D2) show:
- A capability named twice in one change list: the second entry silently overwrites the first.
- A capability name containing `/`: an unhandled `FileNotFoundError`, exit 0.

## Commands run

- `git log --format=%H -1 --grep="^work: w167 ready -> claimed$"`: `23423e61`. With `work/w167` the command fails because the branch is gone.
- `git log --oneline -12`, `git show --stat 12f0b295`, `git show --stat 5fc3ed37`, `git diff 5fc3ed37 12f0b295 --stat -- scripts tests` (empty).
- `git show 12f0b295`: the diff, read once.
- `git diff 23423e61 12f0b295 -- tests features | grep` for test, skip, xfail, assert and parametrize lines: only added lines.
- `git show 23423e61:<file> | grep re.M`: the uses that were there before.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 23423e61…`:
  - ruff: 4 × FURB167. One is new (line 107); line 186 of `stub_claude.py` was edited but already used `re.M`.
  - vulture: clean.
  - import-linter: no contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: nothing printed. `stub_claude.py` is at 270 lines.
- `python3 -m pytest -q -n 0 tests/scenarios/test_supervision.py -k "<the two r92 scenarios>"`: 2 passed.
