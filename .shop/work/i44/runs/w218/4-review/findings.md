# Review of w218 (role-boundaries#r7)

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. The commit does what r7 asks and nothing more: Bash is gone from `agents/bdd-branch-reviewer.md`, the README row matches, and a test checks it.

## Commits reviewed

- `ae666f3937aecf64c1e1038ab4fc34e971202247` "role-boundaries r7: bdd-branch-reviewer has no shell tool". This is the brief's `Commits:`. It is the only commit after `58d3a1db work: w218 ready -> claimed`, and the one the implementer's `result.json` lists. The `work/w218` branch is gone; the brief gives the commits, so I didn't need it.
  - `agents/bdd-branch-reviewer.md:4`: `tools: Read, Glob, Grep, Bash, Write` became `tools: Read, Glob, Grep, Write`.
  - `README.md:127`: the agents-table row has Bash removed.
  - `tests/scripts/test_agents.py:1`: the docstring now says r1-r7; `:73-74` adds `test_r7_branch_reviewer_has_no_shell`.

Suite, from the brief's suite record: 1034 passed, 0 failed at ae666f39. The 11 expected failures are w212's parked requests scenarios, which this commit doesn't touch.

## Removed and weakened tests

None. I read the whole diff of `tests/scripts/test_agents.py`: one test function added, the docstring changed, no assert removed or loosened, no parametrize or subTest case dropped, no skip or xfail added. The commit changes no other test file and nothing under `features/`. The plan lists none under "Tests the decisions break", and none were needed.

## Allowances

The report's `## Tests changed under an allowance` says "none". The commit agrees: the only test change is a new test.

## Cannot verify

- The report's red run (`AssertionError: {'Bash'} is not false` before the change). I don't have the pre-change tree in a runnable form here. It follows from reading the definition at the parent commit (`Bash` in the tools), so it is plausible.

## Findings

1. **Minor — observation (outside w218's commits; the work-item named no commit for it).** `README.md:158` still says "the branch reviewer runs the whole suite once". That contradicts the reviewer's definition ("runs nothing", `agents/bdd-branch-reviewer.md:29`), and r7 now rules it out. The sentence comes from commit `537055a3` (0.28.1 README section), not from w218. Reproduction: `grep -n -i "branch review" README.md` gives line 158. Fix: change it to say that `work run` runs the whole suite once before the branch review and gives the reviewer the result.
2. **Minor — observation (outside the commits, as the plan's open case says).** `spec/decisions/0053-the-v3-agents.md:28` still lists Bash for `bdd-branch-reviewer`. The plan's decision 2 leaves the accepted record as it is, and 0053 itself defers to role-boundaries for the guarantees. A superseding design-decision could bring the table in line later. No change needed here.

Nothing else: no behaviour against r1-r7 or the Purpose, and no code that no line asks for (the commit has no production code; the definition change is r7's own Implementation, "tool lists in `agents/*.md`"). The runtime `--allowedTools` for the branch review (`scripts/supervise_worker.py:42`, per the notes) already leaves out Bash, so the definition and what `work run` allows now agree.

## Checks

- `tools check --base 40bc819b…`:
  - **ruff:** 19 errors, none in a file w218 touched (`grep -c test_agents` gives 0). They are in `tests/scenarios/supervision_branch_steps.py`, `test_supervision.py` and `tests/scripts/stub_claude.py`, from i43's commits.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `tools size --limit 300`: printed nothing; no tracked Python file is over the limit. `test_agents.py` is 91 lines.

## Commands run

- `cat` of the brief, the work-item, the capability, the notes, the plan, the report and `result.json`
- `git show --stat ae666f39`, `git show ae666f39`
- `git log --format='%h %s' 40bc819b..ae666f39`
- `git diff --stat 40bc819b ae666f39 -- features/ tests/` (the features and test changes in that range are i43's, before w218's claim)
- `cat tests/scripts/test_agents.py`, `head spec/decisions/0053-the-v3-agents.md`
- `grep -n -i -E "bash|shell|git |python3|run " agents/bdd-branch-reviewer.md`
- `grep -n -i "branch review" README.md`, `sed -n 152,160p README.md`, `git log -S… -- README.md`
- `wc -l tests/scripts/test_agents.py`: 91
- `python3 -m pytest -q tests/scripts/test_agents.py`: 9 passed, 18 subtests passed
- `python3 <Scripts>/tools check --base 40bc819b…`, `python3 <Scripts>/tools size --limit 300`
