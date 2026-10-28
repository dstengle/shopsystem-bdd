# Research of w218: role-boundaries r7

Search used: no `tools map`, so `tools tests-of` refused; all counts below are `by search`. Scenarios: none found by search.

## 1. Why each scenario is red today

No accepted scenarios. `features/` has no `role-boundaries` feature file, and no scenario carries `@r7` under role-boundaries (by search). The capability is verified by `tests/scripts/test_agents.py`, not by scenarios (spec/index.md:86). Nothing was run: no scenario, and I did not run the unit tests.

Read: r7 is violated today. `agents/bdd-branch-reviewer.md:4` has `tools: Read, Glob, Grep, Bash, Write`. `test_agents.py` has no r7 test (its docstring says r1-r6; `test_r2` checks only Edit for the reviewer).

## 2. Old assumptions

The old form is the reviewer holding Bash. Requirement r7 removes it.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| agents/bdd-branch-reviewer.md:4 (tools line) | grants Bash, Read, Glob, Grep, Write | remove Bash | test_agents.py test_r1-test_r5 read it through `definition()` (by search) | search `bdd-branch-reviewer`, `Bash` |
| agents/bdd-branch-reviewer.md:29 (body "runs nothing") | says no shell command, no git, no probe | already agrees with r7; no change | none | read |
| scripts/supervise_worker.py:42 TOOLS["branch-review"] | `--allowedTools` for the session: Read, Glob, Grep only | already lacks Bash; agrees with r7 | none (no test asserts the list; by search) | read, search `branch-review` |
| scripts/supervise_worker.py:40 (comment) | says the branch review "has no Bash at all" | agrees with r7 once the agent file matches | none | read |
| scripts/supervise_review.py:11, :50 | starts the `bdd-branch-reviewer` session; no tool choice | no change | scenarios in tests/scenarios/supervision_review_steps.py (fake session, by search) | search `bdd-branch-reviewer` |
| README.md:127 | table row lists `Read, Glob, Grep, Bash, Write` | stale after r7 | none | search `bdd-branch-reviewer` |
| spec/decisions/0053-the-v3-agents.md:28 | table row lists Bash for the reviewer | stale record of the decision | none | search |

Mismatch to note: the agent file grants Bash, but the runtime `--allowedTools` list (supervise_worker.py:42) does not. Fixing the agent file does not change what `work run` allows.

## 3. Tests the requirements make impossible to keep

None. No test asserts that the bdd-branch-reviewer holds Bash (by search of `tests/` for `bdd-branch-reviewer` and for the tool string). Removing Bash keeps `test_r1` through `test_r5` passing. Checked: `test_r2` (no reviewer has Edit) and `test_r5` (model opus) do not depend on Bash.

## 4. The file set

Production: agents/bdd-branch-reviewer.md: remove `Bash` from line 4. Found by read.

Test: tests/scripts/test_agents.py: add `test_r7_branch_reviewer_has_no_shell` (`set(SHELL) & set(named("bdd-branch-reviewer")["tools"])` is empty, as test_r6 does for the planner); change line 1 docstring to r1-r7. Found by read (lines 70-71 show the pattern).

Docs (not Python; read by a reader, not the suite):
- README.md:127: drop Bash from the row.
- spec/decisions/0053-the-v3-agents.md:28: either edit the row, or leave the 0053 record and note r7 supersedes it. Both readings are open; I did not choose.

Module path, edited or not (`wc -l`; room under the 300-line limit for Python in CLAUDE.md):
- agents/bdd-branch-reviewer.md: 77 lines (no limit; Markdown)
- tests/scripts/test_agents.py: 88 lines, room 212
- scripts/supervise_worker.py: 259 lines, room 41
- scripts/supervise_review.py: 99 lines, room 201
- scripts/supervise_review_read.py: 65 lines, room 235
- README.md: 383 lines (no limit; Markdown)
- spec/decisions/0053-the-v3-agents.md: 36 lines (no limit; Markdown)
