---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/migration-skill
kind: work-item
part_of: capability-proposal/model-in-consumers-spec-migration
status: withdrawn
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

Withdrawn 2026-10-19: deferred until the skeleton runs (initiative notes)
