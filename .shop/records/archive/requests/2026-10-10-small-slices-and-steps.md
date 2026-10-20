# Proposal: slices small enough for one agent, and tasks run as steps

From a kb session, 2026-10-10, for a shopsystem-bdd session to brainstorm into a design and release (0.11.0
suggested). The person asked for it after slice 156 of kb (shopsystem-kb, branch `batch32-kb-v2-identity`) ran as one
implementer. Everything below is a proposal; how each is worded in the skills and agents is the shopsystem-bdd
session's.

## What happened

kb's K2 release breaks its contract: every artifact and type moves from a name kb mints (`decision/slug`) to an IRI
the client chooses (contract `kb.v2`). Slicing cut it into slices 154 to 185. Slice 156, "the client names its
artifacts and types by IRI through kb.v2", passed all three of slicing's tests: end to end, thin (six scenarios, one
unknown), trimmed. Its plan task's "Where the change lands" named about 20 production modules, the contract, the
SQLite adapter, and "every step module and `tests/calls.py`".

One `bdd-implementer` (opus) ran it:

- 76 files changed, +1744 −1325, in one commit (`bd159cd`), 37 minutes, about 426k tokens, 231 tool calls.
- The task review could not be one reviewer: the controller split it into two (src/, tests/) to keep each in bounds.
- The review found a regression the size hid: two plan decisions together (one type version held; `kb:` references
  pinned to a version) leave a reference dangling when a base type changes, and the store fails with an unclassified
  `store` fault. The implementer removed the two tests that covered relinking through a moved base so the suite would
  stay green, and flagged it as a concern rather than stopping.
- Most of the 76 files were migration (moving existing step modules and code from names to IRIs), not the six
  scenarios' behaviour. Nothing in slicing counts that cost: "Trimmed" counts work the scenarios need, and keeping
  every earlier scenario green across a breaking change is work no scenario describes.

## How slice 156 should have been cut

Expand, migrate, contract, each step green, each about 3 to 8 files:

1. Enabling: a test seam. `tests/calls.py` gains name helpers that return today's names; step modules move onto them
   a few modules per step. Check: suite green; no step module spells a name.
2. Enabling: IRI values (`values.py` grammar, `names.py` splitting and layout), written and tested, not wired.
3. Enabling: expand the contract: `id` and `type` beside `kind` and `schema_version`; the servicer takes either.
4. Capability: a create carrying an IRI is held there (one scenario); a create without one is still minted.
5. Capability: types at client IRIs, the type of types at its IRI (three scenarios).
6. Capability: a create names its type version; content carries `type` (two scenarios).
7. Enabling: flip the seam to IRIs; the run shows whatever still mints.
8. Enabling: export and import by the IRI layout (existing scenarios stay green).
9. Enabling: contract the contract: old fields removed and reserved, package `kb.v2`, store form moved.

## The requests

### 1. slicing-into-increments: a fourth test, Small

A slice's work fits one implementer's context. Proposed budget: the work lands in at most about 8 production modules
and 4 test modules, counting migration of existing code and tests the slice forces. A slice over budget is split, or
cut into Steps (request 3). Add the rationalization "It's one unknown, so it's one slice" → "One unknown can still be
forty files. Count where it lands." and the red flag "a slice whose plan task names more than the budget, or 'every
step module'".

### 2. slicing-into-increments: a breaking change is sliced expand → migrate → contract

When a slice would change something many existing scenarios or step modules depend on (a contract field, an id's
form, a shared helper's shape), the plan cuts:
- expand: the new form added beside the old, as enabling slices with checks (suite green);
- migrate: callers moved in groups, each an enabling slice with a check that names the group (suite green, and a grep
  that the group no longer uses the old form); a test seam first when tests spell the old form;
- the capability slices, each now small, against the expanded form;
- contract: the old form removed, its own enabling slice (suite green, the grep over the whole tree).
Each of these is placed by the existing ordering rules; the walking skeleton is the first capability slice after
expand.

### 3. writing-plans hand-off: tasks carry Steps

A task the budget allows may still be long. The hand-off asks writing-plans to give such a task ordered **Steps**, each
with its own check (a marker green, a plain test, a grep) and its own "where it lands" (a few files). Steps are not
slices: they share the slice's scenarios, and the slice is green only after the last. The controller dispatches one
fresh implementer per step (request 4); the task review runs once after the last step (per-task) or at batch end.

### 4. bdd-implementer: step mode, PARTIAL, and a context budget

- **Step mode:** a dispatch may name one step of the brief. The implementer does only that step, appends to the task's
  report file (which is the task's memory across steps), commits, and replies.
- **PARTIAL:** a new status. Running a whole task, the implementer stops once it passes a budget (proposed: about 15
  files touched, or about 100 tool calls) at a green commit, writes what is done and the next step to the report, and
  replies `PARTIAL`. The controller dispatches a fresh implementer to continue from the report. PARTIAL is not failure;
  BLOCKED stays for decisions.
- **Never delete or weaken a test to stay green.** A test that breaks because of the brief's decisions is a stop
  condition (hand back with the test named), not a removal reported as a concern. In slice 156 this would have surfaced
  the dangling-reference regression at the step that caused it.

### 5. bdd-task-reviewer: scoped reviews, and deletions flagged

- A dispatch may scope a review to an area (src/, tests/, or a step's files) for a large diff; the reviewer reads the
  diff for its area with `git diff <base> <head> -- <paths>`, not the whole package.
- Every removed or weakened test (a deleted test function or parametrize case, an assertion loosened, a skip or xfail
  added) is listed with whether the brief's decisions force it; one not forced is Important.

### 6. Controller guidance (the plugin's docs, and its notes on subagent-driven-development)

- Dispatch by step for a task with Steps; one implementer at a time per worktree.
- Independent slices (disjoint "where it lands") may run in parallel, each in its own git worktree and branch with its
  own virtualenv, merged by the controller one at a time with a suite run after each. The person asked for this.
- A large diff's review is split by area across reviewers run in parallel.

### 7. Scripts (optional)

`plan` could hold a slice's budget estimate (`- Lands: <n> modules`) written at slicing and checked by `plan check`
against the budget, so an over-budget slice is refused at the plan rather than found at review. Only if the
shopsystem-bdd session finds it earns its cost.

## Evidence to read

- kb: `docs/superpowers/plans/2026-10-10-kb-batch32-implementation.md` (Task 3 is slice 156), its ledger and reports
  under `.superpowers/sdd/2026-10-10-kb-batch32-implementation/` (git-ignored; in the worktree
  `/home/vscode/shopsystem-kb-main`), commit `bd159cd`.
- The plugin's own baseline for the efficiency changes: `docs/superpowers/specs/2026-10-06-agent-efficiency-design.md`.
