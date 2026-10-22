---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-19-job-migration-release-common-brief
kind: initiative-archive
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-19
---

# The migration release's common drafting brief

The common brief given on 2026-10-19 to the agents that drafted the migration release (0.21.0) of shopsystem-bdd: the person's standing directions of that day (final state only, the layout, ids for references, "deprecated", rule labels, pytest-bdd, light decisions) and what each drafting agent was to deliver. The drafts it produced are decision-argument/2026-10-19-job-i10-delivery-drafts and decision-argument/2026-10-19-job-i11-i8-final-layout-and-migration-drafts. Copied out of a job workspace on 2026-10-22.

Archived from `.shop/scratch/from-job/design-drafts/common.md` (git-ignored scratch), text as it was.

---

# Common brief: drafting the migration release (0.21.0) of shopsystem-bdd

Repository: /home/vscode/shopsystem-bdd, branch release-0.21.0 (cut from main a950047). The plugin is
moving onto design model v3 (docs/design-model/: design-model.md, grammar.md; how-we-got-here.md for
history). Read docs/capability-format.md, spec/index.md (its Glossary), spec/capabilities/*.md,
decisions/*.md (light form: summary + Decision; Context/Alternatives only for a real trade-off),
work/README.md and work/*/initiative.md, records/README.md, and the skills/, agents/ and scripts/ you need.

The person's standing directions (all 2026-10-19 unless dated):
- Only the final state and migration tools. No intermediate states, no investment in the old system
  beyond migration tools. Nothing of slicing, slice plans, lanes, steps or superpowers survives in the
  plugin's final state, except what i12 (batch measurement on v3, next release) needs left alone:
  scripts/measure, spec/capabilities/batch-measurement.md and skills/analyzing-a-batch stay as they are.
- Layout: spec/ is top level and stands alone (decisions in spec/decisions/<n>-<slug>.md with a generated
  index); work/ and records/ go under .shop/; features/ stays with the code. Superpowers directories
  (docs/superpowers/, .superpowers/) are not used by the plugin in the new version.
- References are ids, never relative paths. Ids are type-first: <kind>/<owner>/<product>/<context>/<name>,
  short form <kind>/<name>; this context is bounded-context/missingmass.io/shopsystem/shopsystem-bdd.
  A requirement is written only capability/<name>#r<n> (decision 0036; #behaviour/r<n> no longer accepted).
- "deprecated" replaces held/holding/superseded: tag @deprecated, `features deprecate`,
  `features deprecated`, a `Deprecated for:` line; glossary entry **deprecated scenario** (Not: held,
  holding, superseded). "hold" and "carry" in other senses become plain words (stays valid, has, contains,
  enforced by, do).
- Every model rule gets a plain label (v_s1: a scenario names no requirement; v_s3: a requirement has no
  scenario; …) printed by `model check` beside the code, defined once in model.lp.
- This repository's scenarios run as pytest-bdd step definitions (unittest binding was rejected). The
  plugin takes the dependencies it needs (decision 0035: clingo, pytest, pytest-bdd).
- The implementer's skills are the ones its definition lists; no Skill tool.
- The spec-round agent is now initiative-round.
- Plugin evidence is not the cheap option: workflow behaviour is shown by repeated headless fixture runs
  (claude -p against fixture repositories); scripts are fully described by requirements.
- Decisions are light. Words: requirement (not "behaviour requirement"), measurement (not fact, in i12),
  fact (only model facts' sense).

You are DRAFTING, not implementing. Write only under your drafts directory; change nothing in the
repository. The person approves drafts at the gate later; nothing you write is approved.

Deliverables, in your drafts directory, in the final layout's form (frontmatter as grammar.md and
`scripts/model --help` define for each kind):
1. `initiative.md` per initiative: its body expanded into the design (what the final state is, why,
   what is removed), short and concrete, in the plugin's prose style (plain, no padding).
2. One capability-proposal per capability changed (`<initiative-name>-<capability>.md`, status drafted,
   argues/adds/changes/removes with requirement ids), AND beside it the full proposed capability file
   (`capabilities/<name>.md`) as it would read after the change: Behaviour lines in EARS with [r<n>] ids
   (keep existing ids for kept lines; new ids continue past the highest id ever used, retired ids in
   frontmatter), Purpose, Implementation-may-change, Not yet. New capabilities likewise.
3. Proposed decisions (`decisions/<n>-<slug>.md`, status proposed, numbers from 0037 upward in the order
   given in your brief), only where something is decided that a line can't carry.
4. Work-items (`work-items/<name>.md`, kind work-item, status drafted, `part_of` its capability-proposal,
   `depends_on` others, the requirements each accepts, and a short body: what goes green and roughly
   which files) breaking the implementation into pieces one fresh implementer can take each.
5. `NOTES.md`: open questions with your recommended answer for each (the person is away; the
   coordinator rules), anything in the repository that contradicts the directions, and risks.

Reply in at most 15 lines: what you wrote, counts, and the top three open questions.
