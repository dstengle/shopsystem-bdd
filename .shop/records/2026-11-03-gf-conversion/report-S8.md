---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s8
kind: report
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# S8: the live-spec tests share one run; the 10 s ceiling

Written by the layer 3 gate from the task's notes: the harness refused the task's own write of this file.

## What changed

- Root `conftest.py`: `pytest_runtest_logreport` sums each test's setup, call and teardown on the controller;
  `pytest_terminal_summary` prints `tests over the <c> s ceiling:` and `<s> <nodeid>` lines, slowest first. The
  ceiling is `$SHOPSYSTEM_TEST_CEILING`, 10 by default. It reports and never fails. `test_ceiling.py` copies the
  real root conftest into a tmp project.
- `tests/scripts/conftest.py`: the session fixture `live_logic` (`spec_solve.run(REPO)`) and `EXPECTED = {}`,
  passed to tests through the session fixture `live_expected` (a test module cannot import a conftest by name,
  because the root conftest has the same module name). The marker `live_logic` is registered in `pytest.ini`.
- `test_spec_guarantees`, `test_revision_done` and `test_features_generate` rewritten as the plan says:
  `test_model_logic_on_the_live_spec_is_fast` (marked), `test_check_on_the_live_repo_is_fast_and_clean`, and
  `test_byte_stable` on two tmp copies of the live `spec/` under `PYTHONHASHSEED` 1 and 2.
- `test_e2e_codified` already asserted the L3 `work-queue#r2` refusal; it now sets `PYTEST_XDIST_AUTO_NUM_WORKERS=2`
  in its commands' environment, since its 9.6 s deliver phase was `work run`'s `-n auto` starting 32 workers for
  two scenarios. The default `-n auto` path stays under test.

## Calls made

1. New `scripts/spec_parse_cache.py` (with its CLAUDE.md row): GF's parse before the guards cached on disk under
   `~/.cache/shopsystem-bdd/parse/<sources sha>/<grammar>/<key>.json`, keyed by the sources sha, grammar, lexicon
   words, GF text and `LIMIT`; written by rename; an unreadable cache is skipped. Cold and warm runs give byte-equal
   features; `model check --json` and `model parse` of the core corpus match the output from before. The live check
   takes 0.76 s warm (6.1 s cold before).
2. `spec_grammar._context`: (lexicon, sources, sha) memoised per state of `spec/**/*.md` and `grammar/*.gf`
   (mtime_ns and size), re-read when `spec_lexicon.read` is replaced. The parse read the lexicon three times a line
   before; `test_revision_done`'s model check fixture went from 10.6 s to 1.2 s.

## Test runs (timeout 600)

- `test_ceiling.py` before the hooks: 1 failed, 1 passed (the expected red).
- The plan's step 4 list with `-m "not fixture and not live_logic" -n 4`, plus `test_spec_parse_cache` and
  `test_spec_grammar`: 155 passed in 7.97 s, none over the ceiling.
- `tests/scripts` (less S7's deletions) with the same marks: 616 passed, 1 skipped, 125 subtests, 13.6 s.
- `--collect-only -m live_logic`: 13 tests (11 in `test_spec_guarantees`, 2 in `test_revision_done`).
- Slowest: `test_e2e_codified` 6.1 s (was 11.2 s), live `features --check` 2.3 s, `test_byte_stable` 1.2 s.

## Left open

- The `live_logic` tests have not run; S12 runs them first.
- The 2 s and 5 s speed tests warm the parse cache with a first run; a cold live parse costs about 6 s.
- `spec_context._once` and `spec_grammar._context` are not thread-safe; nothing runs them on threads today.
