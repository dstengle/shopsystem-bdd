---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-report-p5
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# Report: P5, `model` reads the codified spec

Branch `gfc/P5`, commit 9eda895f. Written by the layer 2 merge from the package's returned notes: the harness refused
the package's own write of this file.

## What was built

- `scripts/model_spec.py` (SpecReading): codified capability files give groups, `member_of`, `in(G,C)`, `group_id`,
  `restates`, `codified`, `retired_group`, `parsed`/`unparsed`/`ambiguous`, `pre` (v15k) and `logic_only`. It reads
  `spec/universal.md` (U nodes `universal-condition/<path>/u<n>`), `restated.json` (`restated_id`), and a codified
  index's glossary through `spec_lexicon` (`typed`, `category`, `value_of`, `linearises`). A scenario's `@g<n>` tag
  gives `generates`; nothing is written as `has_sc`.
- `scripts/model_legacy.py`: the 0.29 bullet and glossary reader, with `ears` and `behaviour_items` moved out of
  `model_parse`.
- `scripts/model_restates.py`: `model restates`.
- `scripts/workqueue_lines.py`: the line check behind `work request`.
- `model_facts.py` dispatches each file on its own marker, takes `<cap>#r<n>@0.29` through `restated.json` (`old_ref`,
  exempt from v3; a work-item may accept such an id with no scenario). KINDS is v5's; the LEGACY kind bridge in
  `model.lp` is gone. `model.lp` adds v_p1, v_p2 and v_p3.
- `scripts/model`: new subcommands `parse` (with the hint), `lexicon [--check]`, `logic` (lazy import of P6's
  `spec_solve`) and `restates`. `why` follows restates. The contract is rewritten for v5 (v_d5 in place of v_d2, no
  "version 3").

## Calls made

- Term ids keep the 0.29 keys (tested: the live glossary's old id set is a subset of the new one).
- A word given in a second category becomes `<word>-<category>`; a value becomes `<value>-of-<kind>`.
- `linearises` carries category, term and kinds, so v_t6 matches spec_lexicon's "given n times". The reserved-verb and
  determiner cases appear only in `lexicon --check`.
- Codified statements give no `mentions` facts (C27).
- `given_unparsed` (v_p3) appears only once the Steps grammar exists (P7). At the layer 2 merge it was switched to
  P7's typed Steps grammar (see gate-L2.md).

## Checks (SHOPSYSTEM_GF unset, P1's install)

- pytest `test_model_spec.py`, `test_model_restates.py`, `test_workqueue_request_parse.py`: 32 passed.
- `model parse` on the `proposed` line: exit 0, one tree. On the `drafted` line: exit 1, output names `` `drafted` ``,
  "parsed up to:" and "nearest words:".
- `model lexicon --check` on the live repo: exit 0 (148 terms, 0 problems).
- `model restates spec-migration`: exit 1, first line `spec-migration#r1: ...`.
- A fixture repo with a codified index: `work request` with a non-parsing line exits 1, names it, writes no file
  (in-process and through the CLI).
- P3's no-new-rows check: empty.
- `tools size --limit 300`: exit 0 (largest owned: `model_facts.py`, 287). Suite: 23 failed = baseline, 1226 passed.
  Model tests plus `test_design_model_check.py`: 322 passed. ruff clean.

## For P14

- Delete `model_legacy.py` and the uncodified branches: `read_glossary_legacy`, `read_legacy_behaviour` and
  `legacy_scenario` in `model_facts`, the `ears` branch of `workqueue_lines.check`, and v_e1/v_e2 and the legacy has_sc
  clauses (v_s2, v_s3, v15f) in `model.lp`.
- `model_work.py` still turns `<cap>#r<n>` in adds/removes/changes into a capability and a number; a `@0.29` id
  resolves there only because it is registered in `Model.nodes` (no node fact). When P14 migrates old references it
  may want `model_work` to see `@0.29` explicitly.

## Module-map rows

- `scripts/model_spec.py` | `model`'s reading of the codified spec: groups, requirements and their parse, universal
  conditions, `restated.json`, the typed glossary, generated scenarios (`@g<n>`)
- `scripts/model_legacy.py` | `model`'s reading of 0.29 capability files and untyped glossaries, and the EARS shape
  check (removed at the release)
- `scripts/model_restates.py` | `model restates`: the coverage of the 0.29 ids by groups, `## Dropped` and moves
- `scripts/workqueue_lines.py` | `work request`'s check of its lines: parsed in the upstream's grammar when its index
  is codified, else the 0.29 shape
