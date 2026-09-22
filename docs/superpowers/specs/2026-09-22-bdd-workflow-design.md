# BDD Workflow Design

Date: 2026-09-22
Status: Draft for review

## Purpose

Replace test-driven development (TDD) in the shopsystem harness with a
behaviour-driven workflow. TDD produces well-designed code but no functional
contract. Gherkin feature files are that contract: code that passes them
conforms to a stated, readable, business-facing specification, and the
specification documents itself.

The workflow must also deliver value incrementally through the thinnest
possible vertical slices, and it must be able to change its own plan when
implementing a scenario produces feedback. The human is out of the loop
except at one gate: approval of the feature files.

## Constraints

- Gherkin scenarios are the only tests written first. There is no unit-level
  red-green cycle. Unit tests may be added afterwards at the agent's
  discretion; they are never the driver.
- The cycle is still red-green: a scenario fails before any code makes it
  pass.
- The worked example uses Python with pytest-bdd.
- The human approves feature files before any step definition or production
  code exists, and again whenever a re-plan changes what a scenario means.
- The human is not consulted at any other point. The agent stops only on a
  listed, observable stop condition.
- Feature formulation happens from the user's perspective, enforced by
  denying the formulating subagent access to the source tree.
- The skills live in this repository and are consumed by other shopsystem
  projects.

Tradeoff under watch: the feature-file gate keeps the contract correct but
may slow delivery. Checkpoint reports record every re-plan so the gate's
frequency is measurable.

## Pipeline

1. superpowers brainstorming produces and commits a spec, unchanged.
2. `formulating-features` fires on spec approval. Output: `.feature` files
   under `features/`. Ends at the human gate.
3. `slicing-into-increments` fires on feature approval. Output: a living
   plan at `docs/superpowers/plans/<date>-<topic>-slices.md`.
4. `bdd-red-green` fires when execution starts a slice, in place of
   superpowers test-driven-development. After each green slice it writes a
   checkpoint and continues. On a stop condition it hands back to
   `slicing-into-increments`.

### Chain of responsibility

The hand-off chain is strictly linear.

| Skill | Writes | May invoke |
|---|---|---|
| formulating-features | `.feature` files | nothing |
| slicing-into-increments | the slice plan | writing-plans, formulating-features |
| bdd-red-green | step definitions, production code, checkpoint entries | slicing-into-increments |

`bdd-red-green` never opens a `.feature` file for writing and never invokes
`formulating-features`. `slicing-into-increments` is the only place that
decides whether the contract has changed.

### Superseding TDD

superpowers skills that name TDD (executing-plans,
subagent-driven-development, writing-plans) continue to be used. Each new
skill states in its body that it supersedes test-driven-development when
both apply, and `bdd-red-green` uses the same triggering conditions in its
description as test-driven-development does. Whether this wins the trigger
reliably is verified by a dedicated test (see Test plan). If it does not,
the fallback is a one-line instruction in consuming projects' CLAUDE.md
stating that BDD replaces TDD.

## Skill: formulating-features

Trigger: a spec has been approved and no `.feature` files exist for it, or
`slicing-into-increments` has handed back a feature whose scenario meaning
must change.

Process:

1. The main agent dispatches a subagent with: the spec, everything under
   `docs/`, and existing files under `features/`. The subagent has no
   access to the source tree. This is enforced by the dispatch prompt
   listing exactly which paths it may read, and by the subagent type used
   having no write tools.
2. The subagent returns feature files that match the following recipe. The
   recipe is stated positively (what each file is), because the baseline
   failure for this skill is wrong-shaped output, not a skipped rule.
   - One `.feature` per user-facing capability, named after the capability,
     never after a module, screen, or table.
   - A `Feature:` line followed by a one-sentence value statement in the
     form "so that ...".
   - Scenarios in declarative Gherkin. Given describes the state of the
     world. When describes one action by one role. Then describes an
     observable outcome. Steps state intent; they never name clicks,
     fields, endpoints, tables, or functions.
   - Each scenario carries a tag naming the assumption it exists to test,
     in the form `@assumes-<short-slug>`.
   - The happy path first, then only the failure and edge scenarios the
     spec requires.
3. The main agent reviews the returned files against the spec for coverage,
   writes them under `features/`, commits, and stops for human approval.

Nothing downstream runs until the human approves.

## Skill: slicing-into-increments

Trigger: feature files have been approved, or `bdd-red-green` has handed
back with a stop condition.

Definitions:

- A slice is the smallest set of scenarios, usually one, that leaves
  something a user could observe end to end. A slice may cut through every
  layer with hard-coded or stubbed internals, provided the scenario passes
  honestly against the system's real entry point.
- Thinness tests, applied to every candidate slice: (a) could it be split
  into two slices that each still pass end to end; (b) does it contain any
  work no scenario in the slice needs. A yes to either means split or trim.

Already-green check: before the plan is finalised, run the feature suite.
Any scenario that already passes is credited to the slice whose work made
it pass (or to a "satisfied by existing behaviour" line when none did) and
is never placed in a later slice. This keeps `bdd-red-green`'s first stop
condition rare enough that a hard stop is justified when it fires.

Ordering: by the assumption tested, riskiest first, with value as the
tiebreaker. The first slice is always the thinnest walking skeleton through
the happy path of the highest-value feature.

Plan format, one markdown file:

- Per slice: number; scenarios turned green, by feature and scenario name;
  the single assumption tested and how its failure would be recognised;
  non-behavioural work the slice needs (migrations, dependencies).
  Non-behavioural work never forms its own slice; it attaches to the first
  slice that needs it.
- A log at the bottom. Each re-slice and each checkpoint appends one entry.

Re-planning, on hand-back from `bdd-red-green`:

- Re-order or split remaining slices: done alone.
- Drop a slice whose assumption is already settled: done alone.
- Change what a scenario means, add a scenario, or remove one: never done
  here. Invoke `formulating-features` for the affected feature, which
  returns the human to the loop. The test for "changes meaning" is any edit
  to a Given, When, or Then line.

Relation to writing-plans: `slicing-into-increments` invokes superpowers
writing-plans with the slice list as input and the constraint that each
task is exactly one slice. writing-plans supplies code-level detail per
task and nothing else.

## Skill: bdd-red-green

Trigger: execution begins a slice. Identical triggering conditions to
superpowers test-driven-development, which this skill supersedes.

The cycle, one scenario at a time from the slice's list:

1. Run the scenario. It must fail for the right reason: an undefined step or
   an assertion on the outcome.
2. Write the missing step definitions. Given and When steps drive the
   system's real entry point, never internal functions. Then steps assert
   only what the scenario states.
3. Write the least production code that turns the scenario green.
   Hard-coded values are acceptable within a slice.
4. Run the whole feature suite. Everything previously green stays green.
5. Refactor with the suite green. Move to the next scenario.

Never touched: feature files. The skill's checklist contains no step that
opens a `.feature` file for writing. A scenario that seems wrong is a
hand-back.

Checkpoint, after every slice goes green: append to the plan's log what a
user can now do, whether the slice's assumption held and the evidence, and
the next slice number. Continue without asking.

Stop conditions (hand back to `slicing-into-increments`), all observable:

- A scenario passed before any code was written for it.
- A scenario cannot be made to fail for the right reason (for example it
  fails during setup rather than on the outcome).
- Turning a scenario green requires work no scenario in the slice describes,
  beyond a trivial helper.
- A previously green scenario breaks and fixing it would change what a step
  means.
- The assumption the slice tests is contradicted by what was built.

Anything else, including doubt about scenario wording, goes into the
checkpoint entry and does not stop the run.

Toolchain for the worked example: pytest-bdd, because it runs under plain
pytest and reuses a Python project's existing test command, fixtures, and
CI configuration.

## Repository layout

```
.claude-plugin/plugin.json                  # manifest so other projects install this repo as a plugin
skills/
  formulating-features/SKILL.md
  slicing-into-increments/SKILL.md
  bdd-red-green/SKILL.md
  bdd-red-green/example/                    # one .feature, step definitions, production code
docs/superpowers/specs/2026-09-22-bdd-workflow-design.md
```

Discovery: Claude Code auto-discovers project skills from `.claude/skills/`,
not from a top-level `skills/`. Packaging as a plugin lets consuming
projects install it the way superpowers is installed, and lets this repo
load it locally during testing. The manifest shape is confirmed against
current documentation before it is written.

## Test plan

Each skill completes its own RED-GREEN-REFACTOR cycle (per
superpowers:writing-skills) before the next begins. The fixture project, a
minimal pytest-bdd project, lives in the session scratchpad, not the repo.
The shipped example under `bdd-red-green/example/` is extracted from it once
the skill passes.

1. **bdd-red-green** (discipline skill). Baseline: a subagent in the
   fixture receives a feature file and a slice, under time pressure and a
   "just get it passing" instruction, without the skill. Record verbatim
   whether it skips red, edits the feature file, batches scenarios, or stops
   on a non-condition. Write the skill against those rationalisations,
   re-run, refactor. Separate trigger test: with superpowers loaded and a
   feature request, the agent selects this skill rather than
   test-driven-development.
2. **formulating-features** (shape skill). Baseline: a subagent receives a
   spec for a small commerce feature and writes feature files with no
   guidance. Score for imperative steps, UI language, horizontal slicing,
   missing value statements. Write the recipe, re-run, then micro-test the
   brief wording: five reps per variant against a no-guidance control,
   every flagged match read by hand.
3. **slicing-into-increments** (pattern skill). Baseline: a subagent
   receives approved features and produces a plan. Score for slices that
   are not end to end and for non-behavioural work as its own slice. A
   re-plan scenario checks that the agent hands to formulating-features
   rather than editing a Then line.

## Out of scope

- Changing any superpowers skill.
- Unit-test guidance beyond "optional, never first".
- Non-Python examples.
- Tooling to enforce the source-tree restriction beyond a plugin agent
  definition with a tools allowlist (SKILL.md cannot restrict tools).
