# Plan 5 of 7: this repository's spec migrated, the old reading deleted

Implementation plan for `design.md` (this folder), phase 5. Read plan 1's "The whole branch" first.

## Goal

This repository's specification is the four parts: `spec/model/` (six areas, design §3.3), `spec/vocabulary/`,
the 455 live lines and 5 universal conditions reworded into domain verbs and services in 22 new capability files with
new ids (§3.6, §9.2, §9.3), `spec/moves.json`, and `spec/adapters/cli.toml`; the features generated anew. Then, in the
same phase, the old reading is deleted: one machinery. Scenario handlers and docs follow in plans 6 and 7.

## Tasks, in order

1. **The model** (§9.1.1): `spec/model/specification.md`, `tracking.md`, `execution.md`, `measurement.md`,
   `analysis.md`, `upgrades.md` from §3.3, reconciled with the 126 glossary entries and every capability's `## Terms`
   and `## Relations`; `python3 scripts/model check` clean of v_m8.
2. **The vocabulary** (§9.1.2): `spec/vocabulary/<area>.md` and `shared.md`, every existing term mapped onto its
   element, the operation verbs new; words of the retired 0.30 vocabulary out of every layer. Clean of v_t18-v_t20.
3. **`spec/adapters/cli.toml`** for this repository: every operation of the model with its command (or `hook`) and
   parameters, `[unexposed]`, `[cli-only]`, `[environment]`; clean of v_a1-v_a4.
4. **`scripts/spec_moves.py`** (session's call: the scaffolding is a module kept for its readers, not a throwaway):
   `apply(root, table)` reads `.shop/records/2026-11-19-domain-contract/rewording.tsv` (old id, new capability, new
   group title, new text) and writes the new capability files (frontmatter `area:`, `specifies:`, `narrator`, `group`,
   `language: codified-2`, `retired: []`, `unbuilt: []`; `## Purpose`, `## Behaviour`; ids from r1/g1), each old
   capability's lines out of `## Behaviour` with every id into `retired:` and a `## Moved` table, `spec/moves.json`;
   `resolve(root, old_id)` read by `model check`'s retired-id rule (a moves.json missing a live id or naming one twice
   refused), `spec/restated.json`'s readers (`scripts/spec_read.py`, `scripts/model_restates.py`), `request_lines`
   and `retires:` readers (`scripts/backlog_items.py`, `scripts/backlog_reword.py`, `scripts/request_accept.py`).
   First `git mv spec/capabilities/batches.md spec/capabilities/batches-0.37.md` and the same for `trials.md`
   (directive-4), their own features likewise.
5. **`rewording.tsv`**, the session's work (§9.2), capability by capability, each row's text checked with `python3
   scripts/model parse` until it reads and then `python3 scripts/model logic` until no new finding. **Session's call
   (person offline)**: the implementer may hand one area's rows to one subagent at a time (it writes only that area's
   rows of the tsv and reports what it renamed in the model or vocabulary); the implementer applies, checks and
   commits. Group titles reworded with their lines (no command codes). Corrections to §3.6's drafted column are made
   here (the drafted column sums to 458: each id lands once).
6. **Universal conditions** (§9.3) in `spec/universal.md`: U17, U18, U19 new; U12, U13, U14, U15, U16 into
   `retired:`.
7. **`spec/index.md`**: `imports: [request, spec]`, `## Glossary` emptied (its entries moved by task 2), Composition by
   area; each capability's `## Terms` and `## Relations` emptied.
8. **The ready items** b318 (5 lines), b309 (3), b334 (1): their lines reworded into the new words by editing
   `.shop/backlog/b318.md`, `b309.md`, `b334.md` (session's call §10: `work line --reword` cannot run mid-branch);
   they pass `python3 scripts/work ready` on the migrated spec. Shaped items and q14 left in their words.
9. **The corpus** `grammar/corpus/spec/` regenerated through `scripts/spec_corpus_write.py`'s `with_block` and
   `without_block` (each new id with `From: <old-cap>#r<n>.`); the frozen copy
   `tests/scripts/fixtures/entailment/` re-frozen from the migrated spec, its expected L8s mapped through moves.json.
10. **Features**: `python3 scripts/features generate` writes the 22 new features and removes the retired ones.
11. **The old reading deleted** (bootstrap ends): `scripts/spec_lf_option.py`; the CLI pack's run frames and `OPTION`/
    `k_option_SetTo` in `scripts/spec_rgl.py`; `WhenRuns`, `ThenPrints`, `ThenExitsErr`, `ThenExitsOk` in
    `scripts/features_vocab4.py`; the run/exit/print branches of `spec_lf_facts*.py`; `refuse_defined` and the bridge
    in `spec_entail.py`/`grammar/entail.lp`; the run slots in `spec_steps4*.py`; `CORE_VERBS`' cli set; the glossary/
    `## Terms` source path of `spec_lexicon`/`spec_relations` (session's call: an entry left there is a vocabulary
    entry with no element, v_t18); the bootstrap #12 construct; every test marked `BOOTSTRAP = True` (plan 2). The
    module map rows follow (`spec_lf_option` replaced by `spec_lf_request`).

## Tests to write first

- `tests/scripts/test_spec_moves.py`: `apply` on a two-capability fixture writes new files, `retired:`, `## Moved`,
  moves.json; a table missing a live id or naming one twice refused; `resolve` of an old id; the `-0.37` renames read.
- `tests/scripts/test_spec_migrated.py`: every live line of this repository parses (v_p*), uses only model elements
  (v_m1-v_m3), every declared refusal stated (v_m4), every operation requested (v_m7); moves.json covers every id
  retired by the move once.
- `tests/scripts/test_readiness_lay_model.py` gains the case on the migrated spec: an item with a model line, a
  vocabulary entry and a requirement line passes `work ready`; b318, b309, b334 pass it.

## Exit check

```
python3 scripts/tools size --limit 300
python3 scripts/model check                      # 0 violations; w_m5 warnings of the task lifecycle accepted (session's call §5.5)
python3 scripts/model logic                      # no finding not in baseline-logic.txt, ids mapped through spec/moves.json
python3 scripts/features generate --check        # every group of every capability has its scenario
python3 scripts/model rules --check && python3 scripts/model forms --check && python3 scripts/model constructs --check
python3 -m pytest --ignore=tests/scenarios \
  --ignore=tests/scripts/test_docs.py --ignore=tests/scripts/test_docs_lines.py \
  --ignore=tests/scripts/test_agents.py --ignore=tests/scripts/test_skill_shaping_items.py
```

Left red, each restored by a later phase and nothing else: `python3 scripts/features vocab --check` and
`tests/scenarios/` (the handlers keyed on `WhenRuns`, plan 6); `tests/scripts/test_docs.py`, `test_docs_lines.py`
(the docs and notes-cli in old words, plan 7); `test_agents.py`, `test_skill_shaping_items.py` (skills and agents in
CLI-pack words, plan 7), each only if it fails. Any other failing test is fixed in this phase.
