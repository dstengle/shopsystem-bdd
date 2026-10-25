# Review of w193: DONE

Verdict: the fix is in place. Branch review 1's fix-now finding 1 was that r114 was met only against the stand-in. To fix it, `work run`'s
apply brief and the `apply` kind of `agents/initiative-round.md` now ask the round for its change list in the result's
`changes`. That is the field `supervise_rounds.py:135` already reads through `supervise_change.entries`. The r114 Then now also
checks that the real brief asks for it. No test was removed or weakened, and nothing changed under `features/`. There are no
Critical findings and nothing to fix now. There is one Minor finding (drop).

## Commits reviewed

- The branch `work/w193` is gone. The claim was taken three times, because of merge-again: `32ce42d3`, `05777a48` and
  `8114d5f6`, each a `work: w193 ready -> claimed`. The done is `d787c410` (`work: w193 claimed -> done`).
- Between the last claim `8114d5f6` and `d787c410`, the one commit that is w193's and not a `work:` commit is:
  - `6b06211b` "work run asks the apply round for the change list it applied (r114)". It touches
    `agents/initiative-round.md` (+1), `scripts/supervise_brief.py` (+7 −3) and
    `tests/scenarios/supervision_formulate_steps.py` (+3 −1). All three are in the fileset.
- The other code commit in that window is `64c62951` (work-queue r31, r32). It belongs to w192, claimed at `620ec316`, and is not
  w193's.
- The implementer's results list `f92c4536` (3-implement) and `69bad2e0` (4- and 5-implement). Both have the same three files as
  `6b06211b`, with the same content: `git diff --stat` between the three commits on those paths is empty. See finding 1.

## Removed and weakened tests

None. I searched the diff for deleted `def test_` and step functions, dropped parametrize or Examples rows, removed or changed
`assert` lines, an added `skip` or `xfail`, and a rewritten step.

The diff's only change to a test is in `lists_written` (`supervision_formulate_steps.py:75-78`). It adds an import (`starts`) and
one assertion: every apply brief for p1 contains "result's `changes`", and there is at least one. Every earlier assertion is
still there. This strengthens the step, as the plan's Decision 2 asks. The plan lists no test under "Tests the decisions break"
("None"), which agrees.

## Allowances

All three reports give "none" under `## Tests changed under an allowance`. None is needed, because no test was weakened.

## Cannot verify

- **Whether a real `initiative-round` apply session now gives `changes`.** Only a real round can show it. The scenario checks
  that `work run` asks for the list, which is all `work run` controls. A real apply round's `result.json` would answer it,
  for example the next one under i33 or i34.
- **The reports' suite figures** (902 passed and 7 failed at the start; the failures being i33's r121, r75 and r105 plus an
  rmtree flake). Per the brief, `work run` runs the suite itself, so I did not run it whole.

## Findings

### 1. Minor, w193, drop: the commits the results list are not the commit that landed

- **Where**: `.shop/work/i31/runs/w193/3-implement/result.json`, and `5-implement/result.json`.
- **What is wrong**: the results name `f92c4536` and `69bad2e0`. The commit on the checked-out line is `6b06211b`.
- **What I verified**: all three commits change the same three files, with identical content there (`git diff --stat` on those
  paths gives nothing). The change is the same commit re-made each time the work-item was merged again.
- **Why it matters**: little. Someone tracing the work-item by hash finds unreachable or other commits.
- **Fix**: none needed.

### Open cases (not findings)

The plan's part 5 leaves these open, and the reports name them. No line asks for any of them, so they are not w193's. Each is
already an observation in branch review 1.

- A DONE apply round with no `changes` keeps its drafted lists (review 1, F1's last point).
- An apply list with no entry for `argues` empties the lists (review 1, F2).

Finding 1's fix makes F2 reachable once a real apply round names several capabilities. It needs a line before a fix.

### Risk checked

- **The risk**: the apply brief and `rewrite_lists` disagree on the id form, or on where `changes` sits.
- **What I verified**:
  - The apply brief reuses the integrate wording (`CHANGE_LIST`): ids are `<capability>#r<n>`, at the result's top-level
    `changes`.
  - `supervise_change.entries` reads `data.get("changes")`.
  - The proposals' lists hold ids in that form, for example `.shop/work/i33/supervision.md:7-8`.
  - They agree.

## Checks

- **`tools check --base 8114d5f6`**:
  - ruff: 1 error, `scripts/workqueue.py:248 I001`. It comes from w192's `64c62951`, not from w193's files.
  - vulture: clean.
  - import-linter: "the project states no import contracts".
- **`tools size --limit 300`**: printed nothing. `supervise_brief.py` has 171 lines and `supervision_formulate_steps.py` has 84.
- **The r114 scenario, run by title**: 1 passed.

## Commands run

- `git log --format='%H %s' -3 --grep="^work: w193 ready -> claimed$"`
- `git log --format='%h %an %s' 32ce42d3^..d787c410 --first-parent`
- `git show --stat 6b06211b f92c4536 69bad2e0`
- `git show 6b06211b`
- `git diff --stat 69bad2e0 6b06211b -- <the three files>`, and the same for `f92c4536 69bad2e0`: both empty
- `git diff 8114d5f6 d787c410 --stat -- scripts tests features agents spec`
- `grep` of r114 in `spec/capabilities/supervision.md`, of `entries`/`rewrite_lists` in `scripts/supervise_change.py`, and of
  the proposals' list lines
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 8114d5f6`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `python3 -m pytest -q -n 0 tests/scenarios/test_supervision.py -k "change_list or adds_changes"`: 1 passed
