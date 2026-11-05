---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p4
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P4, `model check` graph rules to v5

Branch `gfc/P4`, commit ce403243. Written by the layer 1 merge from the package's returned notes: the harness refused
the package's own write of this file.

## What was built

No new modules. Files changed: `scripts/model.lp`, `model_work.py`, `model_requests.py`, the four `test_model*.py`
files, `design_model_check_{glossary,problems,requests,then,trace}.py`, `features/design-model-check.feature`.

- `model.lp` rewritten for v5. New kinds: requirement, requirement-group, scenario, universal-condition (standing).
  job-thread is now a root, glossary-proposal a part, design and analysis record kinds. `has_req` is derived from
  `member_of`. v1, v7b, v_k1, v_k2, v_b2 and the needs/from_cap/across inputs are gone. Per §7.2: v3 merges both
  clauses, v7 is v4's, v18a-c are v4's (over `#defined at/2`), v18d is the old v18, v_d2 is v4's, v_d5 is the old
  v_d2, w_stale_proposed is the old w_stale_intake, and w_stale_intake and w_many_requests are v4's. v_d4 added. New
  rules: v15g-k, v15e on grouped requirements, v15f and v_s1-s3 on groups, v_s4, v_t4-t6, each silent until P5 emits
  its facts.
- `model_work.py`: the v5 lifecycles, design-decision statuses (checked only when present); `accepts` takes
  `<cap>#g<n>`; design and analysis records keep ids `record/<path>/<name>`.
- `model_requests.py`: emits `line/3`, `outcome/3` (first word of the outcome), `upstream/2`,
  `resolution_of_line/2`, and `age/2` when the request has a date.

## Calls made under the delegation

1. v16a keeps its date cutoff for now, against §7.2: dropping it before old initiatives are compacted adds 23 live
   rows. A comment in `model.lp` says it goes at compaction (P14).
2. v7 stays silent until a context-seam node exists. Askers of the form `product/...` are exempt.
3. `merged` is kept as a LEGACY status, allowed only under a done or abandoned initiative (45 live proposals).
4. v15k is included: design §8.2 names it and no package claimed it.
5. v_s4 is a new code for a requirement in no group or in two (C28).
6. v_e1 and v_e2 stay, marked LEGACY; P5 replaces them with v_p1-v_p3.

## Checks

- pytest on the model tests and `test_design_model_check.py`: 272 passed, 80 subtests passed.
- `model check` shows no `kind 'design'` row (live file problems 8 → 3); no `cross-context-request|needs(|v_k1|v_k2|v_b2`
  in `model.lp`; `model rules` lists v_d5 and w_stale_proposed. `tools size` exits 0; the suite is at baseline.

## For later packages

- Refresh `baseline-model-check.txt` after layer 1: two rows are relabelled headers with unchanged counts (v3 (8),
  v_s3 (2)). Done at the layer 1 merge.
- P5 (`model_facts.py`): KINDS still lists cross-context-request and acceptance-scenario; the reader still emits
  capability-requirement and acceptance-scenario, which `model.lp` reads through a LEGACY bridge. For codified
  scenarios emit `generates(G,S)`, not `has_sc`, or the legacy v_s2 clause fires. Facts the new rules read:
  `member_of/2`, `in(G,C)`, `group_id/3`, `generates/2`, `restates/2`, `restated_id/1`, `retired_group/2`, `u_id/2`,
  `codified/1`, `logic_only/1`, `pre/2` (v15k), `typed/1` (gates v_t4), `category/2`, `value_of/3`, `linearises/2`;
  `parsed/1`, `unparsed/2`, `ambiguous/1` are declared.
- P5 (`scripts/model`): the contract text still says v_d2 for the abandoned-initiative rule (now v_d5) and version 3.
- P11: `spec/capabilities/design-model-check.md` still names v18 and v_d2, and its r113 line keeps the v16a cutoff.
