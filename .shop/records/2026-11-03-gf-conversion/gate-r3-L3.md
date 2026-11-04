---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-gate-r3-l3
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Revision 3, layer 3 gate

The gate passed on `gf-conversion`. Base 49b3d5d0. All three task branches had been reset by their tasks from
`main` to that commit, and all three merged with `--no-ff` without conflicts (CLAUDE.md auto-merged: S7 and S8
change different rows).

## Merged

- **S7** (2fe70e70, merge 03498eb9): `spec_engine`, `spec_trace`, `spec_logic`, `spec_logic_np`, `background.lp`,
  `cone.lp` and their tests deleted; `spec_logic_vocab` keeps only `Vocab` and `domain` (`facts`, `pools`, `guards`,
  `guard_id`, `AMOUNT` gone, nothing used them); telingo unpinned from `tools_grammar` (`WHEELS`, `WITHOUT`),
  `scripts/tools`, `tests/toolchain.py` and the tool tests; the CLAUDE.md rows as the plan lists them; and
  `test_nothing_imports_telingo_or_the_old_solver` as the plan writes it (`re.MULTILINE` for ruff). Reviewed: no
  import of the old modules is left in `scripts/`, every remaining `telingo` hit in `tests/` is a negative assertion.
  The extra edit to `scripts/model.lp`'s comment is right.
- **S8** (8ac6bc05, merge 050ce2f0): the ceiling hooks in the root conftest, `tests/scripts/conftest.py` with
  `live_logic`, `EXPECTED` and `live_expected`, the `live_logic` marker, the live tests rewritten, `test_byte_stable`,
  and two calls beyond the plan, both accepted: `scripts/spec_parse_cache.py` (with its row; the parse cost the L2
  gate left for S8/S12) and `spec_grammar._context` (the lexicon read once per state of the files, not three times a
  line). Reviewed: the cache key covers everything `_raw` reads (sources sha, grammar, text, lexicon words, `LIMIT`);
  the memo's state includes `grammar/*.gf` as well as `spec/**/*.md`; the cache test isolates `XDG_CACHE_HOME`.
  `EXPECTED` reaches tests through a fixture rather than an import, a sound departure from the plan's wording.
- **S9** (1eb8b308, merge 8512ff36): README, capability-format, grammar.md, design-model.md (C38) and the skill
  describe facts → `check.lp` → L0-L5 and solver-free generation; `test_no_doc_names_telingo_as_current`.

## Fixed on gf-conversion

- README.md "New tools" bullet: S9 left one 177-character line; rewrapped at the file's width.
- `report-S8.md` and `report-S9.md` written by the gate from the tasks' notes (the harness refused the tasks' own
  writes), committed with this record.

## Results

- `python3 scripts/tools size --limit 300`: exit 0.
- `timeout 600 python3 -m pytest -n 8 -q -m "not fixture and not live_logic" --ignore=tests/scenarios/test_supervision.py`:
  821 passed, 1 skipped, 129 subtests passed, 12.95 s wall. No test over the 10 s ceiling (no ceiling lines printed).
- Not run, by the rules: the 13 `live_logic` tests (they solve the live spec; S12 runs them first, S11 once) and
  `tests/scenarios/test_supervision.py` (still old; not rewritten by any merged task).

## Left

- `$SLOW` is now `-m "not fixture and not live_logic" --ignore=tests/scenarios/test_supervision.py`; every other
  old solver-driven test file is deleted or rewritten.
- `spec_context._once` and `spec_grammar._context` are not thread-safe (nothing threads them today).
- `docs/capability-format.md` lines 217-219 and 402 and several README lines exceed 120 characters; they were so
  before this layer.
