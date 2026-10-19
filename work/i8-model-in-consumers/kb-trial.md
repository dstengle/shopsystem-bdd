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
