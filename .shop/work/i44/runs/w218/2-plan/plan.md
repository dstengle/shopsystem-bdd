# Plan of w218: role-boundaries#r7

## 1. What goes green

- **role-boundaries#r7**: "The plugin's agent definitions shall give the `bdd-branch-reviewer` no shell tool."
  No scenarios: the capability is checked by reading `agents/` (its Purpose; `tests/scripts/test_agents.py`), and
  no feature carries `@r7` under role-boundaries (notes §1). The check that goes green is a new unit test
  in `tests/scripts/test_agents.py`, `test_r7_branch_reviewer_has_no_shell`. It is red at first because
  `agents/bdd-branch-reviewer.md` line 4 grants Bash today (notes §1, §2).
- Retired scenarios: none (the work-item has no Retires section).

## 2. Where the change lands

- `agents/bdd-branch-reviewer.md`: take Bash out of the `tools:` line, leaving Read, Glob, Grep and Write.
  The body already says the reviewer runs nothing. Leave it as it is.
- `tests/scripts/test_agents.py`: add the r7 test, modelled on `test_r6_planner_has_no_shell`: the
  shell tools (the module's `SHELL`) and the `bdd-branch-reviewer`'s tools share nothing. Also change the
  module docstring from r1-r6 to r1-r7.
- `README.md`: drop Bash from the `bdd-branch-reviewer` row of the agents table (line 127), so the docs match
  the definition.

Removed from the researcher's set, as nothing changes in them:
- `scripts/supervise_worker.py`: the branch review's `--allowedTools` (line 42) already leaves out Bash, and its
  comment already says the review has no Bash (notes §2).
- `scripts/supervise_review.py`, `scripts/supervise_review_read.py`: they start the session and choose
  no tools (notes §2).
- `spec/decisions/0053-the-v3-agents.md`: not edited (decision 2).

## 3. Decisions

1. **Only the definition and its check change; the runtime list stays as it is.** `work run` already starts the
   branch review without Bash. r7 is a guarantee about the agent definitions (the "shall" of r7, and
   role-boundaries' Purpose: "verified by reading the definitions under `agents/`"). Rests on role-boundaries#r7.
2. **Decision record 0053 is not edited.** An accepted design-decision is a record of what was decided then, and
   0053 itself says that capability/role-boundaries states the guarantees and `test_agents.py` checks them.
   r7, the later requirement, holds where the two differ. Changing what was decided would take a superseding
   design-decision, which is not this work-item's to write. The narrator sees no difference either way: the
   tool list and the test are the same under both readings. Rests on design-decision/the-v3-agents (its
   pointer to role-boundaries as the statement of the guarantees) and role-boundaries#r7.
3. **"No shell tool" means none of the module's `SHELL` tools**, the same reading r3 and r6 already use
   (`test_r3`, `test_r6`). Rests on role-boundaries#r6 and #r7, which use the same words.

## 4. Tests the decisions break

None. I checked `tests/scripts/test_agents.py`: `test_r1` (only initiative-round has Agent/Task), `test_r2` (no Edit),
`test_r5` (model opus) and `ResultFirst` (which does not read the branch reviewer) do not depend on the
reviewer holding Bash. The notes (§3) found no test anywhere under `tests/` that asserts the reviewer has Bash.

## 5. Open cases

- The agent body's wording (line 29, "you run nothing") already fits r7. Whether it should also say outright
  that the reviewer has no shell tool is for the implementer to name, not to add unasked.
- `architecture-reviewer` and `bdd-task-reviewer` still hold Bash (0053's table). r7 does not cover them, and the
  plan leaves them alone. Note it if it seems worth a follow-up.
