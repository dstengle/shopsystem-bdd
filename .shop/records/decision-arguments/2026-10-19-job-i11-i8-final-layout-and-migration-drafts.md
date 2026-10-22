---
id: decision-argument/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-job-i11-i8-final-layout-and-migration-drafts
kind: decision-argument
about: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/final-layout, design-decision/missingmass.io/shopsystem/shopsystem-bdd/light-decisions, design-decision/missingmass.io/shopsystem/shopsystem-bdd/references-are-ids, design-decision/missingmass.io/shopsystem/shopsystem-bdd/plugin-scenarios-run-as-pytest-bdd, design-decision/missingmass.io/shopsystem/shopsystem-bdd/migration-in-one-pass, design-decision/missingmass.io/shopsystem/shopsystem-bdd/living-plan-to-work-items]
date: 2026-10-19
---

# i11 final layout and i8 model in consumers: drafts and the drafter's notes

The drafts of initiatives i11 (this repository on the final layout and conventions: `spec/decisions/`, `.shop/`, ids for references, rule labels, "deprecated", pytest-bdd) and i8 (migrating a consuming repository to design model v3 with `scripts/migrate`), written on 2026-10-19 by one drafting agent under the common brief (initiative-archive/2026-10-19-job-migration-release-common-brief). Its NOTES.md covers both: open questions with a recommendation each, where i10's and i8's drafts must agree, what in the repository contradicted the directions, risks, and what `model check` reported over the drafts. They were integrated, unapproved, in commit b0231c6 (measurement/2026-10-19-job-migration-release-integration-report) and later reshaped, so none is identical to a committed file: these are superseded drafts. Decisions 0045-0050 drafted here were accepted at the 0.21.0 release gate. Copied out of a job workspace on 2026-10-22; each file's text as it was: NOTES, then i11 (initiative, spec index, proposals, capability files, decisions, work-items), then i8 likewise.

Archived from git-ignored scratch; each file's text as it was.

## `.shop/scratch/from-job/design-drafts/i11-i8/NOTES.md`

~~~~~~
# NOTES: i11 and i8 drafts

Drafts: `i11/` (initiative, 6 capability-proposals, 6 proposed capability files, `spec-index.md`, decisions
0045-0048, 15 work-items) and `i8/` (initiative, 2 capability-proposals, 2 proposed capability files, one of
them new, decisions 0049-0050, 7 work-items). 0051 and 0052 are unused.

## Open questions, each with a recommendation

1. **Where "carry" goes in a Not: list.** The person asked for carry in the Not: lists, but no term means
   "carry": its senses were has, keep and do. v_t1 only reads Not: lists, and its row names a term.
   *Recommended:* add carry, carries, carried, carrying to **requirement**'s Not: list, since most uses were
   "a requirement carries an id". All four forms are needed because the matcher allows a plural "s" only.
   The cost is that a v_t1 row for "carry" names term/requirement, which reads oddly. *Alternative:* a
   context-wide avoided-words bullet in the glossary. That changes the format (design-model-check r48 and
   r49, capability-format) and I did not draft it.
2. **Literal words and v_t1.** As written, a line that names the old tag (`@holding` in design-model-check
   r62, migration-tools r2 and r27, spec-migration r18) is reported by v_t1 once **deprecated scenario**
   avoids "holding", because the matcher treats `@` as a word boundary. *Recommended:* design-model-check r51
   (changed): code spans, double-quoted strings and `@` tags are not mentions. Without this, model check
   cannot pass on this repository's own spec.
3. **The index's name.** *Recommended:* `spec/decisions/index.md`. It sits with the files it indexes and its
   links are bare file names. design-model.md section 8 says `spec/decisions.md`, so it gets a dated note
   (work-item/final-layout-read). The model text is otherwise left alone, being shopsystem-knowledge's
   (observation/2026-10-16-model-owned-by-knowledge).
4. **batch-measurement must "stay as it is" (i12), but two of its lines and four of its steps use words the
   new glossary avoids.** *Recommended:* the two-word proposal final-layout-batch-measurement (r10 carry,
   r16 held), plus the steps reworded at formulation. Titles do not change, so `test_measure.py`'s docstring
   binding and `scripts/measure` are untouched. The alternative is v_t1 rows until i12, so `model check`
   would not exit 0 at release.
5. **test_measure.py's binding.** *Recommended:* it keeps the docstring binding, and `tests/scripts/binding.py`
   is kept for it alone, until i12 rewrites batch-measurement. Converting 38 scenarios that i12 rewrites
   anyway is investment in the old system. The other three script capabilities move to pytest-bdd now.
6. **Decision `source` as ids only.** *Recommended:* yes, with a new free-text field `by` for the person, a
   date, a delegation, a release or commit, or another repository's decision. This repository's 36 decisions
   are rewritten mechanically (work-item/deprecated-and-sources), and the archive and test-log records get
   ids so that sources can cite them. Kinds: design notes and ADRs are decision-argument; plans, requests
   and reports are initiative-archive; test logs are measurement. `model` resolves a decision's sources but
   writes no `source` fact, because grammar.md's v9e allows `source` only on an initiative.
7. **Light form for existing decisions.** *Recommended:* not applied retroactively. Their Context,
   Alternatives and Consequences are record. Only new decisions are light, and model check requires only a
   `## Decision` section (r63).
8. **Old layout in model check.** "No fallback" is kept: nothing old is read. But r61 and r62 report
   `spec/decisions.md`, a top-level `decisions/`, `work/` or `records/`, and `@holding` as file problems that
   name `scripts/migrate`. Without them, an unmigrated repository would pass with half its files unread.
   *Recommended:* keep both. They are refusals, not readings.
9. **Living plan to work-items (decision 0050).** Open slices become work-items under one capability-change
   initiative `migrated-plan`, through formulated capability-proposals with no `adds`. Backlog entries and
   open log entries become observations. On kb that is about 200 observations (160 backlog entries and 43
   QUESTION, REQUEST or RE-FORMULATE entries), and each draws a w_uncited_obs warning.
   *Recommended:* accept this, with the gate offering "keep all". The alternative is to make only the
   backlog into observations and leave the log in the archived plan.
10. **The transient directory.** *Recommended:* `.shop/scratch/` (git-ignored) replaces `.superpowers/` for
    drafts, scout notes, probe files and the coverage map. i10 should use it for the delivery side (scout,
    review findings).
11. **Ordering work-items.** The common brief says work-items `depends_on` others. In grammar.md,
    `depends_on` on a work-item names a capability (`wi_depends`), and model check reports a work-item there
    as unresolved. *Recommended:* `blocked_by` between work-items, as drafted. The person or coordinator
    may want the brief corrected.
12. **`## Constraints carried` in spec/index.md.** I renamed it to `## Constraints` in `spec-index.md` as
    part of the plain-word pass. design-model.md names the section "constraints carried". The heading is not
    a line, so this is optional. *Recommended:* rename it here, and have capability-format teach
    "Constraints".

## Where i10's and i8's drafts must agree with these

- **The glossary merge order.** As soon as **deprecated scenario** is in `spec/index.md`, any Behaviour line
  saying held, holding or superseded fails v_t1. Today that includes review r10 and r11, red-green r2, and
  spec-migration r11 and r13 (and red-green r11 says "carries"). *Recommended:* i10's proposals for review,
  red-green and code-research use "deprecated" and plain words. The glossary change (in
  final-layout-feature-file-tools) merges in the same spec commit as model-in-consumers-spec-migration and
  after i10's proposals, or all together.
- **feature-file-tools.** i10 retires the slice lines (r8-r11, r30-r34, r43-r50; r47 and the
  `slice_expectations.py` text name `docs/superpowers/plans/`). My proposal changes r8 and r10 for plain
  words only; drop those two if i10 retires them. r21 and r40 no longer mention slice tags.
- **design-model-check.** i10 retires r22 and r42 (`#behaviour/r<n>`, decision 0036). Mine leaves them
  untouched. The two proposals touch disjoint ids, and the full file I drafted still shows r22 and r42.
- **formulation.** I reworded r4 to say "the work that turns its replacement green" in place of "a slice";
  r10 (slicing hands back) is i10's.
- **analysis-tools.** r4 ("the line to give `plan log`") is i10's.
- **Red scenarios between work-items.** pytest-bdd's `scenarios()` binds a whole feature file, so formulated
  scenarios of work-items not yet green fail in the suite. `slice_expectations.py` handled this before;
  i10's supervisor has to know which failures are expected (by each work-item's `accepts`).
- **i11 runs after i10 is merged**, and so does work-item/rename-sweep, so the moves and the rename meet only
  what survives. The i8 work-items are blocked by i11's final-layout-read and deprecated-and-sources.
  work-item/migrate-plan needs `scripts/plan`'s format, which i10 deletes. The format is in its `--help`
  and in git history.

## What in the repository contradicts the directions

- `decisions/0022-plugin-adopts-the-design-model.md` and `docs/design-model/design-model.md` section 8 put
  `decisions/`, `work/` and `records/` at the top level. Decision 0045 supersedes 0022.
- `docs/capability-format.md` teaches a decision ledger (`spec/decisions.md`, `## design-decision/<slug>`
  entries) and `formulated_as`. `agents/capability-writer.md` writes `decisions.append.md`. spec-integration's
  Implementation section says "Decisions are appended to `spec/decisions.md` (to be replaced by
  `decisions/` files: initiative i3)".
- design-model-check r45, which reads a ledger, is built and approved, though decision 0032
  (model-reads-a-ledger) is rejected. r45 is removed, and decision 0049 supersedes 0032.
- `work/i8-model-in-consumers/initiative.md` says `@holding` → `@superseded`; the person's later direction
  is `@deprecated`. My draft of i8's initiative says `@deprecated`.
- spec/index.md's Testing section describes the docstring binding of decision 0028, which is rejected.
- Decisions' `source` fields are free text with relative paths: 30 of 36 name a file.
- `records/README.md` says the fixture-run logs are "not yet given ids".
- docs/capability-format.md and spec-integration#r17 tell a proposal to list a term in `adds`/`changes`/`removes`
  (`adds: [term/revision]`), but `scripts/model` reports any such entry as "not a requirement reference"
  (seen by running `model check` over these drafts). And design-model-check#r23 makes a proposal that removed a
  line unresolved for ever once it merges (its id is retired, and r23 reports removing a retired id). No
  proposal has done either yet. Both fixed in final-layout-design-model-check (r23 changed, r66 added;
  work-item/proposal-lists-read).
- Skills and agents write drafts under `.superpowers/` and read `spec/decisions.md`; `scripts/tools` keeps its
  map in `.superpowers/tools/coverage`.

## Risks

- **The pytest-bdd conversion is about 157 scenarios** (59 design-model-check, 63 feature-file-tools, 35
  analysis-tools). The step definitions are new code against tests that pass today. A scenario that fails
  once bound is a finding about the old test, not something to fix in the step. The work is split into five
  conversion work-items so that each fits one implementer.
- **kb's own test code reads the living plan by path.** `tests/slices.py` has
  `PLAN = "docs/superpowers/plans/2026-09-24-kb-slices.md"` and stops the run if it cannot read the plan.
  migration-tools r20 therefore rewrites moved paths in every tracked text file, not only Markdown, and lists
  each non-Markdown file it changed (spec-migration r23). If a step definition body names a moved path, this
  conflicts with spec-migration r7 ("no step definition's body changes"); the gate shows it.
- **After migration, consuming repositories still have `scripts/measure` writing
  `docs/superpowers/measurements/`** until i12 changes it. The first `measure batch` after migrating
  recreates `docs/superpowers/`.
- **`scripts/migrate` imports `scripts/model`'s frontmatter reader and `scripts/features`' parser** so that
  there is one reading of each. A change to either can break migrate. Its scenarios are the guard.
- **kb's gate is large.** It has two mapping questions, one enabling slice whose status says it was "done as
  165.4", and about 200 observation entries. The fixture case cannot show how a person handles a gate that
  size; the kb trial only shows the session's side.
- **`migrate run` numbers a partly numbered capability from one above its highest id.** For kb that is r1,
  since none is numbered. The 0.19.0 skill numbered "from r1 in its order" and did not cover partial
  numbering.

## Checked

The drafts were dropped into a copy of the repository and `scripts/model check` run over them: ids, `part_of`,
`under`, `for` and `blocked_by` all resolve. What it reports is expected before the work: `v_s3` and "accepts
… which no scenario names yet" for lines not yet formulated, `v_w4` for work-items whose every accepted line
is unformulated, r45's scenario until it is removed at formulation, the term entries above, and v_t1 on
literal `@holding` / `" (held)"` in design-model-check r51 and r62, migration-tools r2 and r27 and
spec-migration r18 (what r51's change is for) and on review r10, r11 and red-green r2, r11 (i10's).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/initiative.md`

~~~~~~
---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i11
title: This repository on the final layout and conventions
summary: This repository moves to the final layout and conventions of design model v3, the ones the plugin teaches and i8 migrates consuming repositories to.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 2
source: [observation/2026-10-19-final-state-only]
date: 2026-10-19
---

Covers:
- decisions as `spec/decisions/<n>-<slug>.md`, with a generated index;
- work and records under `.shop/`;
- decisions in the light form: a summary and a Decision section, with Context and Alternatives only for a
  real trade-off;
- ids in place of paths in references: `formulated_as` derived, and `source:` naming record ids;
- a plain label for every model rule, printed by `model check` and used by spec lines and skills;
- "deprecated" in place of held, holding and superseded (the person, 2026-10-19): the tag `@deprecated`,
  `features deprecate` and `features deprecated` for `hold` and `holding`, a `Deprecated for:` line,
  design-decision/held-scenario-formulates-no-requirement reworded, and the glossary entry **deprecated
  scenario** (Not: held, holding, superseded);
- "hold" and "carry" in their other senses reworded in plain words (stays valid, has, contains, enforced
  by, do), with carry added to the Not: lists;
- this repository's scenarios run as pytest-bdd step definitions (design-decision/plugin-scenarios-run-as-unittest
  was rejected 2026-10-19).

## The final state

**Layout** (design-decision/final-layout). `spec/` stands alone: `index.md`, `capabilities/<name>.md`, and
`decisions/<nnnn>-<slug>.md` with `decisions/index.md` written by `model decisions`. `features/<name>.feature`
stays with the code. `.shop/work/<initiative>/` holds the initiatives and their parts, `.shop/records/` the
records (`observations.md`, `measurements/`, `review-findings/`, `decision-arguments/`, `archive/`), and
`.shop/scratch/`, ignored by git, every draft, note and map a session writes. Nothing of the plugin is under
`docs/superpowers/` or `.superpowers/`. `scripts/model` reads that layout only, and reports the old one's
paths (`spec/decisions.md`, top-level `decisions/`, `work/`, `records/`) and an `@holding` tag as file
problems naming `scripts/migrate`: a repository not yet migrated fails the check rather than passing with
half its files unread.

**Decisions** (design-decision/light-decisions). New decisions are a summary and a Decision section;
Context and Alternatives only where options were weighed. Existing decision files keep their sections:
their record is not rewritten.

**References** (design-decision/references-are-ids). `formulated_as` is removed from every capability: the
feature file is `features/<name>.feature`. A decision's `source` is a list of ids; who and what else it came
from, in words, is `by`. So that sources can cite them, every Markdown record gets frontmatter: the archived
design notes are `decision-argument`s, the archived plans and requests `initiative-archive`s, the fixture-run
test logs `measurement`s, each `about` the bounded context.

**Rule labels.** Every `v_` and `w_` relation in `scripts/model.lp` has one plain label beside it
(`label("v_s3", "a requirement has no scenario")`), printed by `model check` beside the code, listed by
`model rules`, and used where the spec, the skills and `docs/capability-format.md` name a rule ("v_s3, a
requirement has no scenario"). The kb report-mode run of 0.20.0 found a session that did not know what
`v_s3` meant; the label is the answer.

**Deprecated.** `features deprecate`, `features deprecated`, `@deprecated`, " (deprecated)",
`Deprecated for:`. The glossary entry **deprecated scenario** (Not: held, holding, superseded) lets
`model check` find any line or scenario that slips back. Decisions keep their ids
(design-decision/held-scenarios, design-decision/held-scenario-formulates-no-requirement,
design-decision/rules-held-by-agent-tools, design-decision/suite-record-holds,
design-decision/plans-carry-intent-not-code): renaming their text is a migration, not an edit.

**Plain words.** "hold" and "carry" in their other senses become stays valid, has, contains, enforced by,
keep or do, in lines, scenarios, skills, agents, docs and the scripts' help. **requirement**'s Not: list
gains carry, carries, carried and carrying (the matcher allows a plural "s" only). The model's own text
(`docs/design-model/`) and records are left as written.

**pytest-bdd** (design-decision/plugin-scenarios-run-as-pytest-bdd). `python3 -m pytest` runs everything.
Each script capability's feature file is bound by `scenarios(...)` in `tests/scenarios/test_<capability>.py`,
its steps are step definitions there, and a scenario whose step has no definition fails. `features bindings
--unbound`, run by a unit test, fails the suite when a scenario has no test or two. `model check` counts a
requirement as covered when a scenario is tagged with it; with every tagged scenario a test that runs, that
count is exact. The docstring binding (`tests/scripts/binding.py`) goes, except for `batch-measurement`,
left to i12. Unit tests that bind no scenario stay as `unittest` tests in `tests/scripts/`, collected by
pytest.

## What is removed

`spec/decisions.md`; `decisions/`, `work/`, `records/` and `docs/superpowers/` at the top level (moved); the
`formulated_as` field; design-model-check#r45 (reading a ledger); `features hold` and `features holding`;
the docstring binding test in each test module but `test_measure.py`.

## What is left alone

- `scripts/measure`, `spec/capabilities/batch-measurement.md` but two words (final-layout-batch-measurement),
  `skills/analyzing-a-batch` and `tests/scripts/test_measure.py` (i12). `measure` still writes under
  `docs/superpowers/measurements/` and reads `docs/superpowers/plans/`; i12 moves it to
  `.shop/records/measurements/`. The kb baseline files move to `.shop/records/measurements/kb-baseline-2026-10-11/`,
  and `measure compare` takes them by path, so nothing it needs is lost.
- Slicing, slice plans, lanes, `scripts/plan` and the delivery skills: i10 removes them. i11's work-items run
  after i10's are merged, so the rename and the moves meet only what survives.
- `docs/design-model/`: the model's text, owned with shopsystem-knowledge; only section 8's layout gets a dated
  note pointing at design-decision/final-layout.

## Parts

Capability-proposals: final-layout-design-model-check, final-layout-feature-file-tools,
final-layout-formulation, final-layout-spec-integration, final-layout-analysis-tools,
final-layout-batch-measurement; and the formulated withdrawn-design-model-check. Spec index and glossary:
`spec-index.md`. Decisions 0045-0048.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/spec-index.md`

~~~~~~
---
id: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
title: shopsystem-bdd
---

# shopsystem-bdd

**State.** Plugin 0.20.0. Every approved Behaviour line describes what the plugin does; requirements have
ids from the start (design model v3). Drafted and not yet approved, all awaiting the gate: i1's ten open
proposals (three withdrawn 2026-10-19 with the slicing, slice-plan-tool and batch-analysis capabilities), i2's, i3's five, and i9's (the ubiquitous language), and the script capabilities' lines reworded to the code during formulation
(listed for the gate in the release's test log). What is approved and unbuilt lives under `Not yet`.
Check with `python3 scripts/model check`; the decisions index, `spec/decisions/index.md`, is written by `python3 scripts/model decisions`;
`python3 scripts/model rules` lists every rule with its label.

## Purpose

A Claude Code plugin that runs a behaviour-driven workflow in a consuming repository: one spec of
capability files per bounded context, Gherkin feature files paired with them as the contract, thin
vertical slices, implementation red-green, review, and measurement of what a batch cost. One human gate,
on the spec's Behaviour lines. It is not a test runner, not a project manager, and keeps no state of its
own outside the consuming repository's files.

## Constraints

- The design model, version 3 (`docs/design-model/`): standing artifacts, initiatives and parts, records;
  grammar.md's rules are kept by this repository's files, in the layout of design-decision/final-layout.
- Claude Code's plugin format: skills, agents with tool lists, `skills` preloading; a plugin agent's hooks
  and permissionMode are ignored, so a role's rules are enforced by its tools (design-decision/rules-held-by-agent-tools).
- superpowers as a declared dependency (design-decision/superpowers-dependency).
- The dependencies the plugin needs, named in its documentation: clingo, pytest, pytest-bdd
  (design-decision/plugin-takes-the-dependencies-it-needs; the solver: design-decision/model-check-solves-with-clingo).

## Composition

The spec side, with the person:

| capability | narrator | group |
|---|---|---|
| `spec-integration` | the person at the gate | service |
| `formulation` | the person who approved the lines | service |
| `spec-migration` | the person migrating a repository onto spec/ | service |
| `spec-consistency` | the person keeping a spec | service |

The build side, dispatched:

| capability | narrator | group |
|---|---|---|
| `code-research` | the session that plans a batch | service |
| `red-green` | the controller that dispatched the implementer | service |
| `review` | the controller closing a task or a batch | service |
| `role-boundaries` | the person running the workflow | guarantees |

Measurement:

| capability | narrator | group |
|---|---|---|
| `batch-measurement` | a session measuring a closed batch | service |

Tools the skills and agents run:

| capability | narrator | group |
|---|---|---|
| `feature-file-tools` | an agent or session editing feature files | service |
| `analysis-tools` | an agent researching or reviewing a project's code | service |
| `design-model-check` | a person or agent checking a repository against the design model | service |

## Testing

- The suite: `python3 -m pytest` from the root. A script capability's scenarios run as pytest-bdd step
  definitions, one module per feature file under `tests/scenarios/`, and `features bindings --unbound`
  fails the suite when a scenario has no test or two (design-decision/plugin-scenarios-run-as-pytest-bdd).
  Unit tests that bind no scenario are `unittest` tests under `tests/scripts/`. `batch-measurement` keeps its
  docstring binding until initiative i12.
- Workflow capabilities (agents and skills): fixture runs recorded under `.shop/records/measurements/fixture-runs/`,
  and batches measured with `scripts/measure`. How their requirements get acceptance-scenarios is open
  (initiative i1); until then `model check` reports them under v_s3.
- `role-boundaries` is guarantees: checked against `agents/*.md`, not by scenarios.

## Glossary

- **batch**: the slices one session plans and one controller executes, archived and measured together.
- **controller**: the session that dispatches implementers and reviewers for a batch.
- **deprecated scenario**: a scenario kept in the suite, tagged `@deprecated`, after its line is changed or removed, until its replacement is green; it formulates no requirement. Not: held, holding, superseded.
- **fact**: one statement `model facts` gives clingo about the repository's files.
- **hand-back**: an implementer's stop on an observed condition, logged with its evidence.
- **requirement**: one Behaviour line of a capability, named `#r<n>`. Not: behaviour requirement, capability requirement, carry, carries, carried, carrying.
- **slice**: a unit of work with an observable done (scenarios or a check); to become a work-item (i4).
- **suite record**: a whole-suite result logged once and used while nothing it depends on has changed.

## Where things live

`spec/` (this index, `capabilities/`, `decisions/` with its generated `index.md`), `features/`, `.shop/work/`,
`.shop/records/` (observations, measurements, review-findings, decision-arguments, archive), `.shop/scratch/`
(drafts and notes, ignored by git), `docs/design-model/` (the model), `docs/capability-format.md` (the format
the plugin teaches consuming repositories).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/final-layout-analysis-tools.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-analysis-tools
kind: capability-proposal
part_of: initiative/i11
status: drafted
date: 2026-10-19
argues: [analysis-tools]
changes: [analysis-tools#r8, analysis-tools#r14]
---

# Analysis tools: the map under .shop/scratch

`tools map` keeps its map in `.shop/scratch/tools/coverage` (r8), since the plugin no longer uses
`.superpowers/` (design-decision/final-layout). r14's "files holding them" becomes "files that contain them".
The proposed file is `capabilities/analysis-tools.md`. This capability's scenarios are the first to move to
pytest-bdd (work-item/analysis-tools-scenarios).

r4 ("the line to give `plan log`") is left to initiative i10, which removes `scripts/plan`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/final-layout-batch-measurement.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-batch-measurement
kind: capability-proposal
part_of: initiative/i11
status: drafted
date: 2026-10-19
argues: [batch-measurement]
changes: [batch-measurement#r10, batch-measurement#r16]
---

# Batch measurement: two words, nothing else

batch-measurement stays as it is until initiative i12 (the person, 2026-10-19). Two of its lines use words the
glossary now avoids, and `model check` would report them under v_t1: r10 ("however many transcript rows
carry it" → "it appears in") and r16 ("the tasks the batch plan held" → "had"). Nothing in `scripts/measure`
changes. Four scenario steps follow at formulation: "the repository holding one living plan", "a repository
holding <plans> … files", "held 5 tasks … the 7 held", "is carried by three transcript rows". Their titles,
which bind the tests, do not change.

The alternative is to leave the words and accept v_t1 rows until i12; NOTES.md recommends this proposal.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/final-layout-design-model-check.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-design-model-check
kind: capability-proposal
part_of: initiative/i11
status: drafted
date: 2026-10-19
argues: [design-model-check]
adds: [design-model-check#r60-r66]
changes: [design-model-check#r2-r8, design-model-check#r10, design-model-check#r11, design-model-check#r14, design-model-check#r15, design-model-check#r19, design-model-check#r20, design-model-check#r23, design-model-check#r26, design-model-check#r33-r35, design-model-check#r37, design-model-check#r44, design-model-check#r51-r54, design-model-check#r59]
removes: [design-model-check#r45]
---

# Design model check: the final layout, ids for references, labels for rules

`model` reads the final layout and nothing else (design-decision/final-layout), derives a capability's feature
file from its name, reads a decision's `source` as ids (design-decision/references-are-ids), reads
`@deprecated` in place of `@holding`, and prints every rule with a plain label. The proposed file is
`capabilities/design-model-check.md` beside this one.

What the gate sees, by id:

- The layout: r19 (what is read), r14, r15, r37 (`spec/decisions/index.md`), r20 and r26 (the feature file is
  `features/<name>.feature`), r45 removed (no ledger is read), r60 (`formulated_as` is a file problem), r61
  (an old layout's paths are file problems, naming `scripts/migrate`).
- References: r64 (a decision's `source` is ids, `by` is not read). r24 is unchanged: `source` was already in
  its list, and now covers a decision's too.
- Proposals' lists: r66 reads `term/<term>` in `adds`, `changes` and `removes`, as docs/capability-format.md
  and spec-integration#r17 already tell a writer to list a term (today `model check` reports every such entry
  as "not a requirement reference"); r23 lets a merged or formulated proposal's `removes` name the id it
  retired (today a proposal that removed a line is unresolved for ever once it merges, so this proposal's own
  removal of r45 would be).
- Decisions: r63 (a decision file needs `## Decision`, design-decision/light-decisions).
- Deprecated: r26, r44, r62 (`@holding` is a file problem, not read as `@deprecated`).
- Labels: r2, r11, r33 (printed with the code; mapped in `--json`), r65 (`model rules`), and each line that
  names a rule now names its label too: r3-r8, r10, r34, r35, r52-r54, r59.
- Mentions: r51 reads no mention inside a code span, a double-quoted string or an `@` tag, so a line or step
  that names a literal (the tag `@holding` in r62 and in migration-tools, `" (held)"`) is not a use of the
  word the glossary avoids. It also says contains for holds.
- Plain words: r4 (carry → have), r34 (hold → have); Purpose likewise.

r22 and r42 (`#behaviour/r<n>`) are left as they are: design-decision/one-requirement-form retires them in
initiative i10.

The labels, one per rule `model.lp` shows, written once there:

| code | label |
|---|---|
| v1 | needs on something that is not a part |
| v2 | a standing edge touches something that is not standing |
| v3 | a scenario is on a needs edge |
| v4 | a depends_on that no using gives |
| v5 | a using against the pin |
| v6 | a crossing names no seam |
| v6b | a job-thread is mapped with a crossing that names no seam |
| v7 | a cross-context-request names no capability it comes from |
| v7b | a cross-context-request is across the wrong seam |
| v7c | an upstream names a downstream client |
| v8 | a work-item names no capability |
| v9a | a part has no part_of |
| v9b | a part has two part_of |
| v9c | a part reaches no initiative |
| v9d | a priority on something that is not an initiative |
| v9e | a source on something that is not an initiative |
| v9f | an initiative is part of something |
| v9g | a part_of cycle |
| v10a | a source that is not an origin |
| v10b | a record is about nothing |
| v10c | a record is about something that is not standing |
| v11 | a capability without exactly one narrator |
| v12a | a decision has no summary |
| v12b | a supersedes cycle |
| v13 | a revisit signal no one reads |
| v15a | a requirement has no id |
| v15b | two requirements share an id |
| v15c | a retired id is used again |
| v15d | a requirement id outside its capability |
| v15e | a proposal changes a requirement no capability has |
| v15f | a formulated proposal leaves a requirement without a scenario |
| v_k1 | a job initiative's first part is not a job-proposal |
| v_k2 | a job-path initiative's first part is not a job-thread |
| v_k3 | a capability-change initiative's first part is not a capability-proposal |
| v_k4 | a defect initiative's first part is not a work-item |
| v_k5 | an initiative has more than one first part |
| v_k6 | a capability-proposal argues more than one capability |
| v_b1 | a work-item is part of something other than a capability-proposal |
| v_b2 | a cross-context-request has a part that is not a capability-proposal |
| v_b3 | a job-thread has a part of the wrong kind |
| v_s1 | a scenario names no requirement |
| v_s2 | a scenario names two requirements |
| v_s3 | a requirement has no scenario |
| v_w1 | a blocked_by cycle |
| v_w2 | a ready work-item is blocked by one not green |
| v_w3 | two claimed work-items claim one file |
| v_w4 | a work-item has no acceptance and no check |
| v_d1 | a done initiative has a part open |
| v_d2 | an abandoned initiative has a part open |
| v_t1 | a word the glossary avoids |
| v_t2 | a term has two entries |
| v_t3 | an avoided word is a term |
| w_unserved_cap | a capability serves no job |
| w_unserved_job | a job nothing serves |
| w_seam_unused | a seam nothing crosses |
| w_uncited_obs | an observation no initiative cites |
| w_many_requests | more than five open requests across one seam |
| w_stale_intake | an initiative proposed more than 90 days ago |

Formulation follows: the scenarios of the changed lines are reworded; steps that use "holding" or "holds"
("a directory holding", "one JSON object holding") are reworded with their lines, since the new glossary
entry avoids "holding".
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/final-layout-feature-file-tools.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-feature-file-tools
kind: capability-proposal
part_of: initiative/i11
status: drafted
date: 2026-10-19
argues: [feature-file-tools]
adds: [feature-file-tools#r57-r59, term/deprecated-scenario]
changes: [feature-file-tools#r2-r5, feature-file-tools#r8, feature-file-tools#r10, feature-file-tools#r18-r24, feature-file-tools#r35, feature-file-tools#r39-r41, feature-file-tools#r45, feature-file-tools#r51, feature-file-tools#r53, feature-file-tools#r54, term/requirement]
---

# Feature file tools: deprecate, and every scenario bound once

"Deprecated" in place of held, holding and superseded (the person, 2026-10-19), and `features bindings`
able to show that every scenario has exactly one test, which is how this repository's scenarios stay
covered under pytest-bdd (design-decision/plugin-scenarios-run-as-pytest-bdd). The proposed file is
`capabilities/feature-file-tools.md`.

- Deprecate: `features hold` becomes `features deprecate` (r19, r20, r35, r39), `features holding` becomes
  `features deprecated` (r21, r22, r40), `retire` acts on `@deprecated` (r23, r24). The title suffix is
  " (deprecated)" and the description line `Deprecated for:`. `deprecated` names the replacement's file and
  `@r<n>` tag where `holding` named its slice tag (r21, r40); a missing `Deprecated for:` line is said, not
  printed as `for: None` (observation/2026-10-16-release-0-19-0-defects).
- Bindings: r57 (`scenarios(...)` binds every scenario of the files it names), r58 (`--unbound` reports a
  scenario bound by no test), r59 (and one bound twice).
- Plain words: "hold"/"holds" → "has", "contains", "include"; "carrying" → "with" (r2-r5, r8, r10, r18, r41,
  r45, r51, r53, r54).
- Glossary (spec/index.md, proposed in `spec-index.md` beside this file): adds **deprecated scenario**
  (Not: held, holding, superseded); changes **requirement**, whose Not: list gains carry, carries, carried,
  carrying (the matcher allows only a plural "s", so each form is listed).

The slice lines (r8-r11, r30-r34, r43-r50) are left to initiative i10, which removes slicing; where i10
retires r8 or r10, their rewording here is dropped.

Formulation follows: the deprecate scenarios are rewritten from the changed lines, and every scenario whose
title or steps say held, holding or superseded is reworded, since v_t1 reads titles and steps.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/final-layout-formulation.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-formulation
kind: capability-proposal
part_of: initiative/i11
status: drafted
date: 2026-10-19
argues: [formulation]
changes: [formulation#r1, formulation#r4, formulation#r6, formulation#r11, formulation#r12]
---

# Formulation: deprecated scenarios

A scenario kept while it passes is deprecated, tagged `@deprecated` with " (deprecated)" on its title and a
`Deprecated for:` line (r1, r4, r12), done with `features deprecate`. r4 no longer names a slice: "until the
work that turns its replacement green retires it", which reads the same under i10's work-items. Plain words:
r6 (holds → contains), r11 (carries → has). The proposed file is `capabilities/formulation.md`.

r10 (slicing hands back a scenario) is left to initiative i10.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/final-layout-spec-integration.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-spec-integration
kind: capability-proposal
part_of: initiative/i11
status: drafted
date: 2026-10-19
argues: [spec-integration]
adds: [spec-integration#r20-r22]
changes: [spec-integration#r9, spec-integration#r17, spec-integration#r19]
---

# Spec integration: decision files in the light form

A decision is drafted as its own file in `spec/decisions/`, in the light form (design-decision/light-decisions),
its `source` naming ids and its `by` the rest (design-decision/references-are-ids), and the index is
regenerated in the spec commit (r20-r22). r9 says the delegation in `by`, where it said it in the source;
r17 and r19 name `.shop/work/`. Implementation: drafts under `.shop/scratch/drafts/`, no ledger. The
proposed file is `capabilities/spec-integration.md`.

The Not yet entry's trigger named i8, which is now migration only; it is reworded to a consuming
repository asking for it.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/capabilities/analysis-tools.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
title: Analysis tools
narrator: an agent researching or reviewing a project's code
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs]
retired: []
---

# Analysis tools

## Purpose
`scripts/tools` finds and installs a project's analysis tools in the project's own interpreter, and gives one
interface to them: a coverage map of which tests execute which code, the functions no test executed, the
references to a name, and a lint check. It is not a test runner for the fast suite and edits no dependency
file; it reports what the tools found and names a tool that is missing rather than skipping it.

## Behaviour
- [r1] **When** `tools` needs an interpreter, it uses the first of these, in this order: the one `--python` gives, used as given; `.venv/bin/python` under the current directory, if that file exists; `venv/bin/python` under the current directory, if that file exists; `$VIRTUAL_ENV/bin/python`, if that file exists, wherever `$VIRTUAL_ENV` points; and else the interpreter running the script. Unless `--log` is given, `tools probe` prints that interpreter's path and whether it came from `--python`, from the project's virtualenv (`.venv`, `venv` or `$VIRTUAL_ENV` alike), or from neither.
- [r2] **If** the project is not a Python project, `tools probe`, `tools install` and `tools check` say in one line that no analysis tools are known for its language and exit 1.
- [r3] **When** `tools probe` is run, `tools` prints one line per tool, `<name> <version>` for an installed tool and `<name> missing: <what it is for>` for a missing one, then the interpreter, and exits 1 when any tool is missing.
- [r4] **When** `tools probe --log` is run, `tools` prints the one `Probe: tools -> ...` line to give `plan log`.
- [r5] **When** `tools install` is run, `tools` installs each missing tool into the interpreter with pip and edits no dependency file.
- [r6] **If** the interpreter is not a virtualenv, `tools install` refuses to install into it and says so.
- [r7] **If** a tool is still missing after `tools install`, `tools` prints the tool, what it is for, what the workflow does without it, and the command that failed with the end of its error, and exits 1.
- [r8] **When** `tools map` is run, `tools` runs the suite once under coverage with a context per test, passing arguments after `--` to pytest, and keeps the map in `.shop/scratch/tools/coverage`.
- [r9] **When** `tools tests-of <file>[:<function, Class.method or line range>]` is run, `tools` prints each test that executed it in the last map, one a line, and how many of the map's tests that is, with the commit the map was made at.
- [r10] **Where** `--by-file` is given, `tools tests-of` prints a count for each test file instead of each test.
- [r11] **If** no test in the map executed the target, or the file has no function by that name, `tools tests-of` exits 1.
- [r12] **If** no map has been made, `tools tests-of` refuses and says to make one with `tools map`.
- [r13] **When** `tools untested <file>...` is run, `tools` prints each function in the files that no test in the last map executed.
- [r14] **When** `tools refs <name>` is run, `tools` prints every reference to that function, class or name defined in the project as `path:line`, including uses through an import or an alias, then one summary line with the number of references, the number of production files that contain them and, as a separate number, the number of test files that contain them, and where the name is defined.
- [r15] **If** nothing in the project is defined as `<name>`, `tools refs` exits 1.
- [r16] **When** `tools check` is run, `tools` runs ruff and vulture over the paths given or the Python files changed since `--base` and, where the project has import contracts, import-linter over the project, each under its own heading, and exits 1 when any reports.
- [r17] **If** a tool `tools check` would run is missing, `tools` names it as missing under its heading instead of skipping it.
- [r18] **If** the interpreter is not a virtualenv and a tool is missing, `tools install` installs nothing, prints for each missing tool the tool, what it is for, what the workflow does without it and that the interpreter is not a virtualenv, and exits 1.
- [r19] **When** `tools install` finds every tool present, `tools` says so and exits 0, whether or not the interpreter is a virtualenv.
- [r20] **When** `tools install` installs a tool, `tools` prints that the tool is installed.
- [r21] **If** the interpreter does not run, `tools probe`, `tools install` and `tools check` refuse, naming it and the end of its error.
- [r22] **When** `tools probe --log` is run, the line names every tool with its version or `missing`.
- [r23] **When** `tools map` is run, `tools` replaces any earlier map, prints pytest's last line, where the map is and the commit it was made at, and exits 0 whether or not the tests passed.
- [r24] **If** `tools map` makes no map, `tools` refuses, naming the command it ran and the end of its output.
- [r25] **When** `tools untested` is run, `tools` prints each function as `<path>:<line> <name>`, then how many functions no test executed and the commit the map was made at, and exits 0 however many there are.
- [r26] **If** no map has been made, `tools untested` refuses and says to make one with `tools map`.
- [r27] **If** coverage is missing from the interpreter, `tools tests-of` and `tools untested` refuse, saying to run `tools install`.
- [r28] **If** jedi is missing from the interpreter, `tools refs` refuses, saying to run `tools install`.
- [r29] **If** the file `tools tests-of` is given does not exist, `tools` refuses, naming it.
- [r30] **When** `tools refs` is run on a name the project defines, `tools` names where it is defined, counts no definition as a reference, and exits 0 however many references there are.
- [r31] **Where** `--base` is given, `tools check` checks the Python files changed since it and not deleted, in place of any paths given.
- [r32] **If** git cannot compare the working tree with `--base`, `tools check` refuses with git's error.
- [r33] **Where** `tools check` has no file to check, it says under the ruff and vulture headings that there is nothing to check, and those two do not make it exit 1.
- [r34] **Where** the project states no import contracts, `tools check` says so under the import-linter heading and does not run it.
- [r35] **When** a tool `tools check` runs prints nothing, `tools check` says under its heading that it is clean.

## Implementation, may change
- The tools probed are coverage, pytest-cov, jedi, ast-grep, ruff, vulture, import-linter and hypothesis.
- A Python project is one with `pyproject.toml`, `setup.py`, `setup.cfg`, `pytest.ini`, `requirements.txt`,
  `tox.ini` or any `.py` file under the current directory.
- `install` runs `<interpreter> -m pip install <package>` per missing tool.
- `map` runs `pytest -q --cov=. --cov-context=test`, writes the commit it was made at beside the data, and is
  its own command, never part of the fast suite. Code on the path of every call is executed by most of the
  suite, so the map narrows a search only for code off that path; a test that ran and failed counts.
- When the interpreter is not the one running the script, the script re-runs itself under it.
- `refs` uses jedi, so it reads the code as the interpreter would and does not find a name built from a
  string. A test file is under a tests or test directory or named `test_*` or `*_test.*`.
- `check` treats `.importlinter` or a `[tool.importlinter` table in `pyproject.toml` as the project's import
  contracts, and says so under the import-linter heading when there are none; headings are `== <tool> ==`.
- Exit status: 0 success, 1 something is missing, refused or reported, 2 bad usage.

## Not yet
- Only Python projects are known; in any other, agents search by text and say that they did — trigger: a project in another language asks for its analysis tools.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/capabilities/batch-measurement.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement
title: Batch measurement
narrator: a session measuring a closed batch
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/measure-refuses-unknown-shapes, design-decision/an-experiment-is-a-release]
retired: []
---

# Batch measurement

## Purpose
`scripts/measure` writes one facts file for a batch, from Claude Code's session transcripts, the plan and git:
dispatches, their tokens, time, attribution, findings and commits, the slices' Lands lines against the files
touched, tasks, hand-backs and the suite record. It also prints a facts file, or two side by side. It is not a
judgement of the batch and does not change the repository's code, plan or transcripts; it refuses rather than
guesses when its inputs are not what it knows.

## Behaviour
- [r1] **When** `measure batch <archive file>` is run, `measure` writes one facts file for the batch running from the commit that added the archive file before it to the commit that added its own.
- [r2] **Where** no archive file is given, `measure batch` measures the open batch, from the last archive commit to now, reading the living plan.
- [r3] **Where** `--from` or `--to` is given, as a commit or an ISO time, `measure batch` uses it in place of that end of the batch.
- [r4] **Where** no `--out` is given, `measure batch` writes the facts to `docs/superpowers/measurements/<archive file's name without .md>.json`.
- [r5] **If** the archive file was not added by any commit, `measure batch` refuses, naming the file.
- [r6] **If** a transcript's shape is not known, `measure batch` refuses, naming the file and what was missing, and writes no facts file.
- [r7] **If** the facts file exists and `--replace` is not given, `measure batch` refuses and leaves the file as it was.
- [r8] **If** no dispatch is found inside the batch, `measure batch` refuses, naming the window it searched, and writes nothing.
- [r9] A subagent transcript that starts inside the batch is counted as a dispatch, and one that starts outside it is not.
- [r10] A request's usage is counted once in the facts, however many transcript rows it appears in, and its reasoning tokens are a part of its output tokens: the facts report reasoning as "of which" the output figure and never add it to that figure.
- [r11] The facts count a session's own requests inside the batch as the controller's when that session dispatched there.
- [r12] The facts attribute a dispatch to a slice or batch work by its description, failing that by the task or slice its prompt names, and otherwise count it as unattributed.
- [r13] The facts count a reviewer's findings as it wrote them: its lines beginning Critical or Important, and its stated count of Minor.
- [r14] The facts give each commit to the implementer running when it was made, and count the files it touched as production, test or other.
- [r15] The facts give each slice its Lands line from the archive file, or the living plan for the open batch, the numbers of production and test files it says it will land, beside the numbers of production, test and other files its dispatches touched.
- [r16] The facts give the tasks the batch plan had when it was added and the tasks it had at the batch's end, the plan's hand-back entries and its suite record.
- [r17] The facts hold no prompt, reply or tool content.
- [r18] **When** `measure show <file>` is run, `measure` prints the facts file as tables.
- [r19] **When** `measure compare <a> <b>` is run, `measure` prints the two facts files side by side.
- [r20] **If** `measure show` is given a file that is not a facts file `measure` wrote, `measure` refuses, naming the file.
- [r21] **If** no archive file is given, no `--plan` is given and the repository holds no `docs/superpowers/plans/*-slices.md` or several, `measure batch` refuses, saying to name the living plan with `--plan`.
- [r22] **If** no archive file was added before the batch's end and no `--from` is given, `measure batch` refuses, saying to give the batch's start with `--from`.
- [r23] **If** `--from` or `--to` is neither a commit nor an ISO time, `measure batch` refuses, naming what it was given.
- [r24] **If** `--repo`, default the current directory, is not inside a git repository, or a git command `measure batch` runs fails, `measure` refuses with git's error.
- [r25] **Where** no archive file is given, `measure batch` names the batch `--name`, default `open`, and without `--out` writes the facts to `docs/superpowers/measurements/<name>.json`.
- [r26] **Where** no archive file is given, the open batch starts at the last commit that added a file under `--archive-dir`, default `docs/superpowers/plans/archive`.
- [r27] The facts hold the archive file's slices and every other slice a dispatch is attributed to, and for the open batch only the slices a dispatch is attributed to.
- [r28] The facts count, as ambiguous, the commits made while more than one implementer was running.
- [r29] **If** no dispatch names a ledger and no `--tasks` is given, or the batch plan is in no commit, the facts leave tasks uncounted and hold a note saying why, and `measure batch` writes the note on stderr.
- [r30] **When** `measure batch` has written the facts, it prints one line naming the file, the number of dispatches and slices, and the window.
- [r31] The facts give each dispatch the closing status its reply states, and count replies that close BLOCKED, PARTIAL or NEEDS_CONTEXT as not done.
- [r32] The facts record the plugin and harness versions the transcripts name, and the batch's window as times and, where known, commits.
- [r33] **Where** the batch starts at a commit, the facts give the files and lines changed from it to the batch's end commit, or to HEAD when the end is not a commit.
- [r34] The facts count the dispatches given more than one prompt as resumed; they give the share of building time from the first branch review on, where building time is the dispatches' own durations summed and not wall-clock time, and a scout's dispatches are left out of both that time and the part of it from the first branch review on; and they give the mean and summed starting context of the dispatches.
- [r35] **When** `measure show` is run, `measure` prints the repository, batch, window, plugin and harness versions and suite record, then the summary, roles and slices tables, the dispatches not done or not attributed, each hand-back and each note.
- [r36] **When** `measure compare` is run, `measure` prints each summary figure and the output, new input, cache read and agent minutes per slice (each summary figure divided by the file's slices) of both files, each file headed by its batch and plugin versions, with the ratio of the second to the first.
- [r37] **If** `measure compare` is given a file that is not a facts file `measure` wrote, or `measure show` or `measure compare` a file it cannot read as JSON, `measure` refuses, naming the file.
- [r38] **If** `measure` refuses, it says why on stderr and exits 1.

## Implementation, may change
- Sessions are read from `~/.claude/projects` (or `--projects`), in the directory named after each worktree of
  the repository; `--sessions` names directories outright. Subagents are the `subagents/*.jsonl` beside a
  session, with a `.meta.json` carrying `agentType` and description.
- Tokens are output, new input (input and cache writes) and cache read; context is the whole input of one
  request; a dispatch's effort is the setting most of its requests ran at.
- Description attribution recognises 'slice <n>', 'step <k>', 'task <n>', 'batch' and 'slices', and a leading
  'spec'; the prompt is searched for a ledger's task brief. A dispatch's kind follows its role and the words
  fix, re-review and probe.
- With two implementers running at a commit, it goes to the later-started one and is counted as ambiguous.
  A test file is under a tests or test directory or named `test_*` or `*_test.*`; `docs/`, `features/`,
  `spec/`, `.superpowers/` and Markdown are other; the rest is production.
- The batch plan is the one the dispatches' ledger names, or `--tasks`; when it cannot be read, tasks are not
  counted and a note says so on stderr.
- The facts file is JSON with a version number; `show` refuses a file of another version.
- Transcripts are removed by the harness after some weeks and found only on the machine and paths the batch
  ran in, which is why a facts file is never written over without `--replace`.
- Exit status: 0 success, 1 refused, 2 bad usage.

## Not yet
None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/capabilities/design-model-check.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or agent checking a repository against the design model
group: service
rests_on: [design-decision/final-layout, design-decision/references-are-ids, design-decision/light-decisions, design-decision/model-check-solves-with-clingo, design-decision/scenario-names-requirement-by-tag, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped]
retired: [r45]
---

# Design model check

## Purpose
`scripts/model` reads a bounded context's files — spec, feature files, decisions, work and records, in the
final layout and no other — as the facts of `docs/design-model/grammar.md`, and reports what the grammar
refuses, each rule by its code and its plain label. It also writes the generated decisions index, lists the
rules, and traces a requirement to why it exists. It does not edit the spec, the work or the records, and it
checks one bounded context: product-level artifacts are read only where the files contain them.

## Behaviour
- [r1] **When** `model check` finds no violation, unresolved reference or file problem, it says so with the counts and exits 0.
- [r2] **When** `model check` finds violations, it prints each violated relation by its grammar.md name and its plain label, with its rows, and exits 1.
- [r3] **If** a requirement bullet in a capability's Behaviour has no `[r<n>]`, `model check` reports it under v15a, a requirement has no id.
- [r4] **If** two requirements of one capability have the same id, `model check` reports them under v15b, two requirements share an id.
- [r5] **If** a capability uses an id it lists as retired, `model check` reports it under v15c, a retired id is used again.
- [r6] **If** a capability-proposal changes a requirement no capability has, `model check` reports it under v15e, a proposal changes a requirement no capability has.
- [r7] **If** a capability-proposal is `formulated` while a requirement it adds or changes has no scenario, and the capability is not guarantees, `model check` reports it under v15f, a formulated proposal leaves a requirement without a scenario.
- [r8] **If** a requirement of a capability that is not guarantees has no scenario naming it, `model check` reports it under v_s3, a requirement has no scenario.
- [r9] **If** a scenario names a requirement its capability does not have, or a capability rests on a decision that does not exist, `model check` reports the unresolved reference and exits 1.
- [r10] **If** a part has no `part_of`, or its `part_of` chain does not reach an initiative, `model check` reports it under v9a, a part has no part_of, or v9c, a part reaches no initiative.
- [r11] **When** `model check` finds warnings, it prints each warning relation with its plain label and its count, and they alone do not change the exit status.
- [r12] **If** the clingo package is missing, `model check` says so with the command that installs it and exits 2.
- [r13] **When** `model facts` is run, it prints the facts read, one a line in clingo's syntax, using only the standard library.
- [r14] **When** `model decisions` is run, `spec/decisions/index.md` lists every decision in `spec/decisions/` with its summary, status, what it supersedes and when to revisit it, each linked to its file.
- [r15] **When** `model decisions --check` is run and `spec/decisions/index.md` is not what `model decisions` would write, it says so, exits 1 and writes nothing.
- [r16] **When** `model why <capability>#r<n>` is run, it prints the requirement, each capability-proposal that adds or changes it, the `part_of` chain to its initiative and the initiative's sources.
- [r17] **If** no capability-proposal adds or changes the requirement, `model why` says so and exits 1.
- [r18] **Where** a proposal's or work-item's list names `<capability>#r<a>-r<b>`, `model` reads it as every id from a to b.
- [r19] `model` reads, under `--root` (default the current directory), `spec/index.md`, `spec/capabilities/*.md`, every `*.feature` under `features/`, every `spec/decisions/*.md` but `index.md`, `.shop/work/<initiative>/*.md`, `.shop/records/observations.md` and any other Markdown under `.shop/records/` whose frontmatter has an `id`, and nothing else.
- [r20] A scenario names a requirement by a tag `@r<n>`, its own or its feature's, in `features/<capability name>.feature`.
- [r21] A reference written `<name>#r<n>` or `capability/<name>#r<n>` is read as a requirement of the capability `capability/<context path>/<name>` in the bounded context, the field fixing the kind where it is written `<name>`.
- [r22] **If** a list names a reference that is not `<capability>#r<n>` or `<capability>#behaviour/r<n>`, with the capability written `capability/<context path>/<name>`, `capability/<name>` or `<name>`, or a range `#r<a>-r<b>` with a greater than b, `model check` reports it as unresolved.
- [r23] **If** a capability-proposal adds or removes a requirement no capability has, `model check` reports it as unresolved, except that adding an id the capability lists as retired is reported under v15c, and removing an id the capability lists as retired is read as that requirement where the proposal is `merged` or `formulated`.
- [r24] **If** a `supersedes`, `source`, `part_of`, `argues`, `under`, `for`, `blocked_by` or `depends_on` names nothing in the repository, or names a node of the wrong kind (`supersedes` needs a design-decision, `under` and `depends_on` a capability, `for` and `blocked_by` a work-item), `model check` reports it as unresolved.
- [r25] **If** `spec/index.md` is missing or has no `id`, a capability's `id` is not `capability/<context path>/<file name>`, a capability has no `## Behaviour` section, or its `retired` lists an entry that is neither `r<n>` nor a number, `model check` reports a file problem naming the file.
- [r26] **If** a feature file is not `features/<name>.feature` for a capability `<name>`, or two of its scenarios share a title, `model check` reports a file problem naming the file. A scenario tagged `@deprecated` is not counted in the title check.
- [r27] **If** a work directory has no `initiative.md`, an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, an initiative's priority is not a number or its date is not `YYYY-MM-DD`, `model check` reports a file problem naming the file; for a work directory with no `initiative.md` it names the directory, not the missing file.
- [r28] **If** a work-item accepts a requirement no scenario names yet, `model check` reports a file problem naming the work-item's file.
- [r29] **If** a decision has no `id`, a record with an `id` has a kind that is not a record kind, a frontmatter value is written as a folded or literal block, or one id names nodes of two kinds, `model check` reports a file problem.
- [r30] **If** `model check` finds a file problem, it prints each and exits 1.
- [r31] **When** `model check` ends without `--json`, it prints the counts of violations, warnings, unresolved references and file problems.
- [r32] **Where** `--limit <n>` is given, default 10, `model check` prints at most n rows of each violated relation and how many more there are.
- [r33] **Where** `--json` is given, `model check` prints the violations, warnings, unresolved references and file problems as one JSON object, with each code printed mapped to its plain label, and the same exit status.
- [r34] **If** an initiative that is not a capability-change has more than one part directly under it, `model check` reports it under v_k5, an initiative has more than one first part, while a capability-change initiative may have several capability-proposals.
- [r35] **If** a capability-proposal argues more than one capability, `model check` reports it under v_k6, a capability-proposal argues more than one capability.
- [r36] A capability-proposal at `formulated` counts as closed when `model check` decides whether an initiative may be done.
- [r37] **When** `model decisions --check` finds `spec/decisions/index.md` is what `model decisions` would write, it says the file is current and exits 0.
- [r38] **When** `model decisions` is run, it prints the file it wrote, and a decision file with no `id` is left out of the index.
- [r39] **If** `model why` is given an argument that is not a requirement reference, it says why and exits 2.
- [r40] **If** no capability has the requirement `model why` names, it says so in place of the requirement's text and still lists the proposals that name it.
- [r41] **When** `model why` is run, it lists each capability-proposal that adds, changes or removes the requirement, in date order with its status and date. **If** no capability-proposal adds or changes it, including when every one that names it only removes it, `model why` exits 1; one proposal that adds or changes it is enough for exit 0.
- [r42] A reference written `capability/<context path>/<name>#behaviour/r<n>`, the requirement as a part in shopsystem-knowledge's IRI form, names the same requirement as `capability/<context path>/<name>#r<n>`.
- [r43] A node is written `<kind>/<context path>/<name>`, or in short `<kind>/<name>`, and a field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`) and the capability part of a `#r<n>` reference may write the bare `<name>`; `part_of`, `for` and `blocked_by` need `<kind>/<name>`; the context path is `<owner>/<product>/<context name>` and the bounded context is `bounded-context/<context path>`.
- [r44] A scenario tagged `@deprecated` is not read as an acceptance-scenario, whatever `@r<n>` tag it has.
- [r46] **If** a node's `id` is not `<kind>/<context path>/<name>` with its own kind, or spec/index.md's `id` is not `bounded-context/<context path>`, `model check` reports a file problem naming the file.
- [r47] **If** a reference is written `<context name>/<name>`, `decision/<name>` or `obs/<name>`, `model check` reports it as unresolved.
- [r48] A glossary entry is a bullet of `spec/index.md`'s `## Glossary` written `- **<term>**: <one-sentence definition>. Not: <word>, <word>.`, the `Not:` part optional, and `model` reads it as a term of the bounded context, with the id `term/<context path>/<term>`, the term lowercased with spaces as hyphens.
- [r49] **If** a bullet in `spec/index.md`'s `## Glossary` is not of that form, `model check` reports a file problem naming the file.
- [r50] **When** `model facts` is run, it prints for each glossary entry a `node` fact of kind `term`, a `term_of` fact naming the bounded context, and an `avoid` fact for each word after its `Not:`.
- [r51] **When** `model facts` is run, it prints a `mentions` fact for each requirement and each scenario and each term or avoided word it contains, matching a whole word, whatever its case, with a plural "s" allowed, outside code spans, double-quoted strings and `@` tags, so that "restore" is no mention of "store" and a line naming the tag `@holding` is no mention of "holding".
- [r52] **If** a requirement or a scenario mentions a word that its context's glossary lists after `Not:`, `model check` reports it under v_t1, a word the glossary avoids, naming the requirement or scenario, the word and the term.
- [r53] **If** two glossary entries have one term, `model check` reports it under v_t2, a term has two entries.
- [r54] **If** a word one term lists after `Not:` is another term of the context, or the term itself, `model check` reports it under v_t3, an avoided word is a term.
- [r55] **If** `import clingo` fails, `model check` looks for an interpreter that has clingo in this order: `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`, `/usr/local/bin/python3`, `/usr/bin/python3`, and runs again under the first that has it.
- [r56] **When** `model check` has run again under another interpreter, it does so once, and a second failure to import clingo does not run it again.
- [r57] **If** no interpreter has clingo, `model check` exits 2 with its message naming each interpreter it tried.
- [r58] A capability-proposal or a work-item may have the status `withdrawn`, and `model check` counts a withdrawn part as closed when it decides whether an initiative may be done.
- [r59] **If** an initiative is `abandoned` while a part of it, at any depth, is neither closed nor `withdrawn`, `model check` reports the initiative under v_d2, an abandoned initiative has a part open.
- [r60] **If** a capability's frontmatter has `formulated_as`, `model check` reports a file problem naming the file.
- [r61] **If** the repository has `spec/decisions.md`, or a `decisions/`, `work/` or `records/` directory at its root, `model check` reports a file problem for each, naming the path and `scripts/migrate`.
- [r62] **If** a scenario is tagged `@holding`, `model check` reports a file problem naming the file and the scenario's title.
- [r63] **If** a decision file has no `## Decision` section, `model check` reports a file problem naming the file.
- [r64] `model` reads a decision's `source` as a list of ids, each resolved as r24 says for `source` and naming a node of any kind, and does not read its `by`.
- [r65] **When** `model rules` is run, it prints each rule's code and plain label, one a line, the violations first and then the warnings, and exits 0.
- [r66] **Where** a capability-proposal's `adds`, `changes` or `removes` names `term/<term>`, `model` reads it as that glossary term, and reports it as unresolved when the glossary has no such term, except a term that a `merged` or `formulated` proposal removes.

## Implementation, may change
- `scripts/model.lp` is grammar.md v3 sections 1, 3 and 4 in clingo, with FIX notes where grammar.md does not
  compile as written; facts use grammar.md's relation names.
- Each rule's plain label is a fact `label("<code>", "<label>")` beside the rule in `model.lp`, the one place it
  is written; `check` and `rules` read the labels from the solve. A unit test fails when a relation `model.lp`
  shows has no label or two.
- Output: `<code>  <label>  (<count>)` above a violated relation's rows; `warning <code>  <label>  (<count>)`;
  `rules` prints `<code>  <label>`. `--json` adds `"labels": {code: label}` for the codes it prints.
- Node ids: the bounded-context is spec/index.md's `id`; a requirement without an id is `<capability>#line<k>`;
  a scenario is `<feature path>:<title>`.
- The frontmatter reader is a YAML subset: scalars, `[a, b]` lists and `- x` block lists.
- A decision's `source` gives no `source` fact (grammar.md's `source` is an initiative's); its ids are only
  resolved.
- `model decisions` links each row to `<file name>`, relative to `spec/decisions/index.md`.

## Not yet
- Product-level artifacts (jobs, the context-map, seams, pins) read from a product repository — trigger: a second bounded context is checked together with this one.
- A work-queue view (ready items, claims) — trigger: initiative i10 is approved.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/capabilities/feature-file-tools.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: an agent or session editing feature files
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/held-scenarios, design-decision/plugin-scenarios-run-as-pytest-bdd]
retired: []
---

# Feature file tools

## Purpose
`scripts/features` reads and edits Gherkin feature files without the test runner: it counts and lists
scenarios by tag or title, retags a scenario, moves a scenario between files and verifies the move,
deprecates and retires scenarios kept while they still pass, checks that every scenario has exactly one test
binding it and rewrites the titles test modules bind, and writes the `slice_expectations.py` pytest plugin
into a repository. It is not a Gherkin runner and does not run any test; it edits only the feature files,
test modules and directory it is pointed at.

## Behaviour
- [r1] `features` reads every `*.feature` under `--dir` (default `features`), recursively, and text inside a docstring is never taken as a scenario, keyword or tag.
- [r2] **If** a feature file contains a `Rule:` block, `features` refuses, naming the file.
- [r3] **If** an edit would leave a file that `features` cannot read, `features` refuses the edit and leaves every file as it was. `features` reads a file as invalid when it contains a `Rule:` block outside a docstring, and checks nothing else of the result.
- [r4] **When** `features count --by-tag` is run, `features` prints the number of scenarios with each tag and a total, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags. The total counts every scenario, those with no tag included.
- [r5] **When** `features list --tag <tag>` is run, `features` prints the file and title of each scenario whose tags, its feature's and its Examples' included, include that tag.
- [r6] **When** `features list --title <text>` is run, `features` prints the file and title of each scenario whose title contains the text.
- [r7] **If** `features list` matches no scenario, `features` prints nothing and exits 1.
- [r8] **When** `features tag <title> <slice>` is run on a title exactly one file has, `features` makes the scenario's first slice tag the new one, removes any further slice tags, and leaves its other tags and every other line unchanged.
- [r9] **Where** the scenario has no slice tag, **when** `features tag` is run, `features` adds the new slice tag to the scenario's last tag line, or on a tag line of its own above the scenario when it has none.
- [r10] **If** `features tag` is given a title no file has, or one several files have, `features` refuses, naming every file that has it, and changes no file.
- [r11] **If** `features tag` is given a tag not written `slice-<n>`, `slice-<n>.<m>` or `r<n>`, `features` exits 2 as bad usage and changes no file.
- [r12] **When** `features move <title> --to <file>` is run, `features` removes the scenario's block from its file and appends it unchanged to the end of the destination file.
- [r13] **Where** `--inline-background` is given, **when** `features move` is run, `features` puts the source Background's steps before the moved scenario's first step.
- [r14] **Where** `--keep-feature-tags` is given, **when** `features move` is run, `features` puts the source's feature tags that the destination's feature tags lack on a tag line of their own immediately above the moved scenario's `Scenario:` line, after any tag line the scenario already has, and joins them to none.
- [r15] **If** the destination of `features move` does not exist, `features` refuses and changes no file.
- [r16] **When** `features verify-moved --from <dir>` finds every scenario in the two trees alike by title in its effective tags, description, and Background and own steps, `features` prints how many scenarios match and exits 0.
- [r17] **If** a scenario's effective tags, description or steps differ between the two trees, `features verify-moved` names the scenario and which of them changed, and exits 1.
- [r18] **If** a title is used by more than one scenario in either tree, `features verify-moved` names the title as a duplicate and exits 1.
- [r19] **When** `features deprecate <title> --for <new title>` or `--for-removal` is run, `features` gives the scenario the tag `@deprecated`, " (deprecated)" at the end of its title and a description line `Deprecated for: <new title>` or `Deprecated for: removal`, and changes nothing else in it, whether or not the replacement exists yet.
- [r20] **If** `features deprecate` is given a scenario already tagged `@deprecated`, `features` refuses it.
- [r21] **When** `features deprecated` is run, `features` lists each deprecated scenario with what it is deprecated for and, for a replacement, the file and `@r<n>` tag of the scenario with that title, or says that no scenario has the replacement's title, or that the scenario is deprecated for removal.
- [r22] **When** `features deprecated` is run and no scenario is deprecated, `features` says none is deprecated.
- [r23] **When** `features retire <title>` is run on a scenario tagged `@deprecated`, `features` removes that scenario's block and leaves the rest of the file as it was.
- [r24] **If** `features retire` is given a scenario not tagged `@deprecated`, `features` refuses because it is not deprecated, and leaves the file as it was.
- [r25] **When** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` (default `tests`) whose title no feature file has, or not the feature it names, `features` reports the module, line, title and feature of each, and exits 1.
- [r26] **When** `features bindings` finds every binding names a scenario, `features` says so and exits 0.
- [r27] **If** a test module under `--tests` does not parse, `features bindings` and `features rebind` refuse, naming the module.
- [r28] **When** `features rebind <old> <new>` is run, `features` rewrites `<old>` to `<new>` in each binding call that names it, changes nothing else in the module, and prints how many bindings it rebound, zero included.
- [r29] **If** `features rebind` is given a new title that is no scenario in a feature file, `features` refuses and changes no test module.
- [r30] **When** `features plugin <directory>` is run, `features` writes `slice_expectations.py` into the directory and prints the line that registers it in the `conftest.py` beside it.
- [r31] **Where** `slice_expectations.py` is registered and one living plan is found, a test tagged to a slice the plan has as planned or blocked is expected to fail: its failure is reported as expected, its pass fails the run, and the run reports how many tests of which slices were expected to fail.
- [r32] **Where** `slice_expectations.py` is registered, a test tagged to a slice that is in progress, green or no longer in the plan runs as it is.
- [r33] **Where** `--slice <n>` is given to pytest, `slice_expectations.py` runs that slice's tests as they are.
- [r34] **Where** no one living plan is found, `slice_expectations.py` expects no test to fail and the run says so.
- [r35] **If** `features move`, `features deprecate` or `features retire` is given a title no file has, or, without `--file`, one several files have, `features` refuses, naming every file that has it, and changes no file.
- [r36] **If** the destination of `features move` is the scenario's own file, `features` refuses and changes no file.
- [r37] **If** a title is in the `--from` tree and not the other, or in the other tree and not `--from`, `features verify-moved` names it as missing or as added, and exits 1.
- [r38] `features list --tag` finds the tag whether it is given with its leading `@` or without.
- [r39] **When** `features deprecate` has deprecated a scenario, `features` prints its file and its new title.
- [r40] **When** `features deprecated` finds a deprecated scenario with no `Deprecated for:` line, or whose replacement has no `@r<n>` tag, `features` says so on that scenario's line.
- [r41] **If** `features rebind` is given a new title that several feature files have, `features` refuses and changes no test module.
- [r42] **If** a binding call names the old title of `features rebind` in a string written over several lines, `features` refuses, naming the module and line, and changes no test module.
- [r43] **If** `features plugin` is given a path that is not a directory, `features` refuses and writes nothing.
- [r44] **When** `features plugin` is run, `features` writes over any `slice_expectations.py` already in the directory, and reads no feature file.
- [r45] **Where** the directory given to `features plugin` has an `__init__.py`, the line `features plugin` prints imports `slice_expectations` relative to the package.
- [r46] **If** `features` refuses a command or an edit, it says why on stderr and exits 1.
- [r47] `slice_expectations.py` reads as the living plan the file the ini value `slice_plan` names under pytest's root directory, or else the one `docs/superpowers/plans/*-slices.md` under it, and finds none when there are none or several.
- [r48] **Where** `--slice` is given to pytest more than once, `slice_expectations.py` runs the tests of every slice named, each written `<n>` or `slice-<n>`, as they are.
- [r49] **Where** `slice_expectations.py` is registered, the run's header names the living plan it read, relative to the root directory, or says no one living plan was found.
- [r50] **If** the ini value `slice_plan` names a file that does not exist, `slice_expectations.py` expects no test to fail, and the run's header names that file.
- [r51] **When** `features tag <title> r<n>` is run on a title exactly one file has, `features` makes `@r<n>` the scenario's one requirement tag, removing any other `@r<m>` tag it has, and leaves its other tags and every other line unchanged.
- [r52] **Where** `--file <path>` is given, the `features` script looks for the scenario's title in that file only, whatever the command.
- [r53] **If** `--file` names a file that does not have the title, `features` refuses, naming the file, and changes no file.
- [r54] **If** `--file` names a file that has the title twice, `features` refuses, naming the file, and changes no file.
- [r55] **If** `--file` names a file outside `--dir`, `features` refuses and changes no file.
- [r56] **Where** `--file <feature path>` is given, **when** `features rebind` is run, `features` rewrites only the bindings whose feature argument names that file, the feature argument resolved against `--dir`; without `--file` it rewrites every binding of the old title.
- [r57] `features bindings` reads a `scenarios(<path>, ...)` call under `--tests` as binding every scenario of each feature file it names, and of every feature file under a directory it names.
- [r58] **Where** `--unbound` is given, **when** `features bindings` is run, it also reports the file and title of each scenario that no `scenario(...)` or `scenarios(...)` call binds, in the feature files named after `--unbound` or, with none named, every feature file under `--dir`, and exits 1 when there is one.
- [r59] **Where** `--unbound` is given, **if** a scenario is bound by more than one call, `features bindings` reports its file and title with the module and line of each call, and exits 1.

## Implementation, may change
- Gherkin is parsed line by line, not by a Gherkin library. A docstring opens and closes on `"""` or three
  backticks. A scenario's block is its tag lines, its `Scenario:` line and everything up to the next
  scenario's tag lines; `move` drops the block's trailing blank lines.
- `tag` and `deprecate` add to the last tag line; a new tag line takes the scenario's indentation. Background
  steps inlined by `move` take the scenario's step indentation; kept feature tags take the `Scenario:` line's.
- `verify-moved` compares lines stripped of indentation, blank lines and comments, and also reports titles
  missing from or added to the second tree.
- `move` also refuses a destination that is the scenario's own file.
- `deprecate` writes the description line as `Deprecated for: <title>` or `Deprecated for: removal`, indented
  like the scenario's first following line.
- `bindings` reads only a title written as a plain string in the call; a feature given as a name is looked up
  among the module's own top-level assignments. A `scenario` or `scenarios` path names a feature file by its
  base name, as it does today, or a directory by every feature file under it. `rebind` refuses a title written
  over several lines.
- Output lines: `list` prints `<path>: <title>`; `deprecated` prints
  `<path>: <title> | for: <what> | <replacement's path> @r<n>` or `none deprecated`; `bindings` prints
  `<path>:<line>: no scenario titled "<title>" in <feature>`, and with `--unbound`
  `<feature path>: <title> | bound by no test` or `<feature path>: <title> | bound by <module>:<line>, <module>:<line>`.
- `plugin` prints `from slice_expectations import *` (with a leading `.` when the directory is a package) and
  says the plugin is registered when `python -m pytest --help` lists `--slice`.
- `slice_expectations.py` finds the plan as the one `docs/superpowers/plans/*-slices.md` under pytest's root
  directory, or the ini value `slice_plan`; it marks waiting tests `xfail(strict=True)` and reads each slice's
  `- Status:` word.
- Exit status: 0 success, 1 a check failed or an edit was refused, 2 bad usage.

## Not yet
- `Rule:` blocks are refused rather than parsed — trigger: a feature file needs a `Rule:`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/capabilities/formulation.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/formulation
title: Formulation
narrator: the person who approved the lines
group: service
rests_on: [design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/held-scenarios, design-decision/controller-per-spec-round]
retired: []
---

# Formulation

## Purpose
Writes the acceptance-scenarios for approved Behaviour lines, one feature file per capability, from the
narrator's side and without sight of the code. It is `formulating-features`, run in a `initiative-round` that
dispatches `feature-formulator`s. It decides nothing: a line with two readings comes back as a question.

## Behaviour
- [r1] **When** lines are approved, each added or changed line with one reading has its scenarios in its capability's feature file `features/<name>.feature`: one scenario or one outline, or one scenario per reason for a line every call must keep (r9); every scenario that is not deprecated formulates a line.
- [r2] Formulated scenarios are committed without being shown to the person for approval.
- [r3] **If** a line admits two readings, it gets no scenario and the person is shown the question with its two readings; the rest of the capability is formulated.
- [r4] **When** a line is changed or removed and its old scenario passes today, the old scenario stays in the suite tagged `@deprecated`, with " (deprecated)" at the end of its title and a `Deprecated for:` line naming what replaces it, until the work that turns its replacement green retires it.
- [r5] **When** a line is changed or removed and its old scenario does not pass today, the old scenario is replaced or removed.
- [r6] **When** feature files are committed, `features bindings` reports that every binding names a scenario, and the commit contains only the feature files and the test files `features rebind` changed.
- [r7] **When** an existing feature file is changed, every scenario not added, changed or removed is byte for byte as it was, tags included.
- [r8] A feature file begins `# formulated from spec/capabilities/<name>.md`, then `Feature: <title>`, then `Narrator: <narrator>`.
- [r9] A line every call must keep is formulated as one scenario per reason the line gives, each with one representative call.
- [r10] **When** slicing hands back a scenario with evidence, the scenario is rewritten to fit its line and the evidence, or a question with two readings goes to the person.
- [r11] Each scenario has the tag `@r<n>` of the one line it formulates, on the scenario's tag line, and its title is free.
- [r12] A scenario tagged `@deprecated` keeps the `@r<n>` tag it had and formulates no line.
- [r13] **Where** `model check` can run, **when** feature files are committed, it reports no scenario that names no line or two, and no added or changed line without a scenario; **where** it cannot, the round says so and checks coverage by hand.
- [r14] **When** a scenario uses a word its context's glossary avoids, the scenario is reworded to its line through the small-change path, without a further gate.

## Implementation, may change
- The session dispatches `initiative-round` with the job `formulate`; the round dispatches one `feature-formulator`
  a capability with the brief in the skill, checks coverage one to one, runs each old scenario alone before
  replacing it, uses `features deprecate`, `features rebind` and `features bindings`, splices and commits.
- A scenario's title usually restates its line's condition, though the `@r<n>` tag is what names the line; Then lines name a refusal's reason, never message text.

## Not yet
None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/capabilities/spec-integration.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-integration
title: Spec integration
narrator: the person at the gate
group: service
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/spec-writers-blind-to-code, design-decision/controller-per-spec-round, design-decision/light-decisions, design-decision/references-are-ids]
retired: []
---

# Spec integration

## Purpose
Merges an approved brainstorming note, or a question's answer, into the bounded context's one spec,
and stops at the one human gate: the Behaviour lines. It is `integrating-a-proposal`, run by the session
the person talks to, with each round handed to a fresh `initiative-round` that dispatches the
`capability-writer`. It is not formulation and not planning; it writes nothing a client can run.

## Behaviour
- [r1] **When** an approved note is integrated, the session shows the person every added, changed and removed Behaviour line, each with its id, and every question the note left open, each question with the lines its answers would give.
- [r2] **Where** the change comes from a note, a drafted line that quotes no sentence of the note is shown to the person as a question, not as a line.
- [r3] **While** the person has not said yes to the lines and answered every question, nothing under `spec/` changes.
- [r4] **When** the person answers a question, the answer is drafted as a further round and the changed lines are shown again before anything is written.
- [r5] **If** the person rejects a line, that line is not written to `spec/`.
- [r6] **When** the person says yes, the approved drafts are applied to `spec/`, with the Behaviour lines exactly as approved, and committed alone, with the approval and its date in the commit message.
- [r7] **When** a note would start a second spec in a context that has one, the session integrates it into the existing `spec/` instead.
- [r8] **Where** a change adds or changes at most two Behaviour lines in existing capabilities, changes no published contract and leaves nothing unknown, the session writes the lines itself from `spec/` alone and still stops at the gate before writing them.
- [r9] **Where** the person has delegated decisions to the session's recommendations, the commit, and the decision's `by` where the change is a decision, say that the lines were approved under that delegation.
- [r10] **When** this session is the one that brainstormed the note, it says so and recommends a new session for the integration before starting it.
- [r11] **When** integration is applied, the session hands the changed capabilities to formulation.
- [r12] **When** a line is added to a capability, it takes the id one above every id the capability has used or retired, wherever the line sits in the section.
- [r13] **When** a line is changed, it keeps its id.
- [r14] **When** a line is removed, its id is added to the capability's `retired` list and no later line takes it.
- [r15] **When** the approved drafts are committed, the commit message names each id added, changed and removed.
- [r16] **Where** `model check` can run, **when** the approved drafts are applied, the only new problems it may report are: an added line with no scenario yet, a removed line's scenario that now names no line, and a scenario that uses a word the new glossary entry avoids; formulation clears all three, and any other new problem stops the commit.
- [r17] **Where** a repository keeps `.shop/work/`, a change to a glossary term rides with the capability-proposal that needs it, which lists the term in `adds`, `changes` or `removes`.
- [r18] **When** the approved drafts are committed, the commit message names each term added, changed and removed.
- [r19] **Where** a repository has no `.shop/work/`, **when** a glossary change is drafted, the session shows it to the person like a Behaviour line and writes nothing to `spec/` before the person says yes.
- [r20] **When** a change makes a decision, the person is shown it as one file `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in `spec/decisions/`, with a one-sentence summary and a Decision section, and a Context and Alternatives only where options were weighed.
- [r21] **When** a drafted decision names what it came from, its `source` lists records, initiatives or decisions by id, and the person, a date, a delegation or anything outside the repository is written in its `by`.
- [r22] **When** the approved drafts are committed with a decision, `spec/decisions/index.md` is the one `model decisions` writes, in the same commit.

## Implementation, may change
- The session dispatches `initiative-round` with the job `integrate` or `apply`, the note's path, a drafts path
  `.shop/scratch/drafts/<date>-<note>/` and the round number; the round dispatches `capability-writer`,
  which writes only under `<drafts>/round-<n>/` and replies with the change list, questions, cut sentences
  and paths, last of all to a reply file.
- The round checks `git status --porcelain` against the state before dispatch and sends back an agent that
  wrote outside its drafts path; it checks the change list in both directions.
- The writer drafts a decision as a whole file under `<drafts>/round-<n>/spec/decisions/`; applying it copies the
  file and runs `model decisions`.
- The format the writer follows is `docs/capability-format.md`.

## Not yet
- The gate approves requirement ids listed by a capability-proposal (`adds`, `changes`, `removes`) under `.shop/work/` rather than lines shown as text; until then the gate shows each line with its id — trigger: a consuming repository keeps `.shop/work/` and asks for it.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/decisions/0045-final-layout.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/final-layout
summary: "A bounded context's files are spec/ (index.md, capabilities/, decisions/ with a generated index.md), features/ beside the code, and .shop/ for its work and records, with .shop/scratch/ for what is never committed; scripts/model reads that layout and no other."
date: 2026-10-19
status: proposed
supersedes: [plugin-adopts-the-design-model]
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19"
---

# 0045. The final layout

## Decision

This repository, and every repository the plugin works in, is a bounded context of design model v3 in this
layout:

```
spec/            stands alone: what the context is
  index.md         the context: purpose, constraints, composition, testing, glossary
  capabilities/    <name>.md, one file per capability
  decisions/       <nnnn>-<slug>.md, one file per decision; index.md generated by `model decisions`
features/        <name>.feature, one per capability, with the code that runs them
.shop/           how the context is changed and what was noticed
  work/            <initiative>/initiative.md and its parts
  records/         observations.md, measurements/, review-findings/, decision-arguments/, archive/
  scratch/         drafts, notes and maps of a session; ignored by git, never read as the model
```

`scripts/model` reads only these paths; there is no fallback to an earlier layout, and an earlier layout's
paths are reported as file problems. `scripts/migrate` is the one place that knows an earlier layout. The
plugin writes nothing under `docs/superpowers/` or `.superpowers/`.

This replaces design-decision/plugin-adopts-the-design-model, whose layout put decisions, work and records at
the top level. Its other half stands, restated here: grammar.md's rules hold over these files.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/decisions/0046-light-decisions.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/light-decisions
summary: "A decision file is light: frontmatter (id, summary, date, status, supersedes, revisit_when, source, by) and a Decision section; Context and Alternatives are written only where options were weighed."
date: 2026-10-19
status: proposed
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19"
---

# 0046. Light decisions

## Decision

A decision file is `spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest number in the directory.
Its frontmatter is `id`, `summary` (one sentence), `date`, `status`, and where they apply `supersedes`,
`revisit_when`, `revisit_signal`, `source` and `by`. Its body is a `# <nnnn>. <title>` heading and a
`## Decision` section: a paragraph, a layout or a convention. `## Context` and `## Alternatives` are added
only where there was a real trade-off, two options weighed; `## Consequences` is not written. A decision that
needs neither is a summary and a Decision section, nothing else.

Existing decision files keep their sections: they are not rewritten to the light form, since the Context,
Alternatives and Consequences of an accepted decision are record.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/decisions/0047-references-are-ids.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/references-are-ids
summary: "Frontmatter names other files by id, never by path: a capability's feature file is features/<its name>.feature and formulated_as is not written; a decision's source lists ids, and where else it came from, in words, is its by."
date: 2026-10-19
status: proposed
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19"
---

# 0047. References are ids

## Decision

A frontmatter field that names another file of the bounded context names it by its id, never by a path.

- `formulated_as` is gone: a capability `<name>` is formulated in `features/<name>.feature`, always.
- A decision's `source` is a list of ids of nodes in the repository: records (an observation, a measurement, a
  review-finding, a decision-argument, an initiative-archive), an initiative, another decision. Anything else
  it came from, such as the person and a date, a delegation, a release or commit, or a document outside the
  repository, is written in words in `by`, which `scripts/model` does not read.
- A record cited by id has one: every Markdown file under `.shop/records/` but `observations.md` and a
  `README.md` has frontmatter `id`, `kind` and `about`. Archived design notes are `decision-argument`s,
  archived plans, requests and reports `initiative-archive`s, test logs and batch files `measurement`s.

The one path left in frontmatter is a work-item's `fileset`, which claims files and names nothing in the
model. Ids keep the form of design-decision/capability-ids-are-context-scoped.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/decisions/0048-plugin-scenarios-run-as-pytest-bdd.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/plugin-scenarios-run-as-pytest-bdd
summary: "In this repository a script capability's scenarios run under pytest-bdd: one scenarios() call binds its feature file, its steps are step definitions under tests/scenarios/, and features bindings --unbound fails the suite when a scenario is bound by no test or by two."
date: 2026-10-19
status: proposed
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19, rejecting design-decision/plugin-scenarios-run-as-unittest"
---

# 0048. Plugin scenarios run as pytest-bdd

## Decision

`python3 -m pytest` runs the whole suite from the repository's root (`pytest.ini`: `testpaths = tests`,
`bdd_features_base_dir = features/`). Each script capability's feature file is bound by one module,
`tests/scenarios/test_<capability with underscores>.py`, whose one binding is
`scenarios("<capability>.feature")`; its Given, When and Then steps are step definitions in that module, with
the fixtures the modules share in `tests/scenarios/conftest.py`. A scenario whose step has no definition
fails, so a scenario added to a feature file is red until it has steps.

`tests/scripts/test_bound.py` runs `features bindings --unbound` over the script capabilities' feature files
and fails when a scenario is bound by no test or by two. With the tag reading of `model check`, that keeps
the coverage it reports exact: every scenario that names a requirement is a test that runs.

Unit tests that bind no scenario stay in `tests/scripts/` as `unittest` tests, collected by pytest.
`tests/scripts/binding.py` and the docstring binding go, except for `batch-measurement`, whose scenarios keep
it until initiative i12 rewrites them.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/analysis-tools-scenarios.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools-scenarios
kind: work-item
part_of: capability-proposal/final-layout-analysis-tools
status: drafted
wkind: capability
under: analysis-tools
accepts: [analysis-tools#r1-r35]
blocked_by: [work-item/pytest-bdd-suite]
fileset: [tests/scenarios/test_analysis_tools.py, tests/scripts/test_tools.py, scripts/tools, .gitignore]
---

# analysis-tools' scenarios as pytest-bdd

Goes green: every scenario of `features/analysis-tools.feature`, bound by
`scenarios("analysis-tools.feature")` in `tests/scenarios/test_analysis_tools.py`, with r8's map in
`.shop/scratch/tools/coverage`.

- Each test in `tests/scripts/test_tools.py` whose docstring is a scenario's title is that scenario's binding
  today: move what it sets up into Given steps, what it runs into When steps and what it asserts into Then
  steps, with `parsers.parse` or `parsers.re` where steps share a shape, then delete the test. Its
  `BindingTest` goes. Tests whose docstring is no title stay as they are.
- `scripts/tools`: `MAP = os.path.join(".shop", "scratch", "tools", "coverage")`, and its help text; nothing
  else changes. `.gitignore` gains `.shop/scratch/` (this work-item or the layout move, whichever lands first).
- A scenario that fails once bound is a finding, not a fix to make here: the docstring test passed, so the
  step definitions differ from it; compare them.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/bindings-unbound.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/bindings-unbound
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: drafted
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r57-r59]
blocked_by: [work-item/feature-file-tools-scenarios]
fileset: [scripts/features, tests/scenarios/test_feature_file_tools.py]
---

# features bindings sees scenarios() and finds what nothing binds

Goes green: r57-r59's scenarios.

- `binding_calls` also collects `scenarios(<path>, ...)` calls (any number of positional string arguments,
  or names among the module's top-level assignments): each path names a feature file by base name, or a
  directory whose `*.feature` files it binds, resolved against `--dir`.
- `bindings --unbound [<feature file>...]`: after the existing report, list each scenario of the named files
  (default every file under `--dir`) that no call binds, as `<feature path>: <title> | bound by no test`, and
  each bound by more than one call with every call's `<module>:<line>`; exit 1 when any. A Scenario Outline
  is one scenario here, by title.
- Without `--unbound` the command behaves as today (r25, r26).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/decision-files-taught.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/decision-files-taught
kind: work-item
part_of: capability-proposal/final-layout-spec-integration
status: drafted
wkind: capability
under: spec-integration
check: "the T-integrate fixture case with a note that makes one decision, run 3 times with claude -p against the plugin's working copy: each run writes spec/decisions/<next n>-<slug>.md with a summary and a Decision section only, its source ids and by, spec/decisions/index.md current (model decisions --check exits 0) in the spec commit, and no file under .superpowers/ or docs/superpowers/; results in .shop/records/measurements/fixture-runs/"
blocked_by: [work-item/deprecated-and-sources]
fileset: [agents/capability-writer.md, agents/initiative-round.md, skills/integrating-a-proposal/SKILL.md, docs/capability-format.md, skills/formulating-features/SKILL.md, skills/checking-spec-consistency/SKILL.md, agents/feature-formulator.md, agents/spec-checker.md]
---

# The writers write decision files, under the final layout

spec-integration#r20-r22 have no scenarios (workflow; design-decision/workflow-scenarios-run-as-fixture-sessions),
so the check is fixture runs.

- `agents/capability-writer.md`: "The ledger" section becomes "Decisions": a new decision is a whole file
  `<drafts>/round-<n>/spec/decisions/<nnnn>-<slug>.md`, `nnnn` one above the highest in `spec/decisions/`,
  frontmatter as design-decision/light-decisions, `source` ids and `by` words; no `decisions.append.md`.
  Its description and the paths it may read (`spec/` includes `spec/decisions/`).
- `skills/integrating-a-proposal/SKILL.md` and `agents/initiative-round.md` (`apply`): copy decision drafts
  into `spec/decisions/`, run `scripts/model decisions`, commit the index with `spec/`; delegation goes in
  `by`. The spec is `spec/index.md`, `spec/decisions/`, `spec/capabilities/`.
- `docs/capability-format.md`: Layout (the tree of design-decision/final-layout); the capability file without
  `formulated_as` and "the feature file is `features/<name>.feature`"; "The decisions file" becomes "Decision
  files" in the light form, with one worked example; the sentence kinds table (`spec/decisions/`); Checking
  (reads the final layout; labels from rule-labels); requirement ids' paragraph on ledger headings goes.
- Drafts paths: `.superpowers/spec-drafts/` → `.shop/scratch/drafts/` in integrating-a-proposal,
  formulating-features, checking-spec-consistency, initiative-round, capability-writer, feature-formulator,
  spec-checker; the `.gitignore` step adds `.shop/scratch/`.
- Fixture: extend the scratch harness's T-integrate case (`/home/vscode/scratch/shopsystem-bdd/`, the shelf
  fixture) to the final layout and a note with one decision; score the checks above.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/deprecate-commands.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/deprecate-commands
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: drafted
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r19-r24, feature-file-tools#r35, feature-file-tools#r39, feature-file-tools#r40]
blocked_by: [work-item/feature-file-tools-scenarios]
fileset: [scripts/features, tests/scenarios/test_feature_file_tools.py, tests/scripts/test_features.py]
---

# features deprecate, features deprecated, retire on @deprecated

Goes green: the deprecate, deprecated and retire scenarios.

- `scripts/features`: `hold` becomes `deprecate` (same arguments: `<title> --for <new title> | --for-removal`,
  `--file`), writing `@deprecated`, " (deprecated)" and `Deprecated for: <title|removal>`; `holding` becomes
  `deprecated`, printing `<path>: <title> | for: <what> | <replacement path> @r<n>`, or the reason in that
  last field (no scenario has that title; deprecated for removal; no `Deprecated for:` line; the replacement
  has no `@r<n>` tag), and `none deprecated`; `retire` acts on `@deprecated` only. `hold` and `holding` are
  removed, not kept as aliases. The contract text in `--help` follows.
- `for: None` (observation/2026-10-16-release-0-19-0-defects) goes with it: r40 says so on the line.
- Unit tests in `test_features.py` that call `hold`/`holding` are renamed with the commands.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/deprecated-and-sources.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/deprecated-and-sources
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r26, design-model-check#r44, design-model-check#r51, design-model-check#r62, design-model-check#r63, design-model-check#r64]
blocked_by: [work-item/final-layout-read]
fileset: [scripts/model, tests/scenarios/test_design_model_check.py, spec/decisions/, .shop/records/]
---

# @deprecated read, @holding refused, decisions' sources as ids

Goes green: the scenarios of the lines listed, and `model check` on this repository still exits 0.

`scripts/model`:
- `read_features` skips a scenario tagged `@deprecated` (r44, r26's title check); a scenario tagged
  `@holding` is a file problem `<path>: scenario "<title>" is tagged @holding; the tag is @deprecated`
  (r62) and is otherwise read like any scenario.
- `mention()` and `read_mentions`: text inside backticks and double quotes, and `@<word>` tokens, are
  removed before matching (r51), in requirement text and in scenario titles and steps.
- `read_decisions`: a file with no `## Decision` heading is a file problem (r63); each `source` entry is
  qualified and wanted with kind None (r24, r64), and no `source` fact is written; `by` is not read.

This repository (a migration):
- Each Markdown file under `.shop/records/` but `observations.md` and `README.md` gets frontmatter where it
  has none: `id: <kind>/missingmass.io/shopsystem/shopsystem-bdd/<file stem>`, `kind`, `about:
  bounded-context/missingmass.io/shopsystem/shopsystem-bdd`, `date` from the name. Kinds:
  `archive/design-notes/` decision-argument; `archive/plans/` and `archive/requests/` initiative-archive;
  `measurements/fixture-runs/` measurement. Nothing else in a record changes.
- Each decision's `source` string becomes `source: [<ids>]` and `by: "<the rest>"`: a part naming a record
  by path becomes that record's id (`records/archive/design-notes/2026-10-11-green-suite-design.md` →
  `decision-argument/2026-10-11-green-suite-design`; `records/measurements/fixture-runs/2026-10-12-spec-round-test-log.md`
  → `measurement/2026-10-12-spec-round-test-log`; `work/i3-requirement-ids/initiative.md` → `initiative/i3`;
  `design-decision/<x>` and `observation/<x>` stay as ids); every other part (the person and a date, a
  release, a commit, README sections, `docs/design-model/…`, other repositories' decisions) goes to `by`,
  parts joined with "; ". Thirty-six files; `model check` must report no unresolved source.
- `spec/decisions/index.md` regenerated.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/design-model-check-scenarios-1.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-scenarios-1
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r1, design-model-check#r9, design-model-check#r12, design-model-check#r13, design-model-check#r16-r18, design-model-check#r21-r25, design-model-check#r27-r32]
blocked_by: [work-item/pytest-bdd-suite]
fileset: [tests/scenarios/test_design_model_check.py, tests/scripts/test_model.py]
---

# design-model-check's scenarios as pytest-bdd, first half

Goes green: the scenarios of the lines listed, bound by `scenarios("design-model-check.feature")` in
`tests/scenarios/test_design_model_check.py`; the module's other scenarios stay red until
design-model-check-scenarios-2, final-layout-read, rule-labels and deprecated-and-sources bind them.

- Each docstring test of `tests/scripts/test_model.py` binding one of these scenarios becomes step definitions
  and is deleted. The `ModelTest` helpers that build a repository (index, capability, feature, decision, work
  files) become fixtures or plain functions in `tests/scenarios/conftest.py`, so the later work-items reuse
  them; write them for the final layout's paths from the start where a step names no path
  (`spec/decisions/`, `.shop/work/`, `.shop/records/`), and leave the current paths where a scenario names
  them (final-layout-read changes those).
- `BindingTest` stays in `test_model.py` until design-model-check-scenarios-2 removes it.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/design-model-check-scenarios-2.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/design-model-check-scenarios-2
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r36, design-model-check#r38-r43, design-model-check#r46-r50, design-model-check#r55-r58]
blocked_by: [work-item/design-model-check-scenarios-1]
fileset: [tests/scenarios/test_design_model_check.py, tests/scripts/test_model.py]
---

# design-model-check's scenarios as pytest-bdd, second half

Goes green: the scenarios of the lines listed, in the module design-model-check-scenarios-1 made. `BindingTest` and the `binding` import leave `test_model.py`; the unit tests that
bind no scenario stay.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/every-scenario-bound.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/every-scenario-bound
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: drafted
wkind: enabling
for: work-item/bindings-unbound
check: "python3 -m pytest passes and includes tests/scripts/test_bound.py; python3 scripts/features bindings --unbound features/analysis-tools.feature features/design-model-check.feature features/feature-file-tools.feature exits 0; no tests/scripts module but test_measure.py imports binding"
blocked_by: [work-item/analysis-tools-scenarios, work-item/deprecate-commands, work-item/bindings-unbound, work-item/final-layout-read, work-item/rule-labels, work-item/deprecated-and-sources]
fileset: [tests/scripts/test_bound.py, tests/scripts/binding.py]
---

# The suite fails when a scenario has no test or two

- `tests/scripts/test_bound.py`, a unittest test: runs `scripts/features --dir features bindings --tests tests
  --unbound` over the feature files of the script capabilities bound by pytest-bdd (analysis-tools,
  design-model-check, feature-file-tools, and migration-tools once i8 adds it) and asserts exit 0, printing
  the report on failure.
- `tests/scripts/binding.py` stays, used only by `test_measure.py`, with a docstring saying i12 removes it.
- `spec/index.md`'s Testing says the same (the text is in `spec-index.md`).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/feature-file-tools-scenarios.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools-scenarios
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: drafted
wkind: capability
under: feature-file-tools
accepts: [feature-file-tools#r1-r18, feature-file-tools#r25-r34, feature-file-tools#r36-r38, feature-file-tools#r41-r56]
blocked_by: [work-item/pytest-bdd-suite]
fileset: [tests/scenarios/test_feature_file_tools.py, tests/scripts/test_features.py]
---

# feature-file-tools' unchanged scenarios as pytest-bdd

Goes green: the scenarios of `features/feature-file-tools.feature` for every line whose behaviour this
proposal does not change, bound by `scenarios("feature-file-tools.feature")` in
`tests/scenarios/test_feature_file_tools.py`. The deprecate scenarios (r19-r24, r35, r39, r40) and the
bindings ones (r57-r59) are formulated already and stay red here: they are work-item/deprecate-commands and
work-item/bindings-unbound. Mark nothing xfail; the work-item is done when only those are red.

- As for analysis-tools: each docstring test in `tests/scripts/test_features.py` that binds a scenario becomes
  step definitions and is deleted; `BindingTest` goes; other unit tests stay.
- The lines i10 retires (slice tags, `slice_expectations.py`) are not converted if i10 has removed them by
  the time this starts; convert whatever the feature file has.
- No change to `scripts/features` here.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/final-layout-read.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/final-layout-read
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r14, design-model-check#r15, design-model-check#r19, design-model-check#r20, design-model-check#r37, design-model-check#r60, design-model-check#r61]
blocked_by: [work-item/design-model-check-scenarios-2]
fileset: [scripts/model, tests/scenarios/test_design_model_check.py, tests/scripts/test_model.py, spec/, features/, .shop/, decisions/, work/, records/, docs/superpowers/, README.md, docs/design-model/design-model.md, .gitignore]
---

# model reads the final layout, and this repository moves to it

Goes green: the scenarios of the lines listed; r45's scenario is removed with the line (it is retired), and
`model check` on this repository exits 0 after the move. One work-item, because the reader and the files must
change in one commit for this repository's own check to stay clean.

`scripts/model`:
- `read_decisions` reads `spec/decisions/*.md` but `index.md`; the ledger branch goes (r45).
- `read_work` reads `.shop/work/`, `read_records` `.shop/records/`.
- `read_capabilities` takes the feature file as `features/<name>.feature` always; a `formulated_as` key is a
  file problem (r60). `read_features` matches files to capabilities by that name (r20, r26's first half).
- r61: a file problem for each of `spec/decisions.md`, `decisions/`, `work/`, `records/` that exists under the
  root: `<path>: the layout has no <path>; run scripts/migrate`.
- `render_decisions` and `cmd_decisions` write `spec/decisions/index.md`, rows linked `[<id>](<file name>)`,
  the header line saying it is generated by `scripts/model decisions` from `spec/decisions/` and never
  edited by hand.
- The contract in `--help` (the `CONTRACT` text) states the final paths and nothing of the ledger.

This repository (a migration; `git mv` so history follows):
- `decisions/*.md` → `spec/decisions/`; `spec/decisions.md` removed and `spec/decisions/index.md` written
  by `model decisions`.
- `work/` → `.shop/work/`; `records/` → `.shop/records/`; `docs/superpowers/plans/*` →
  `.shop/records/archive/plans/`; `docs/superpowers/specs/*` → `.shop/records/archive/design-notes/`;
  `docs/superpowers/` removed.
- `formulated_as` removed from every `spec/capabilities/*.md` (each names `features/<name>.feature` today).
- `.gitignore`: `.superpowers/` becomes `.shop/scratch/`.
- Path mentions in `README.md`, `spec/index.md` (as `spec-index.md` proposes), `.shop/work/README.md`,
  `.shop/records/README.md` (its table re-pathed) and initiative bodies follow. Decisions' `source` strings
  are left to deprecated-and-sources.
- `docs/design-model/design-model.md` section 8: a dated note under the tree, "In the plugin's repositories
  (2026-10-19, design-decision/final-layout): decisions under `spec/decisions/`, work and records under
  `.shop/`." The model's text is otherwise unchanged.
- Tests that build repositories in the old layout (in `tests/scripts/test_model.py` and the step modules)
  build the final one; the scenarios that name paths were reworded at formulation.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/formulation-deprecates.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/formulation-deprecates
kind: work-item
part_of: capability-proposal/final-layout-formulation
status: drafted
wkind: capability
under: formulation
check: "a T-formulate fixture case where one line is changed and its old scenario passes, run 3 times with claude -p: each run deprecates the old scenario with features deprecate (tag @deprecated, ' (deprecated)' title, Deprecated for: the new title), rebinds its test, writes the new scenario tagged with the line's id, and model check reports no v_s1, v_s2 or v_t1; results in .shop/records/measurements/fixture-runs/"
blocked_by: [work-item/deprecate-commands, work-item/rename-sweep]
fileset: [skills/formulating-features/SKILL.md, agents/feature-formulator.md, agents/initiative-round.md]
---

# Formulation deprecates

formulation#r1, r4, r6, r11, r12 are workflow lines with no scenarios, so the check is fixture runs.
`skills/formulating-features/SKILL.md` and the agents it dispatches say deprecate, `features deprecate`,
`features deprecated`, " (deprecated)" and `Deprecated for:` (the rename-sweep did the words; this
work-item runs the skill to show the behaviour). Build the fixture from the shelf generator in
`/home/vscode/scratch/shopsystem-bdd/make_shelf.py`, final layout.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/proposal-lists-read.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/proposal-lists-read
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r23, design-model-check#r66]
blocked_by: [work-item/design-model-check-scenarios-2]
fileset: [scripts/model, tests/scenarios/test_design_model_check.py]
---

# Terms in a proposal's lists, and a merged removal resolved

Goes green: r23's and r66's scenarios, and `model check` on this repository reports no unresolved entry for
final-layout-design-model-check's `removes: [design-model-check#r45]` or final-layout-feature-file-tools's
`term/` entries once they are merged.

- `read_part`, for a capability-proposal: an entry of `adds`, `changes` or `removes` written `term/<term>`
  (or in full) is qualified and resolved against the glossary's term nodes, not passed to `resolve_req`;
  one the glossary lacks is unresolved, unless the list is `removes` and the proposal's status is `merged`
  or `formulated`. No fact is written for it (grammar.md has no relation for a proposal and a term).
- A `removes` entry naming an id its capability lists as retired, in a `merged` or `formulated` proposal,
  writes the `removes` fact and is not unresolved; in any other status it is unresolved as today.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/pytest-bdd-suite.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/pytest-bdd-suite
kind: work-item
part_of: capability-proposal/final-layout-analysis-tools
status: drafted
wkind: enabling
for: work-item/analysis-tools-scenarios
check: "python3 -m pytest -q from the root passes and collects every test python3 -m unittest discover -s tests/scripts runs, the same count; python3 -m pytest --collect-only -q tests/scenarios exits 0"
fileset: [pytest.ini, tests/scenarios/__init__.py, tests/scenarios/conftest.py, README.md, spec/index.md]
---

# The suite under pytest, with a home for step definitions

Goes green: nothing new; the suite runs under `python3 -m pytest` from the root, the unit tests unchanged.

- `pytest.ini` at the root: `[pytest]`, `testpaths = tests`, `bdd_features_base_dir = features/`; pytest's
  defaults otherwise.
- `tests/scenarios/` (a package) with `conftest.py`: the fixtures every step module shares, lifted from the
  helpers the unittest classes already have (`ModelTest`'s temporary repository and its writers in
  `tests/scripts/test_model.py`, `Workspace` in `test_features.py`, the project builders in `test_tools.py`):
  a fixture giving a fresh temporary directory as the root, a `run` fixture that runs a script
  (`scripts/model`, `scripts/features`, `scripts/tools`) with `sys.executable` and returns the completed
  process, and a `context` fixture (a dict) that steps use to pass the result from When to Then.
- The unit tests in `tests/scripts/` keep importing `binding` as they do (pytest's default import mode puts
  their directory on `sys.path`); check that pytest collects the same number of tests unittest runs.
- README's Testing and `spec/index.md`'s Testing say `python3 -m pytest` (the text is in the proposal's
  `spec-index.md`).

Dependencies: pytest and pytest-bdd, already named by design-decision/plugin-takes-the-dependencies-it-needs.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/rename-sweep.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/rename-sweep
kind: work-item
part_of: capability-proposal/final-layout-feature-file-tools
status: drafted
wkind: enabling
for: work-item/deprecate-commands
check: "grep -rniwE 'hold|holds|holding|held|superseded|carry|carries|carried|carrying' over skills/ agents/ docs/capability-format.md README.md scripts/model scripts/model.lp scripts/features scripts/tools spec/ features/ tests/scenarios/ prints only the exceptions this work-item lists; python3 scripts/model check exits 0 with no v_t1 row; python3 -m pytest passes"
blocked_by: [work-item/deprecate-commands, work-item/deprecated-and-sources, work-item/rule-labels]
---

# "Deprecated" and plain words everywhere that survives

Goes green: the check. Runs after initiative i10's work-items are merged, so it meets only what survives
them, and after this initiative's proposals are merged, so the glossary's new entry is in `spec/index.md`.

- Deprecated (the scenario sense): `@holding` → `@deprecated`, `features hold`/`holding` → `features
  deprecate`/`deprecated`, " (held)" → " (deprecated)", `Held for:` → `Deprecated for:`, "held scenario" →
  "deprecated scenario", "superseded" (of a scenario) → "deprecated": in skills/ (formulating-features,
  migrating-to-capabilities only where i8 has not rewritten it, checking-spec-consistency,
  integrating-a-proposal), agents/ (feature-formulator, initiative-round, capability-writer, and any
  delivery agent i10 left), `docs/capability-format.md`, README, the scripts' help and comments, test names.
- Decisions' text, ids kept: design-decision/held-scenarios and
  design-decision/held-scenario-formulates-no-requirement are reworded to `@deprecated`, `features
  deprecate`, `features deprecated` (summary and body; the summary's "the slice that turns its replacement
  green" becomes "the work that turns its replacement green"), and `spec/decisions/index.md` regenerated.
  Other decisions' text where "hold"/"carry" appears in another sense, likewise, ids kept.
- Plain words: "hold(s)" → stays valid, has, contains, keeps, is enforced by; "carry/carries/carried" →
  has, keeps, does, names. Not in a decision's id or file name, a record, `docs/design-model/`, or LICENSE.
- Exceptions the check allows: decision ids and file names (held-scenarios, held-scenario-formulates-no-requirement,
  rules-held-by-agent-tools, suite-record-holds, plans-carry-intent-not-code) wherever they are cited;
  `scripts/measure`, `tests/scripts/test_measure.py`, `skills/analyzing-a-batch/` and batch-measurement's
  lines other than r10 and r16 (i12); `spec/index.md`'s glossary entry's `Not:` list.
- batch-measurement's four reworded steps (capability-proposal/final-layout-batch-measurement) need nothing
  in `test_measure.py`: it binds by title.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i11/work-items/rule-labels.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/rule-labels
kind: work-item
part_of: capability-proposal/final-layout-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r2-r8, design-model-check#r10, design-model-check#r11, design-model-check#r33-r35, design-model-check#r52-r54, design-model-check#r59, design-model-check#r65]
blocked_by: [work-item/design-model-check-scenarios-2]
fileset: [scripts/model.lp, scripts/model, tests/scenarios/test_design_model_check.py, tests/scripts/test_model.py, docs/capability-format.md, skills/]
---

# A plain label for every rule

Goes green: the scenarios of the lines listed: each violated or warning relation printed with its label,
`--json`'s `labels`, `model rules`.

- `scripts/model.lp`: one fact `label("<code>", "<label>").` beside each rule, with the labels of the table in
  capability-proposal/final-layout-design-model-check exactly, and `#show label/2.`
- `scripts/model`: `solve` returns the labels apart from the relations; `check` prints `<code>  <label>  (<n>)`
  and `warning <code>  <label>  (<n>)`; `--json` adds `"labels"` for the codes in its output; `rules` prints
  every label, violations then warnings, in `model.lp`'s order, and needs clingo as `check` does (its
  missing-clingo path is the same).
- A unit test: every relation in `model.lp`'s `#show` lines has exactly one label, and no label names a
  relation that is not shown.
- Text that names a rule names its label too, "v_s3 (a requirement has no scenario)": the table in
  `docs/capability-format.md`'s Checking and Glossary sections, and the skills that name rules
  (migrating-to-capabilities, checking-spec-consistency, formulating-features, integrating-a-proposal), and
  `agents/initiative-round.md`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/initiative.md`

~~~~~~
---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i8
title: Migrate a consuming repository to design model v3
summary: Migration tools only, that take a consuming repository from the old system to the final layout of design model v3; the plugin keeps nothing of the old system beyond them.
kind: capability-change
owner-level: shopsystem-bdd
status: proposed
priority: 3
source: [review-finding/2026-10-13-kb-and-bdd-assessment]
date: 2026-10-15
---

Rewritten 2026-10-19 to the person's direction: there is no intermediate state in a consuming repository,
only the final one (the layout of initiative/i11) and the tools that move a repository there. shopsystem-kb
and shopsystem-knowledge move after the plugin itself is on the model.

Covers:
- adding ids to a repository already on capability files (shipped in 0.19.0, spec-migration);
- the decision ledger in `spec/decisions.md` to one decision file each, with a generated index;
- living slice plans to work-items;
- `@holding` scenarios to `@deprecated` (the person, 2026-10-19: deprecated in place of superseded);
- the repository layout: `spec/decisions/`, `.shop/work`, `.shop/records`;
- the glossary in its form.

## The final state

The layout and conventions are i11's (design-decision/final-layout, design-decision/light-decisions,
design-decision/references-are-ids); this initiative only moves a repository to them, in one pass with one
gate (design-decision/migration-in-one-pass).

**`scripts/migrate`** (capability/migration-tools) is the only code in the plugin that knows the old layout.
`migrate status` says what is left of it. `migrate run` makes every change that is transcription, in four
steps computed before any is written: ids (the numbering and id rewrites Adding Ids did by hand in 0.19.0),
layout (the moves, ids for the records among them, moved paths rewritten in tracked text files, `.gitignore`),
decisions (the ledger split into `spec/decisions/<nnnn>-<name>.md`, `source` to ids and `by`, the index), and
deprecated (`@holding` to `@deprecated`, `Held for:` to `Deprecated for:`, bindings rebound). `migrate plan`,
run once scenarios are tagged, turns the living plan's open slices into work-items under
`initiative/migrated-plan` and its backlog and open log entries into observations
(design-decision/living-plan-to-work-items). It refuses rather than guesses: a `formulated_as` naming
another file, a ledger property it does not know, a slice in progress, a scenario a slice names that has no
`@r<n>` tag.

**`migrating-to-capabilities`** has one process for a repository that has a `spec/` (the old Adding Ids
section folds into it) and keeps its first-spec process for one that has none, which ends by running the
same steps for what is left. In order: preconditions and the baseline under `.shop/scratch/migration/`; the
context path, asked of the person if `spec/index.md` lacks it; `migrate run`, verified (suite equal,
`verify-moved`, word-diff of Behaviour lines showing only ids) and committed alone as the mechanical move;
the scenario mapping by `feature-formulator`; one gate, showing the mapping's questions, glossary bullets
out of form, each open slice (keep or drop) and each entry that would become an observation (keep or leave
out); `features tag`, the glossary rewritten in the person's words, `migrate plan --drop … --leave …`; verify
(`migrate status` 0, `model check` clean but the `v_s3` of lines that had no scenario, the suite equal) and
commit. `capability-writer`'s migration brief writes decision files, not a ledger.

**What the plugin keeps of the old system**: `scripts/migrate` and the migration skill's text. Nothing else
reads a ledger, a slice plan, `@holding` or a top-level `work/`.

## How it is shown working

- Script: migration-tools' scenarios, as pytest-bdd step definitions (design-decision/plugin-scenarios-run-as-pytest-bdd),
  each against a small repository built in a temporary directory.
- Workflow: a fixture case, T-migrate-final, in the scratch harness (`/home/vscode/scratch/shopsystem-bdd/`):
  an old-layout shelf repository (capabilities without ids, `spec/index.md` without an id, a ledger with
  `decision/` headings and sources naming `docs/superpowers/specs/` and `adrs/`, an `@holding` scenario bound
  by title, a living plan with a planned capability slice, an enabling slice before it, a blocked slice and a
  green one, backlog and log entries, an archive, a glossary bullet out of form, pytest-bdd steps). The skill
  runs headless (`claude -p --plugin-dir` the working copy) three times, the gate answered by the harness;
  each run is scored on: `migrate status` exit 0, `model check` exit 0, the suite's summary and passing titles
  equal to the baseline's, `verify-moved` clean before tagging, the two commits, the work-items and
  observations expected, nothing under `docs/superpowers/`. Three of three, recorded in
  `.shop/records/measurements/fixture-runs/`.
- Trial: a fresh clone of shopsystem-kb (https://github.com/dstengle/shopsystem-kb) at its current head,
  outside any repository the plugin owns, with the gate answered by the controller from the session's
  recommendations, as the 2026-10-16 trials were. Scored like the fixture, except `model check` may report
  `v_s3` for kb's ten lines that have no scenario today; the suite equal at 1603 passed. Nothing is pushed:
  kb moves for real only when its own session runs the migration with the person at the gate.

## What is removed

The 0.19.0 "Adding Ids" section as a hand procedure (its numbering is `migrate run`); the ledger in the
first-spec process (`decisions.append.md`); the migration's `.superpowers/spec-drafts/` path (now
`.shop/scratch/drafts/`); slice-plan editing in the migration ("rewrite the feature half of `Scenarios:`
lines" goes: the plan becomes work-items).

## Parts

model-in-consumers-migration-tools (a new capability), model-in-consumers-spec-migration. Decisions 0049,
0050.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/model-in-consumers-migration-tools.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/model-in-consumers-migration-tools
kind: capability-proposal
part_of: initiative/i8
status: drafted
date: 2026-10-19
argues: [migration-tools]
adds: [migration-tools#r1-r45]
---

# Migration tools: scripts/migrate

A new script capability (group service), `capabilities/migration-tools.md`, fully described by its lines as
the plugin's scripts are. Three commands:

- `migrate status` (r2, r3): what is left of the old system, exit 0 when nothing is.
- `migrate run [--context <id>] [--dry-run] [--tests <dir>]` (r4-r29), four steps in order, all computed
  before any is written: **ids** (r11-r16: the Adding Ids numbering and id rewrites of 0.19.0, now a script),
  **layout** (r17-r21: the moves, record ids, moved paths rewritten in tracked text files, `.gitignore`), **decisions**
  (r22-r26: the ledger to decision files, `source` to ids and `by`, the index), **deprecated** (r27-r29:
  `@holding` to `@deprecated`, bindings rebound).
- `migrate plan [--plan <file>] [--drop <n,...>] [--leave <name,...>] [--dry-run]` (r30-r44): run after the
  scenarios are tagged; the living plan to work-items under `initiative/migrated-plan`, and its backlog and
  open log entries to observations.

Shared: r1, r7-r10 (dry run, printed changes, refusal before any write, nothing to do on the final layout),
r45 (exit statuses).

Shown on kb (records/measurements/fixture-runs, 2026-10-16 and 2026-10-17 trials, and a clone at `2eed357`):
21 capabilities with 371 lines and no ids, `spec/index.md` with no frontmatter, a ledger of 154
`## decision/...` entries (20 named `0001-` to `0020-` in ledger order, the rest unnumbered), 154 `source`
lines naming `docs/superpowers/specs/*.md`, `adrs/*.md` or words ("the person's delegation of 2026-10-10"),
31 ADRs and a README under `adrs/`, a living plan `docs/superpowers/plans/2026-09-24-kb-slices.md` with one enabling
slice (180.1, `blocked: done as slice 165.4`), 160 backlog entries and 45 log entries, 43 of them
`QUESTION FOR THE SPEC:`, `REQUEST` or `RE-FORMULATE`, 15 archived plans, 40-odd batch plans, 9 design notes and one request. No
`@holding` scenario, no glossary, no `work/` or `records/`. Each of those has a line here.

kb's `tests/slices.py` names the living plan by its path (`PLAN = "docs/superpowers/plans/2026-09-24-kb-slices.md"`)
and stops the run when it cannot read it; r20 rewrites that path so kb's suite gives the same answer after the
move. Removing kb's own slice machinery is kb's work, after its migration.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/model-in-consumers-spec-migration.md`

~~~~~~
---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/model-in-consumers-spec-migration
kind: capability-proposal
part_of: initiative/i8
status: drafted
date: 2026-10-19
argues: [spec-migration]
adds: [spec-migration#r15-r23]
changes: [spec-migration#r4, spec-migration#r9, spec-migration#r11, spec-migration#r13, spec-migration#r14]
---

# Spec migration: to the final layout, in one pass

Migration ends on the final layout whatever the repository had of the old system
(design-decision/migration-in-one-pass), with one gate. The proposed file is `capabilities/spec-migration.md`.

- What the person sees: r16 (the gate adds glossary bullets out of form, the plan's open slices, the entries
  that would become observations), r23 (each file other than Markdown in which a moved path was rewritten: on kb, `tests/slices.py` reads the living plan by path, and its suite stops when the plan is not where it says).
- What it ends with: r15 (the layout; `migrate status` clean), r17 (work-items and observations,
  design-decision/living-plan-to-work-items), r18 (`@deprecated`, still bound), r19 (decision files, sources
  as ids), r20 (`model check` clean but the lines that had no scenario), r21 (the glossary in form), r22
  (the mechanical move in a commit of its own, reviewable before the gate).
- Changed: r11 and r13 say deprecated for held, and set aside r18's renaming; r14 names `spec/decisions/`
  and `.shop/` where it named "outside spec/" and drops ledger headings, which no longer survive a
  migration; r4 and r9 are plain words (holding → with, carry → have).

The mechanical half is a new script capability, capability/migration-tools
(capability-proposal/model-in-consumers-migration-tools); these lines are the person's view of it.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/capabilities/migration-tools.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/migration-tools
title: Migration tools
narrator: a person or session migrating a repository to the final layout
group: service
rests_on: [design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout, design-decision/references-are-ids, design-decision/capability-ids-are-context-scoped, design-decision/plugin-takes-the-dependencies-it-needs]
retired: []
---

# Migration tools

## Purpose
`scripts/migrate` makes every mechanical change that takes a repository from the old system to the final
layout (design-decision/final-layout): requirement and node ids, the moves of the old directories with ids
for the records among them, the decision ledger split into decision files, `@holding` renamed to
`@deprecated`, and a living slice plan turned into work-items and observations. It is the only code in the
plugin that knows the old layout. It decides nothing that needs judgment: it refuses, naming what it cannot
place, and leaves the mapping of scenarios to lines, the context path and the gate to the session.

## Behaviour
- [r1] `migrate` reads and changes files only under `--root`, default the current directory.
- [r2] **When** `migrate status` is run, it prints each thing of the old system the repository has, one a line: `spec/decisions.md`; a `decisions/`, `work/` or `records/` directory at the root; each file under `docs/superpowers/`; a living plan `*-slices.md`; each scenario tagged `@holding`; each capability with `formulated_as`, with an `id` not `capability/<context path>/<file name>`, or without `retired`; each capability with a Behaviour line that has no `[r<n>]`; and `spec/index.md` with no `id`; and it exits 1.
- [r3] **When** `migrate status` finds none of those, it says the repository is on the final layout and exits 0.
- [r4] **If** the root is not a git working tree, `migrate run` and `migrate plan` refuse.
- [r5] **If** `spec/index.md` has no `id` and `migrate run` is given no `--context`, it refuses, saying the context's id is needed, and changes no file.
- [r6] **If** `--context` is not `bounded-context/<owner>/<product>/<context name>`, or is not the `id` `spec/index.md` already has, `migrate run` refuses and changes no file.
- [r7] **Where** `--dry-run` is given, `migrate run` and `migrate plan` print every change they would make and change no file.
- [r8] **When** `migrate run` or `migrate plan` changes files, it prints each change, one a line, under the name of its step, and the number of changes of each step.
- [r9] **If** any change of `migrate run` or `migrate plan` cannot be made, it refuses before changing any file, naming each change it could not make.
- [r10] **When** `migrate run` is run on a repository on the final layout, it changes no file and says there is nothing to migrate.
- [r11] **When** `migrate run` is run, `spec/index.md`'s frontmatter has the context's `id`, written when it had none.
- [r12] **When** `migrate run` is run, each Behaviour bullet with no `[r<n>]` gets one, numbered from one above the highest id its capability has used or retired, in the order the bullets come, and its text is unchanged.
- [r13] **When** `migrate run` is run, each capability with no `retired` gets `retired: []`, and each capability's `id` is `capability/<context path>/<file name>`.
- [r14] **When** `migrate run` is run, each `decision/<name>` reference in frontmatter and each `## decision/<name>` heading becomes `design-decision/<name>`, each `obs/<x>` reference becomes `observation/<x>`, each `## obs/<x>` heading becomes `## observation/<context path>/<x>`, each frontmatter `id` under `spec/decisions/` and `.shop/` is written `<kind>/<context path>/<name>`, and nothing else in a reference changes.
- [r15] **When** `migrate run` is run, `formulated_as` is removed from each capability whose `formulated_as` is `features/<its file name>.feature`.
- [r16] **If** a capability's `formulated_as` names any other file, `migrate run` refuses, naming the capability and the file.
- [r17] **When** `migrate run` is run, it moves with git: `decisions/*.md` to `spec/decisions/`; `work/` to `.shop/work/`; `records/` to `.shop/records/`; `docs/superpowers/specs/` to `.shop/records/archive/design-notes/`; `docs/superpowers/plans/`, with its `archive/`, to `.shop/records/archive/plans/`; `docs/superpowers/requests/` to `.shop/records/archive/requests/`; `docs/superpowers/measurements/` to `.shop/records/measurements/`; `docs/superpowers/reports/` to `.shop/records/archive/reports/`; any other file under `docs/superpowers/` to `.shop/records/archive/` under its path below `docs/superpowers/`; and each other directory a ledger entry's `source` names a file in, such as `adrs/`, to `.shop/records/decision-arguments/`.
- [r18] **If** a file would be moved onto a file that exists, `migrate run` refuses, naming both.
- [r19] **When** `migrate run` is run, each Markdown file under `.shop/records/` but `observations.md` and `README.md` that has no frontmatter `id` gets `id`, `kind`, `about` and `date`: the id `<kind>/<context path>/<its file name without .md>`, lowercased with each run of other characters than letters, digits and hyphens as one hyphen; the kind by its directory (`decision-arguments/` and `archive/design-notes/` decision-argument, `measurements/` measurement, `review-findings/` review-finding, any other under `archive/` initiative-archive); `about` the bounded context; the date its name begins with, or else the date of the commit that added it. Any frontmatter it had is kept.
- [r20] **When** `migrate run` has moved files, each moved path, written in full from the root, is rewritten to its new path in every tracked text file outside `.shop/records/`, and each file other than Markdown it so changed is listed with the line.
- [r21] **When** `migrate run` is run, a `.superpowers/` line of `.gitignore` becomes `.shop/scratch/`, and `.shop/scratch/` is added to `.gitignore` when it has neither.
- [r22] **When** `migrate run` is run, each entry of `spec/decisions.md` becomes the file `spec/decisions/<nnnn>-<name>.md`, `nnnn` its position in the ledger written in four digits, or `<name>.md` when the name already begins with those four digits and a hyphen, and `spec/decisions.md` is removed.
- [r23] A decision file made from a ledger entry has the frontmatter `id` `design-decision/<context path>/<name>`, `summary` the entry's text up to its first blank line or property line with its lines joined by a space, `date`, `status: accepted`, and the entry's `supersedes` and `revisit_when` where it has them; its body is `# <nnnn>. <name with hyphens as spaces>` and a `## Decision` section of the entry's text.
- [r24] **If** a ledger entry has a property line other than `date:`, `revisit_when:`, `supersedes:` or `source:`, or has no `date:`, `migrate run` refuses, naming the entry.
- [r25] **When** `migrate run` writes a decision's `source`, from a ledger entry or a decision file's own `source`, each part of it, split at `;`, that begins with the path of a file the run moved, old or new, becomes that file's record id; each part that is an id of a node kind stays as it is; and the rest of each part, and every other part, is written in `by`, joined with "; ".
- [r26] **When** `migrate run` has written the decision files, `spec/decisions/index.md` is what `model decisions` writes.
- [r27] **When** `migrate run` is run, each scenario tagged `@holding` is tagged `@deprecated`, " (held)" at the end of its title becomes " (deprecated)", its `Held for:` line becomes `Deprecated for:`, and nothing else in it changes.
- [r28] **When** `migrate run` retitles a scenario, each `scenario(<feature>, "<old title>")` binding call under `--tests`, default `tests`, that names it is rewritten to the new title, and nothing else in the module changes.
- [r29] **If** a test module under `--tests` does not parse, or names an old title in a string written over several lines, `migrate run` refuses, naming the module.
- [r30] `migrate plan` reads as the living plan the one `*-slices.md` directly in `.shop/records/archive/plans/`, or the file `--plan` names.
- [r31] **If** there is no living plan or there are several, `migrate plan` refuses, naming those it found.
- [r32] **If** a slice of the plan is `in progress`, `migrate plan` refuses, naming it.
- [r33] **When** `migrate plan` is run, each slice whose status is not green and that `--drop` does not name becomes a `planned` work-item `.shop/work/migrated-plan/slice-<n>.md`, `n` the slice's number with its dots as hyphens, with the id `work-item/<context path>/slice-<n>`, `wkind` capability for a capability slice and enabling for an enabling or stack slice, and as its body the slice's heading, its `Observable:`, `Unknown:`, `Needs:`, `Lands:` and `Status:` lines, and its place in the plan.
- [r34] **When** `migrate plan` writes a capability slice's work-item, it is `under` the capability of its first `Scenarios:` entry's feature, `part_of` `capability-proposal/<context path>/migrated-<that capability>`, and `accepts` `<capability>#r<n>` for each `<feature> / <title>` entry, `@r<n>` being the requirement tag of the scenario of that title in `features/<feature>.feature`.
- [r35] **If** a `Scenarios:` entry names a title no scenario of its feature file has, or a scenario with no `@r<n>` tag, `migrate plan` refuses, naming the slice and the entry.
- [r36] **When** `migrate plan` writes an enabling or stack slice's work-item, its `check` is the slice's `Check:` text, it is `for` the work-item of the first capability slice after it in the plan that becomes a work-item, and it is `part_of` that work-item's capability-proposal.
- [r37] **Where** no capability slice after an enabling or stack slice becomes a work-item, `migrate plan` writes that slice as an observation in place of a work-item.
- [r38] **When** `migrate plan` is run, each entry of the plan's Backlog, and each Log entry that begins `QUESTION FOR THE SPEC:`, `REQUEST` or `RE-FORMULATE` with its continuation lines, that `--leave` does not name, is appended to `.shop/records/observations.md` as `## observation/<context path>/<date>-backlog-<k>` or `<date>-log-<k>`, `k` counting that section's entries of that date from 1, with `about:` the bounded context, `by:` the plan's backlog or log, `date:`, and the entry's text as it was.
- [r39] **When** `migrate plan` writes any work-item, it also writes `.shop/work/migrated-plan/initiative.md`, the initiative `initiative/<context path>/migrated-plan`, kind capability-change, status started, priority 1, dated today, its source an observation `<today>-migrated-plan` it appends, naming the plan and how many slices it migrated; and for each capability a work-item is under, `migrated-<capability>.md`, a capability-proposal `part_of` the initiative, `argues` the capability, status formulated, dated today.
- [r40] **If** `.shop/work/migrated-plan/` exists, `migrate plan` refuses and changes no file.
- [r41] **When** `migrate plan` finds no slice to migrate, it writes no initiative, proposal or work-item and says so, and still writes the observations.
- [r42] **When** `migrate plan` has run, `model check` reports no violation, unresolved reference or file problem in the files it wrote.
- [r43] **When** `migrate plan --dry-run` is run, it lists each slice it would migrate or drop and each entry it would make an observation, by the name `--drop` and `--leave` take.
- [r44] **If** `--drop` or `--leave` names a slice or entry the plan does not have, `migrate plan` refuses, naming it.
- [r45] **If** `migrate` refuses, it says why on stderr, exits 1 and changes no file; bad usage exits 2.

## Implementation, may change
- Python 3 with the standard library; moves are `git mv`, the commit date is `git log --diff-filter=A
  --format=%as -- <path>`. It does not commit.
- `run`'s steps, in order: ids, layout, decisions, deprecated. Every change is computed first, then written;
  a refusal in any step writes nothing.
- The ledger is read by `## (design-)?decision/<name>` headings; an entry ends at the next heading. Property
  lines are `<name>: <value>`, one a line.
- `plan` parses the old plan format (`## Slice <n>: <name>`, `- Kind:`, `- Scenarios: <feature> / <title>;
  …`, `- Check:`, `- Status:`, sections `Backlog` and `Log` of `- <date> <text>` entries); it does not use
  `scripts/plan`. `--drop` takes slice numbers, `--leave` observation names, both comma-separated.
- A slice's `Scenarios:` entry is split at `; ` between entries and at the first ` / ` within one.
- The help text (`--help`) is the contract.
- Exit status: 0 done, 1 refused or something left to migrate (`status`), 2 bad usage.

## Not yet
- Product-level repositories (jobs, a context-map) — trigger: shopsystem-knowledge is migrated.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/capabilities/spec-migration.md`

~~~~~~
---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/spec-migration
title: Spec migration
narrator: the person migrating a repository onto spec/
group: service
rests_on: [design-decision/one-spec-per-context, design-decision/gate-on-behaviour-lines, design-decision/migration-in-one-pass, design-decision/living-plan-to-work-items, design-decision/final-layout]
retired: []
---

# Spec migration

## Purpose
Moves a repository onto the final layout of design model v3 (design-decision/final-layout) in one pass,
whatever it has of the old system: design notes and approved feature files with no `spec/`, capability files
without ids, a decision ledger, top-level `decisions/`, `work/` or `records/`, `docs/superpowers/`, a living
slice plan, `@holding` scenarios. It is `migrating-to-capabilities`: the first integration where there is no
`spec/`, re-pairing the existing scenarios, and `scripts/migrate` for every mechanical change, with one gate.
It changes the meaning of no approved scenario.

## Behaviour
- [r1] **If** the working tree is not clean, a slice is in progress, or the suite does not run cleanly, migration stops before any change and says which.
- [r2] **When** migration drafts the spec, the person is shown the capabilities, which old features' scenarios each receives, every line no scenario backs, and every question, and nothing under `spec/` changes before their yes.
- [r3] **If** two scenarios with one title would land in one capability, the person is asked to retitle one at the gate.
- [r4] **When** migration is done, each capability has one feature file named for it, with the scenarios mapped to it; each scenario's effective tags, title, description and tables, and its Background steps followed by its own steps, are as they were, the new `@r<n>` tags aside.
- [r5] **When** migration is done, the suite's summary, its passing scenarios by title and its count of scenarios per tag equal those before it, retitles approved at the gate and the new `@r<n>` tags aside.
- [r6] **If** any of those differ beyond what they set aside, migration stops and reports the difference without editing a scenario.
- [r7] No step definition's body changes in a migration.
- [r8] **When** migration is done, each note is headed as a proposal integrated into `spec/` on its date.
- [r9] **Where** a repository has capability files whose Behaviour lines have no ids, **when** it is migrated to ids, each line gets `[r<n>]` in its order from r1 with its text unchanged, each capability gets `retired: []`, and each capability's id becomes `capability/<context path>/<name>`.
- [r10] **When** a repository is migrated to ids, its context's id is `bounded-context/<context path>`, the context path being the owner's domain, product and context name the person gives at the gate, unless `spec/index.md` already names them.
- [r11] **When** a repository is migrated onto `spec/` or to ids, each scenario that is not deprecated gets the `@r<n>` tag of the line it formulates, and nothing else in a scenario changes but the deprecations the gate led to and the renaming of r18.
- [r12] **If** a scenario formulates no line or more than one, migration to ids shows it to the person at the gate as a question and tags nothing before the answer.
- [r13] **When** migration onto `spec/` or to ids is done, the suite's summary, its passing scenarios by title and its count of scenarios per tag equal those before it, the new `@r<n>` tags, the deprecations the gate led to, and the " (deprecated)" titles of those and of r18's renaming aside.
- [r14] **When** a repository is migrated to ids, its `decision/<name>` references become `design-decision/<name>`, every frontmatter `id` under `spec/decisions/` and `.shop/` is written in full, its observation headings `## obs/<x>` become `## observation/<context path>/<x>`, and nothing else in a reference changes.
- [r15] **When** a repository is migrated, it ends on the final layout: decisions one file each in `spec/decisions/` with the generated `index.md`, work and records under `.shop/`, nothing of the plugin under `docs/superpowers/` or `.superpowers/`, and `migrate status` saying there is nothing left to migrate.
- [r16] **When** migration stops at the gate, the person is shown, besides r12's questions, each glossary bullet not in the glossary's form, each open slice of the living plan, and each backlog and log entry that would become an observation, and nothing after the mechanical move is committed before their answers.
- [r17] **When** migration is done, each open slice the person kept is a work-item accepting the requirements its scenarios are tagged with, each slice the person dropped is only in the archived plan, each entry the person did not leave out is an observation, and the plan and its archives are records under `.shop/records/archive/plans/`.
- [r18] **When** migration is done, each scenario that was tagged `@holding` is tagged `@deprecated`, with " (deprecated)" for " (held)" on its title and `Deprecated for:` for `Held for:`, and its test still binds it.
- [r19] **When** migration is done, each decision of the ledger is a decision file with the entry's text as its summary and Decision, and its `source` names by id the records the files it named became.
- [r20] **When** migration is done, `model check` reports no violation, unresolved reference or file problem, and no `v_s3` (a requirement has no scenario) but for lines that had no scenario before.
- [r21] **When** migration is done, each glossary bullet is in the glossary's form, in the words the person gave at the gate.
- [r22] **When** migration is done, the mechanical move is one commit, before the gate, in which no Behaviour line's text and no scenario but its renaming of r18 changes; the tags, work-items and observations the gate allowed are the next.
- [r23] **When** migration is done, the person is shown each file other than Markdown in which the migration rewrote a path it moved, with the line.

## Implementation, may change
- A baseline under `.shop/scratch/migration/`: the summary line, the passing tests (`-q -rA`), a copy of
  `features/`, and `features count --by-tag`.
- `scripts/migrate status`, `run` and `plan` (capability/migration-tools) make the mechanical changes; the
  session asks the context path before `run` when `spec/index.md` lacks it, maps scenarios to lines with
  `feature-formulator`, tags with `features tag`, then runs `plan` with the gate's `--drop` and `--leave`.
- `capability-writer` drafts with the migration brief; `features move` (with `--keep-feature-tags`,
  `--inline-background`) moves scenarios; `features verify-moved` compares them.
- Bindings follow step definitions: `scenarios(...)` per capability where every step has one body, otherwise
  `@scenario(<file>, <title>)` from the old modules.

## Not yet
None.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/decisions/0049-migration-in-one-pass.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/migration-in-one-pass
summary: "A consuming repository moves from the old system to the final layout in one migration, with one gate: scripts/migrate makes every mechanical change and is the only code that knows the old layout; the session does what needs judgment."
date: 2026-10-19
status: proposed
supersedes: [model-reads-a-ledger]
source: [observation/2026-10-19-final-state-only, review-finding/2026-10-13-kb-and-bdd-assessment]
by: "the person, 2026-10-19"
---

# 0049. Migration in one pass

## Decision

There is no intermediate state in a consuming repository. `migrating-to-capabilities` takes it from whatever
it has of the old system (a decision ledger, top-level `decisions/`, `work/` or `records/`, `docs/superpowers/`,
a living slice plan, `@holding` scenarios, lines without ids) to the layout of
design-decision/final-layout in one run, committed in two commits: the mechanical move, then the tags,
work-items and observations the gate's answers allow.

`scripts/migrate` does everything that is transcription: numbering lines, rewriting ids, moving files,
splitting the ledger into decision files, renaming `@holding` to `@deprecated`, and turning a living plan's
open slices into work-items. It refuses rather than guesses. The session does what is judgment: the context
path when `spec/index.md` lacks it, mapping scenarios to lines, glossary bullets out of form, which open
slices to keep and which plan entries to leave out. All of it is shown at one gate.

`scripts/model` and every other script read only the final layout: design-decision/model-reads-a-ledger,
rejected 2026-10-19, is superseded so that no reading of the ledger is ever built.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/decisions/0050-living-plan-to-work-items.md`

~~~~~~
---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/living-plan-to-work-items
summary: "A living plan's open slices become work-items under one capability-change initiative, migrated-plan, with one formulated capability-proposal per capability; its backlog and open log entries become observations; the plan itself becomes a record."
date: 2026-10-19
status: proposed
source: [observation/2026-10-19-final-state-only]
by: "the person, 2026-10-19"
---

# 0050. A living plan becomes work-items and observations

## Decision

- Each slice that is not green and that the person keeps at the gate is a `planned` work-item
  `work-item/<context path>/slice-<n>` (dots in `n` as hyphens). A capability slice is `under` the capability
  of its first scenario and `accepts` the requirements its scenarios are tagged with. An enabling or stack
  slice keeps its `check` and is `for` the first capability slice after it in the plan; with none after it,
  nothing needs it yet, and it is an observation.
- The work-items are parts of `initiative/<context path>/migrated-plan` (capability-change, `started`), through
  one `capability-proposal/<context path>/migrated-<capability>` per capability, `formulated` with no `adds`:
  its requirements are approved and formulated already. Its source is an observation of the migration.
- Each Backlog entry, and each Log entry that is a `QUESTION FOR THE SPEC:`, a `REQUEST` or a `RE-FORMULATE`,
  is an observation `about` the bounded context, unless the person leaves it out at the gate. Origins are
  triaged like any other.
- The plan's order is not kept as `blocked_by`: it said what should come first, not what must. Each
  work-item's body notes its place in the old plan.
- The plan file and its archives are `initiative-archive` records under `.shop/records/archive/plans/`.

## Alternatives

One defect initiative per slice (a defect initiative takes one work-item, and a slice is not a defect);
backlog entries as work-items (most are hardening noticed in review, which v3 makes origins, not work).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/work-items/kb-trial.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/kb-trial
kind: work-item
part_of: capability-proposal/model-in-consumers-spec-migration
status: drafted
wkind: capability
under: spec-migration
check: "a fresh clone of https://github.com/dstengle/shopsystem-kb under a scratch directory, the skill run headless against the plugin's working copy with the gate answered by the controller from the session's recommendations: migrate status exit 0, model check with no violation, unresolved reference or file problem but v_s3 for the lines that had no scenario before (10 at 2eed357), the suite 1603 passed as before, nothing pushed; recorded in .shop/records/measurements/fixture-runs/ with cost and turns"
blocked_by: [work-item/migration-skill]
---

# The migration on a clone of shopsystem-kb

A trial, not kb's migration: the clone is thrown away and nothing is pushed. Expect, from kb at `2eed357`:
371 lines numbered, 154 decision files (20 named `0001-` to `0020-` as they are), 31 ADRs to
`.shop/records/decision-arguments/`, one living plan whose only open slice is enabling with no capability
slice after it (so it becomes an observation, or is dropped at the gate: its status says it was done as
165.4), about 200 backlog and log observations, `tests/slices.py`'s `PLAN` path rewritten (and listed), and
two scenario-mapping questions as in the 2026-10-17 trial. Record what the gate showed, the two commits'
sizes, every refusal `migrate` gave and what the session did about it. kb's own slice machinery
(`tests/slices.py`, `@slice-<n>` tags) is left for kb.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/work-items/migrate-decisions.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-decisions
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r22-r26]
blocked_by: [work-item/migrate-layout]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py]
---

# The decisions step

Goes green: r22-r26.

- Ledger entries are `## design-decision/<name>` or `## decision/<name>` headings up to the next `## `
  (after the ids step every one is `design-decision/`). File name and frontmatter as r22 and r23; the title
  is the name with any leading `nnnn-` dropped and hyphens as spaces, first letter upper case.
- `source` (r25), for ledger entries and for decision files already under `spec/decisions/` (this
  repository's form): split at `;`, strip; a part beginning with an old or new path of a moved file → that
  file's record id (from the layout step's map) and the rest of the part, if any, to `by`; a part matching
  `<kind>/...` with a node kind → kept; anything else → `by`. Write `source: [a, b]` and
  `by: "<parts joined with '; '>"`, omitting either when empty.
- r24's refusals. r26: run `scripts/model decisions --root <root>` after writing (or call its renderer
  through the same import as the ids step), and include the index in the step's changes.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/work-items/migrate-deprecated.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-deprecated
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r27-r29]
blocked_by: [work-item/migrate-status-and-ids]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py]
---

# The deprecated step

Goes green: r27-r29.

- Reuse `scripts/features`' parser (import it as the ids step imports `model`) to find scenarios tagged
  `@holding`, their title line and `Held for:` line; edit those lines only.
- Bindings: `scripts/features`' `binding_calls` finds `scenario(<feature>, "<title>")` calls; rewrite the
  title constant in place as `features rebind` does, refusing a title written over several lines (r29).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/work-items/migrate-layout.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-layout
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r17-r21]
blocked_by: [work-item/migrate-status-and-ids]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py]
---

# The layout step

Goes green: r17-r21.

- The move table of r17, applied with `git mv` (directories whole where the destination does not exist,
  file by file otherwise); the ledger's `source` paths are read to find the other directories (`adrs/` on
  kb). A refusal for each collision (r18).
- r19: record frontmatter. The date is a leading `YYYY-MM-DD` of the file name, else
  `git log --diff-filter=A --format=%as -- <old path>` (first line), else today. Existing frontmatter is kept
  and the missing keys are added after its last line.
- r20: the moved paths are each file's path from the root before and after (and each moved directory's,
  with a trailing slash); replace whole occurrences in every tracked text file (`git ls-files`, skipping
  binary files and `.shop/records/`), longest path first; list each changed file that is not `.md`, with
  line numbers.
- r21: `.gitignore`.
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/work-items/migrate-plan.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-plan
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r30-r44]
blocked_by: [work-item/migrate-layout]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py]
---

# The living plan to work-items and observations

Goes green: r30-r44 (design-decision/living-plan-to-work-items).

- Parse the plan as `scripts/plan`'s `--help` describes the format (read it before i10 removes the script, or
  from git history): `## Slice <n>: <name>` blocks, `- Kind:`, `- Scenarios:` (entries `<feature> /
  <title>` joined by `; `), `- Check:`, `- Status:` (the word before the colon), `## Backlog` and `## Log`
  entries `- <date> <text>` with indented continuation lines. A slice with a Status word not in planned,
  in progress, green, blocked is refused.
- Files written: `.shop/work/migrated-plan/initiative.md`, `migrated-<capability>.md` per capability,
  `slice-<n>.md` per work-item, in the forms of r33-r39 and `scripts/model --help`; observations appended to
  `.shop/records/observations.md` (created with `# Observations` and the line "Dated, never edited." when
  missing). Ids and file names must pass `model check`'s id rule (`[a-z0-9]+(-[a-z0-9]+)*` after the context).
- `--dry-run` (r43) prints `slice <n>: work-item | observation | drop` and `observation <name>: <first 80
  characters>` lines.
- A scenario test runs `model check` on the result (r42).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/work-items/migrate-status-and-ids.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migrate-status-and-ids
kind: work-item
part_of: capability-proposal/model-in-consumers-migration-tools
status: drafted
wkind: capability
under: migration-tools
accepts: [migration-tools#r1-r16, migration-tools#r45]
blocked_by: [work-item/final-layout-read, work-item/deprecated-and-sources]
fileset: [scripts/migrate, tests/scenarios/test_migration_tools.py, tests/scenarios/conftest.py]
---

# scripts/migrate: status, the run's frame, and the ids step

Goes green: the scenarios of migration-tools r1-r16 and r45, in `tests/scenarios/test_migration_tools.py`
bound by `scenarios("migration-tools.feature")` (the feature file is written at formulation); the other
steps' scenarios stay red for the work-items after this one.

- `scripts/migrate`, Python 3 standard library, `--help` its contract (CONTRACT text like `scripts/model`'s),
  argparse: `--root`; `status`; `run [--context ID] [--dry-run] [--tests DIR]`; `plan [--plan FILE]
  [--drop LIST] [--leave LIST] [--dry-run]`. Exit 0, 1 (refused, or `status` found something), 2 usage.
- The frame every step uses: a step returns a list of changes (move, write file, rewrite file) and a list of
  refusals; `run` computes all steps on an in-memory view of the tree, then refuses with every refusal or
  writes every change (r7-r10). Printing: `<step>: <change>` lines, then `<step>: <n> changes`.
- `status` (r2, r3): the checks in r2's order, one line each, naming the path.
- The ids step (r11-r16), the 0.19.0 Adding Ids step 2 as code (skills/migrating-to-capabilities, Adding
  Ids, step 2 has the rules): index id, `[r<n>]` numbering, `retired: []`, capability ids, `decision/` and
  `obs/` rewrites in frontmatter and headings, frontmatter ids in full, `formulated_as`. It works on the files
  wherever they are when it runs (before the layout step moves them): `decisions/`, `work/`, `records/`,
  `spec/decisions.md`. Reuse `scripts/model`'s frontmatter reader by importing it from the script's
  directory (`importlib` from `Path(__file__).with_name("model")`), so both read one YAML subset; write
  frontmatter by editing lines in place, never by re-serialising, so nothing else in a file changes.
- Step fixtures: a builder in `tests/scenarios/conftest.py` for an old-layout repository (a git repository
  in a temporary directory with `git init`, an identity, and an initial commit).
~~~~~~

## `.shop/scratch/from-job/design-drafts/i11-i8/i8/work-items/migration-skill.md`

~~~~~~
---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migration-skill
kind: work-item
part_of: capability-proposal/model-in-consumers-spec-migration
status: drafted
wkind: capability
under: spec-migration
check: "T-migrate-final, the fixture case of initiative i8's 'How it is shown working', run 3 times with claude -p --plugin-dir the working copy, the gate answered by the harness: each run ends with migrate status exit 0, model check exit 0, the suite's summary and passing titles equal to the baseline's, features verify-moved clean before tagging, the mechanical move and the gate's changes as two commits, the expected work-items (2) and observations (backlog and log entries less those left out), and nothing under docs/superpowers/ or .superpowers/; 3 of 3, recorded in .shop/records/measurements/fixture-runs/"
blocked_by: [work-item/migrate-decisions, work-item/migrate-deprecated, work-item/migrate-plan]
fileset: [skills/migrating-to-capabilities/SKILL.md, agents/capability-writer.md, README.md, docs/capability-format.md]
---

# migrating-to-capabilities moves a repository to the final layout

spec-migration's lines are workflow (no scenarios; design-decision/workflow-scenarios-run-as-fixture-sessions),
so the check is the fixture case.

`skills/migrating-to-capabilities/SKILL.md`:
- Description: also when a repository has `spec/decisions.md`, top-level `decisions/`, `work/` or `records/`,
  `docs/superpowers/`, a `*-slices.md` plan or `@holding` scenarios, or when `migrate status` exits 1.
- Preconditions as now (clean tree, no slice in progress, a clean baseline), the baseline under
  `.shop/scratch/migration/`.
- "Moving to the final layout" replaces "Adding Ids", in this order: (1) `migrate status`; if
  `spec/index.md` has no id, ask the person for the context path and stop until they answer; (2) `migrate
  run --dry-run`, then `migrate run --context <id>`; verify: suite summary and passing titles equal (the
  " (deprecated)" retitles of r18 applied to the baseline), `features verify-moved --from <baseline>/features`,
  `git diff --word-diff` of `spec/capabilities/` showing only `[r<n>]`, `retired: []`, ids and the removed
  `formulated_as`; commit alone, `migrate: final layout`; (3) map the scenarios with `feature-formulator`
  as Adding Ids step 3 does now; (4) one gate: the mapping's questions, glossary bullets not in form (the
  person's words for each), `migrate plan --dry-run`'s slices (keep or drop) and observation entries (keep
  or leave out; offer "all kept" for a long list), every file other than Markdown `run` listed; (5)
  `features tag` per row, `features deprecate` and `features rebind` for scenarios the answers deprecate,
  the glossary bullets rewritten, `migrate plan --drop … --leave …`; (6) verify: `migrate status` 0,
  `model check --limit 100000` with no violation, unresolved reference or file problem but `v_s3` (a
  requirement has no scenario) for lines that had none, suite equal, `features count --by-tag` equal but
  the new tags and deprecations; commit `features/`, the rebound tests, `spec/` and `.shop/` together.
- The first-spec Process: the drafts path `.shop/scratch/drafts/<date>-migration/`; the writer's decisions
  are files copied into `spec/decisions/` and indexed with `model decisions` (no `decisions.append.md`); the
  `Scenarios:` rewrite of the living plan goes; step 6 ends with "Moving to the final layout" for what is left.
- Red flags and rationalizations: a ledger kept "for later", a plan edited by hand, an observation written by
  hand for a backlog entry, `migrate run` output edited before the commit.
- `agents/capability-writer.md`'s migration brief: one decision file per ADR and per note decision, `source`
  naming the ADR's record id once moved (the brief gives the map), not a ledger entry.
- README and `docs/capability-format.md`: one paragraph on migrating, naming `scripts/migrate`.

Fixture T-migrate-final, built by a generator `make_oldlayout.py` in `/home/vscode/scratch/shopsystem-bdd/`
from `make_shelf.py`: two capabilities (lines without ids), `spec/index.md` without frontmatter and a glossary
with one bullet `- **revision** — the count of writes` not in form, `spec/decisions.md` with four
`## decision/<name>` entries (one `supersedes:`, one `revisit_when:`, sources naming
`docs/superpowers/specs/<note>.md`, `adrs/0001-<x>.md` and words), `adrs/` with one ADR, features with
pytest-bdd steps (one module binding by `scenarios()`, one by `@scenario(file, title)`), one `@holding`
scenario bound by title, `docs/superpowers/plans/<date>-shelf-slices.md` with a planned capability slice,
an enabling slice before it, a blocked capability slice, two backlog entries and two log entries (one
`QUESTION FOR THE SPEC:`), `docs/superpowers/plans/archive/` with one archived batch, a requests file; the
gate's answers in the harness: context `bounded-context/missingmass.io/demo/shelf`, the glossary bullet's
form, drop the blocked slice, leave out one backlog entry. Every line has a scenario, so `model check` exits
0.
~~~~~~
