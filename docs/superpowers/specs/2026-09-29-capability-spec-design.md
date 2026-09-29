# Capability Spec Design

Date: 2026-09-29
Status: Draft for review
Builds on: `docs/stage-1-capabilities-and-features.md` (the format),
`docs/superpowers/specs/2026-09-22-bdd-workflow-design.md` (the workflow)

## Purpose

Make capability files, paired one-to-one with feature files, the spec the
plugin works from, as described in the stage-1 doc. Two deliverables:

1. The plugin's pipeline reads and maintains `spec/` instead of a
   brainstorming note.
2. A skill that migrates a repository with notes and approved features, but
   no `spec/`, onto that layout without changing any approved scenario.

## Constraints

- `spec/` is a single instance per bounded context. A brainstorming note is
  a dated proposal that is integrated into `spec/`; it never becomes a
  second spec.
- `spec/decisions.md` is a ledger: one entry per decision, with when it was
  made and the condition for reopening it. Entries are append-only; a later
  entry names what it supersedes. The format is uniform so the file can
  later be rendered from a query over decision properties.
- The human gate is on Behaviour lines, not on scenarios.
- No tooling beyond markdown and Gherkin. Pairing is a naming convention
  and a header comment.
- superpowers skills are not changed.

## Pipeline

1. `superpowers:brainstorming` produces a dated note under
   `docs/superpowers/specs/`, as today. The note proposes changes to
   `spec/`.
2. `integrating-a-proposal` merges the note into `spec/`: new capability
   files, added, changed or removed Behaviour lines, mechanism into
   Implementation, deferrals into Not yet, new ledger entries, `index.md`
   updated, open questions written down.
3. The person approves the added, changed and removed Behaviour lines and
   answers the questions. Answers become lines or ledger entries.
4. `formulating-features` formulates only the changed capabilities: a new
   line gets a scenario, a changed line rewrites its scenario, a removed
   line removes it.
5. `slicing-into-increments` places what changed, as it places any scenario
   added after a plan was cut.
6. `bdd-red-green` implements, unchanged.

Migration is the first integration: `spec/` starts empty, every existing
note is a proposal, and the approved features are evidence. The only work
unique to migration is re-pairing existing features, tests and plans.

### Chain of responsibility

| Skill | Writes | May invoke |
|---|---|---|
| integrating-a-proposal | `spec/` | formulating-features |
| formulating-features | `.feature` files | integrating-a-proposal (a question only) |
| slicing-into-increments | the slice plan, `@slice-<n>` tags | writing-plans, formulating-features |
| bdd-red-green | step definitions, production code, checkpoints | slicing-into-increments |
| migrating-to-capabilities | `spec/`, feature files, test bindings, the slice plan | formulating-features |

## File conventions

Layout and capability file shape are as in the stage-1 doc, with one fix:
names are hyphenated on both sides, `spec/capabilities/write-path.md` ↔
`features/write-path.feature`.

Ledger entry:

```markdown
## decision/<slug>
<one line: the decision, with its reasoning when there is no revisit signal>
date: <YYYY-MM-DD>
revisit_when: <a signal someone will actually see>     (optional)
supersedes: decision/<slug>                            (optional)
source: <path to the note or ADR it came from>         (optional)
```

Feature file header:

```gherkin
# formulated from spec/capabilities/<name>.md
Feature: <capability title>
  Narrator: <narrator>
```

## Agent: capability-writer

- Tools: Read, Glob, Grep. Model: opus.
- May read the note(s) it is given, `spec/`, `features/` and `docs/`. No
  source, tests, configuration or build files, for the same reason the
  formulator cannot: the spec is written from the narrator's side.
- Its definition carries the stage-1 format rules: the four kinds of
  sentence and their sections; cut what fits none; EARS patterns with
  preconditions first and at most one trigger; no "shall"; the response is
  observable by the narrator or the sentence is Implementation; tables stay
  tables; the ledger entry shape.
- Writes nothing. Returns:
  1. every changed or new file under `spec/` as a fenced block;
  2. a change list, one row per Behaviour line: `added | changed | removed`,
     the capability, the line, and the note sentence it comes from (quoted);
  3. new ledger entries;
  4. questions: conditions the note never states, one line each, with no
     line written for them;
  5. cut sentences: note sentences that fit no section.
- In migration mode it additionally returns the mapping table (see
  Migration).

The stage-1 doc moves into the plugin as the reference the agent
definition is written from (`docs/capability-format.md`), and is not read
at run time.

## Skill: integrating-a-proposal

Trigger: a brainstorming note has been approved; or `formulating-features`
returns a line that admits two readings; or slicing logs a
`QUESTION FOR THE SPEC:`.

Process:

1. Dispatch `capability-writer` with the note path (or the question and the
   capability it concerns).
2. Check the change list both ways: every behavioural sentence of the note
   is a line, a question, or a cut sentence; every added or changed line
   cites its note sentence. Missing rows go back to the agent.
3. Write the files. Append ledger entries; never edit an existing one.
   Commit `spec/` alone.
4. Gate: show the person the added, changed and removed lines and the
   questions. Wait for an explicit yes. Removed lines are shown because
   they delete contract. Answers are integrated by another dispatch and
   shown again.
5. Invoke `formulating-features` with the changed capabilities and the
   change list.

## Changes: formulating-features and feature-formulator

- Input: the changed capability paths and the change list, not a spec path.
- The formulator may read `spec/` and `features/`. The note under `docs/`
  is no longer an input. It formulates from Behaviour only; Purpose and
  Not yet are context; Implementation is never formulated.
- File name and header as in File conventions. The `So that …` line is
  dropped; Purpose carries the value.
- One scenario per EARS line, titled by restating the line's condition. A
  Scenario Outline where a line has a Where with several configurations, or
  several cases; a table of commands gives one scenario per row.
- The one-line description under each scenario title stays.
- EARS to Gherkin mapping as in the stage-1 doc.
- A changed line rewrites its scenario; a removed line removes it.
- Coverage check is mechanical: lines and scenarios are 1:1, both ways.
- The settled/deciding sort and the scenario-level approval (0.6.0) are
  removed: a scenario formulated from an approved line is approved by
  construction. A line the formulator cannot turn into one scenario
  because it admits two readings comes back as a question with both
  readings, no scenario is written, and the skill invokes
  `integrating-a-proposal`.
- Hand-back brief: if the capability's line decides the scenario, rewrite
  it citing the line, and slicing resumes. Otherwise return the question,
  which goes to `integrating-a-proposal`.
- Description: triggers on capability files having changed, no longer on
  a spec being approved.

## Changes: slicing-into-increments

- Stack slices are cut from the constraints in `spec/index.md` that state
  a bound.
- `index.md`'s order of building is a dependency constraint; risk orders
  the rest as today.
- `QUESTION FOR THE SPEC:` lines are logged as today and then sent to
  `integrating-a-proposal`, so the answer lands in a capability or the
  ledger.
- A scenario removed by a changed spec is logged; its step definitions and
  code are left for the architecture review to flag.
- The third row of the re-plan table still invokes `formulating-features`,
  which may escalate to integration.

## Changes: agents

- `bdd-branch-reviewer`: "the spec is a vision document" is replaced.
  Behaviour lines are the contract. Where they are silent, a reasonable
  person's expectation still makes a finding, and the finding is also
  raised as a question for the spec.
- `architecture-reviewer`: reads the ledger and the Implementation
  sections. Code that differs from an Implementation section is a note to
  update that section, not a defect. A ledger entry whose `revisit_when`
  has fired is reported.
- `bdd-implementer`, `bdd-task-reviewer`, `bdd-red-green`: "the spec"
  becomes "the capability's Behaviour" where it refers to the contract.

## Skill: migrating-to-capabilities

Trigger: the repository has `features/` and one or more notes under
`docs/superpowers/specs/` but no `spec/`; or the person asks for a
migration.

Preconditions, each a stop if unmet: the working tree is clean; no slice
in the living slice plan is `in progress`. Then record the baseline: the
suite summary line, the set of passing scenarios as `feature / scenario`,
and the collected count for each `@slice-<n>` tag.

1. **Write the spec.** Dispatch `capability-writer` in migration mode with
   every note (oldest first; later notes supersede earlier ones), `adrs/`
   if present, and every feature file as evidence. It returns `spec/` and
   a mapping table:
   - Every existing scenario maps to exactly one line. A line written from
     an approved scenario is approved already.
   - Where several scenarios verify one rule (a happy path and a boundary),
     the rule is split into one line per scenario. Scenarios are never
     merged.
   - A note line with no scenario behind it is unbacked: new contract.
   - A conflict between a note and a scenario, a scenario covering two
     lines, or a scenario name used in two source files is a question.
     Scenario text is never changed to resolve one.
   - Ledger: one entry per ADR with `source:` pointing at it; the notes'
     decisions dated by their note. `index.md` from the notes' purpose,
     constraints, order of building and testing. Not yet from the notes'
     deferrals.
2. **Gate.** As step 4 of `integrating-a-proposal`, showing only unbacked
   lines and questions. Commit `spec/`.
3. **Re-pair.** The main agent, which may touch tests:
   - Build each capability's feature file from its mapped scenarios in
     line order with the new header. Titles, descriptions, steps, tables
     and tags, `@slice-<n>` included, move verbatim.
   - Where source files had different Backgrounds, inline each scenario's
     Background as its first Given steps.
   - Invariant: each scenario's effective step sequence (Background then
     its own steps) is identical before and after.
   - Rebind test modules to the new file names. Step definitions visible
     only in a module that no longer binds their scenarios move to
     `conftest.py` or to the binding module, unedited.
   - Rewrite the feature part of `Scenarios:` lines in the living
     `*-slices.md` and log the migration there. Batch implementation plans
     are history and are not touched.
   - Delete the old feature files.
4. **Verify.** The suite summary line, the passing-scenario set and every
   slice-tag count equal the baseline. Any difference stops the migration
   and is reported; nothing is changed to make the numbers match. Features,
   tests and the slice plan are committed together.
5. **Hand off.** Each note gets a one-line header: `Proposal, integrated
   into spec/ on <date>.` Approved unbacked lines go to
   `formulating-features`, then slicing.

## Documentation and release

- README: the pipeline above; the two new skills and the new agent; a
  suggested `CLAUDE.md` line for consuming repositories: "Brainstorming
  reads `spec/` first; its note proposes changes to `spec/`, which
  integrating-a-proposal merges."
- The 2026-09-22 design doc gains a pointer to this one where its pipeline
  and formulating sections are superseded.
- Version 0.8.0.

## Test plan

Per superpowers:writing-skills: a headless baseline before each edit, the
same prompt after, both plugins by `--plugin-dir`, Opus, fixtures in the
scratchpad, results logged under `docs/superpowers/testing/`.

1. **capability-writer / integrating-a-proposal.** Baseline: the promo note
   and the stage-1 doc as prose, no agent. Score: "shall"; Behaviour
   responses the narrator cannot observe; rationale kept; unstated
   conditions not raised as questions; decisions missing from the ledger.
   Green: the same with the agent. Second fixture: a second note into an
   existing `spec/`. Score: no second spec; change list complete; earlier
   ledger entries untouched; removed lines shown at the gate.
2. **formulating-features.** Fixture: approved capabilities with a tempting
   Implementation sentence and a line with two readings. Score: 1:1; new
   header; nothing from Implementation; the two-reading line returned as a
   question with no scenario.
3. **slicing-into-increments.** Fixture: a hand-back no line decides.
   Score: routed to formulating, then integration; no line edited by
   slicing; stack slices from `index.md`.
4. **migrating-to-capabilities.** The cart fixture with two features that
   merge into one capability and differing Backgrounds, then a scratchpad
   copy of `shopsystem-kb` at HEAD (never the real checkout). Score: suite
   line, passing set and tag counts identical; no effective step sequence
   changed (checked by a throwaway script in the harness); lines split, not
   scenarios merged; collisions and conflicts raised as questions.
5. **Trigger.** With superpowers loaded and a note just approved,
   `integrating-a-proposal` fires rather than `formulating-features` or
   `writing-plans`.

Build order: the agent and integrating-a-proposal; formulating-features;
slicing and agent wording; migrating-to-capabilities; docs and version.

## Out of scope

- Relationships between contexts, `@uses` tags, requests, capability
  groups, beliefs (stage-1's "Not in stage 1").
- Rendering the ledger or cross-capability tables by tool.
- Rewriting historical batch implementation plans.
- Changing any superpowers skill.
