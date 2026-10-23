---
id: initiative/missingmass.io/shopsystem/shopsystem-bdd/i11
title: This repository on the final layout and conventions
summary: This repository moves to the final layout and conventions of design model v3, the ones the plugin teaches and i8 migrates consuming repositories to.
kind: capability-change
owner-level: shopsystem-bdd
status: done
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
