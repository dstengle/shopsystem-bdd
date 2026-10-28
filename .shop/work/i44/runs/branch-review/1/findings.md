# Branch review of i44 (the branch reviewer has no shell tool)

**Verdict: DONE.** No finding is triaged fix now and nothing is Critical. I ran every check myself. w218 does what role-boundaries r7 asks and nothing more.

The suite has 11 failures at HEAD under plain `pytest`. All 11 are i39's parked w212 requests scenarios (StepDefinitionNotFoundError). The plugin counts them as expected failures under `--whole-suite` (supervision r43, `scripts/work_items.py:99-111`), and i39's ledger records them. None of them comes from i44.

## How this review ran

The installed plugin 0.28.1 started this review (`Scripts:`), not the branch's own code. So the brief has no `Read:`, `## Runs` or `## Commits`, and my prompt is the one from before i43, which has Bash. Under that prompt I made the runs below myself. At HEAD, `agents/bdd-branch-reviewer.md` (r7, this initiative) and review r32 say the branch reviewer runs nothing and has no shell. That takes effect only once the plugin is released with i43's `supervise_branch_runs.py`.

## Range and work-items

- **Range:** `40bc819b..d5e53571` (Base `40bc819b06ac8dd62a03580aaee217c7afa0b330`, `work: start i44, fulfilling q24`; HEAD `d5e53571013de98942df1194bb56e8a318c1562d`).
- **w218** (role-boundaries#r7), green. Its one commit is `ae666f39`, between `58d3a1db` (ready -> claimed) and `26340221` (claimed -> done). It touches `agents/bdd-branch-reviewer.md`, `tests/scripts/test_agents.py` and `README.md`, all three in its `fileset:`.
- **Commits of i44 that belong to no work-item.** All are the workflow's own commits; none is a stray change:
  - the apply round `c1446053` (`spec/capabilities/role-boundaries.md`, +r7);
  - the `work note`, `work answer` and `work add` commits;
  - the proposal's and the initiative's transitions.
- **Commits of another initiative.** i44's `initiative.md` was committed while i43 was still running on `main`. So the range also holds i43's tail, from `ffe63851` to `b871d675 work: i43 started -> done`: i43's apply and formulate rounds, w215, w216, w217, its branch reviews 1 and 2, and its measurement. Those belong to i43's work-items, and i43's branch review 2 (`fda31ecd`, range `ebbf1bea..fdf90439`) reviewed them. I did not review them again here. Their only effect on this review is the ruff errors below (Observation 1).
- **i44's own change outside `.shop/`** (`git diff --stat b871d675 HEAD -- . ':(exclude).shop'`): README.md, agents/bdd-branch-reviewer.md, spec/capabilities/role-boundaries.md and tests/scripts/test_agents.py, 7 insertions and 3 deletions.

## Suite

`Suite: 1034 passed, 11 failed at d5e53571 in 33.50 s` (1 skipped, 56 subtests passed).

- **Parallel:** yes. `pytest.ini` sets `addopts = -n auto`.
- **In-process:** no. The step definitions drive the scripts through `subprocess`, in 16 modules under `tests/scenarios/`. The suite is under 60 s, so this is no finding.
- **The 11 failures:** all are in `tests/scenarios/test_requests.py`, and all are w212's scenarios. `--work-item w212` gives the same 11 failed, plus 180 passed and 1 skipped. w212 is i39's work-item, parked awaiting-answer.
- **The run:** I ran the whole suite twice, not once. The first run's summary line was cut off in the tool's output, so I ran it once more with the output saved to a scratch file. The line above is from that second run.

## Checks

- **w218's check** (the plan's §1), `python3 -m pytest -q tests/scripts/test_agents.py`: 9 passed, 18 subtests passed. The capability has no scenarios (role-boundaries Purpose).
  - `--work-item w218` selects no r7 scenario (there is none) and ran 180 passed, 1 skipped.
  - The report's red run (`{'Bash'} is not false` before the change) follows from the parent's `tools: Read, Glob, Grep, Bash, Write`. I did not rerun it.
- **`tools check --base 40bc819b…`:**
  - **ruff:** 19 errors, none in a file i44 touched:
    - `.shop/work/i43/runs/review/2-apply/apply.py`: 5 × SIM115;
    - `tests/scenarios/supervision_branch_steps.py`: 9 × FURB167, plus PLC0206 and PIE810;
    - `tests/scenarios/test_supervision.py:14`: I001;
    - `tests/scripts/stub_claude.py:196-197`: FURB167.

    All of these are i43's, and i43's branch reviews reported them.
  - **vulture:** clean.
  - **import-linter:** "the project states no import contracts".
- **`tools size --limit 300`:** printed nothing. No tracked Python file is over 300 lines; `test_agents.py` is 91.
- **`features deprecated`:** 11 deprecated scenarios. All of them predate the branch and none is i44's. The @r117 scenario of `design-model-check.feature` has its replacement r121 green; that is i39's, already in i39's ledger.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run/real agreement:** not applicable. The plugin has no operation with both a dry-run and a real mode.

## Removed and weakened tests

None. I searched i44's diff of `tests/` for:
- removed `def test_` lines;
- removed or changed `assert` lines;
- parametrize or subTest cases;
- `skip` and `xfail`.

The only change to `tests/scripts/test_agents.py` is the docstring (r1-r6 -> r1-r7) and the new `test_r7_branch_reviewer_has_no_shell` (`:73-74`). The plan's "Tests the decisions break" lists none, which is right.

## Allowances

The report's `## Tests changed under an allowance` says "none", and the commit agrees.

## Cannot verify

Nothing. Every check above was run at d5e53571.

## Findings

1. **Minor, w218, observation.** `spec/decisions/0053-the-v3-agents.md:28` still lists `Read, Glob, Grep, Bash, Write` for `bdd-branch-reviewer`.
   - **Why it matters:** role-boundaries `rests_on` this decision, so a reader of the binding decisions sees a tool list that r7 rules out.
   - **Why it stays:** the plan's decision 2 leaves the accepted record unedited, and 0053 points to role-boundaries as the statement of the guarantees, so r7 holds.
   - **Fix:** if wanted, a superseding design-decision, or a note in 0053 that names r6 and r7.
   - **Reproduction:** `grep -n bdd-branch-reviewer spec/decisions/0053-the-v3-agents.md` gives line 28.
2. **Minor, none (README of 0.28.1, `537055a3`), drop.** `README.md:158`, in the 0.28.1 release notes, says "the branch reviewer runs the whole suite once".
   - **Why it matters:** that was true of 0.28.1 but is no longer true at HEAD (r7, review r32). It is a dated changelog entry, so it is not wrong as history.
   - **Fix:** when the next release's notes are written, they say that `work run` makes the branch review's runs and the reviewer has no shell.

No behaviour contradicts r1-r7 or role-boundaries' Purpose, and there is no code that no line asks for: w218 changes no production code, and its tool-list change is r7's own Implementation ("Tool lists … in `agents/*.md`"). The risk I checked was whether the definition and what `work run` allows differ. They agree: `scripts/supervise_worker.py:40-42` gives `branch-review` `["Read", "Glob", "Grep"]`, with no Bash.

## Shape

- **Size limit (CLAUDE.md):** met. Nothing is over 300 lines, and i44 touched no file near the limit.
- **Module map:** i44 touched no row's module. `agents/` and `tests/scripts/test_agents.py` are covered by the row "`tests/scripts/`: tests of the scripts that no scenario drives", and the test sits in the existing module.
- **Code no scenario reaches:** none added by i44; vulture is clean.

## Coupling

i44 adds no dependence on another project. The tool list is read by Claude Code's `--agent` loading (frontmatter `tools:`), the same published contract r1-r6 already rely on. Nothing new would break if that changed.

## Observations

1. The i43 ruff errors (19) are still at HEAD. Reproduction: `python3 <Scripts>/tools check --base 40bc819b…` gives "Found 19 errors", none in i44's files.
2. Plain `pytest` is red on w212's 11 parked scenarios. They are xfail only under `--whole-suite`; this is already in i39's ledger. Reproduction: `python3 -m pytest -q --work-item w212` gives "11 failed, 180 passed, 1 skipped".
3. i44's Base lies inside i43's run on the shared `main`, so `Base..HEAD` holds 70-odd i43 commits. A review started by the released `work run` gets their attribution from r156. Reproduction: `git log --oneline 40bc819b..HEAD` lists i43's commits from `ffe63851` to `b871d675`.
4. The plan's open case: `bdd-task-reviewer` and `architecture-reviewer` still hold Bash, and no line asks otherwise. Reproduction: `README.md:126,128` and `agents/*.md`.
