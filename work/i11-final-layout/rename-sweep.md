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
