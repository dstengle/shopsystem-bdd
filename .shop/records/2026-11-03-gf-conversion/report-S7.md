---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s7
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Report S7: the old solver deleted, telingo unpinned, the module map

## What changed

- **Deleted:** `scripts/spec_engine.py`, `scripts/spec_trace.py`, `scripts/spec_logic.py`, `scripts/spec_logic_np.py`,
  `grammar/background.lp`, `grammar/cone.lp`, `tests/scripts/test_spec_engine.py`, `tests/scripts/test_spec_trace.py`
  and `tests/scripts/test_spec_logic.py`.
- **`scripts/spec_logic_vocab.py`** (now 136 lines): `facts`, `pools`, `Vocab.guards`, `guard_id` and `AMOUNT` are
  removed. Nothing used them: S3 did not use `AMOUNT`. The docstring now names `grammar/check.lp`, the domain facts
  with `initial/3`, and `spec_facts.define`, in place of `background.lp` and `spec_logic.definition`. `Vocab.define`'s
  docstring says the Def literals stand in for the condition (design-r3 §3.2), not "its rule derives it".
- **telingo unpinned:**
  - `scripts/tools_grammar.py`: `WHEELS = {"pgf": "1.1", "clingo": "5.8.2"}`, `WITHOUT` without telingo, and the
    docstrings changed to match;
  - the docstrings of `scripts/tools`;
  - `tests/toolchain.py`: `WHEELS = ("pgf", "clingo")`;
  - `tests/scripts/test_tools.py:80` and `tests/scripts/test_tools_grammar.py`: telingo removed from the expected
    lists and the pip logs.
- **`scripts/model.lp`**: one comment named telingo as the requirement language's checker. It now names
  `model logic`. This is an extra edit, outside the plan's file list, made so that no tracked script names telingo.
- **`CLAUDE.md` rows:**
  - `grammar/`: `check.lp` replaces `background.lp` and `cone.lp`;
  - the `spec_logic.py`/`spec_logic_np.py` row is removed (the `spec_facts` row stays);
  - `spec_logic_vocab.py`: "`domain`, the domain facts for `grammar/check.lp` (kinds, sub-kinds, actors, values,
    transitions, `initial/3`)";
  - the `spec_engine.py` and `spec_trace.py` rows are removed;
  - `spec_solve.py`: "facts → `check.lp` → findings, L1-L5";
  - `tools_grammar.py`: "pgf and clingo".
- **New test:** `test_tools_grammar.py::GrammarTest::test_nothing_imports_telingo_or_the_old_solver`, as the plan
  gives it. It uses `re.MULTILINE` rather than `re.M`, because ruff's FURB167 flags the alias.

## Test runs

- The new test, before the change: FAIL (0.46 s).
- `timeout 600 python3 -m pytest -q -n 4 tests/scripts --ignore=…test_spec_guarantees.py
  --ignore=…test_revision_done.py --ignore=…test_features_generate.py`: 501 passed and 1 skipped, plus 125 subtests,
  in 17.7 s. The ignores for the deleted files are dropped.
  - `test_e2e_codified` took 11.4 s, which is over the ceiling. It was over before this task, and S8 owns it.
- `test_features_generate.py`, `test_tools_grammar.py` and `test_tools.py`, run separately: 35 passed and 1 skipped
  in 7.1 s.
- `python3 scripts/tools size --limit 300`: exit 0.
- `python3 scripts/tools check scripts tests`: vulture reports "clean", so no dead code is left in
  `spec_logic_vocab.py`. Ruff's remaining hits are all in files this task did not touch.
- `git grep "spec_engine\|spec_trace\b\|spec_logic\b\|spec_logic_np\|background.lp\|cone.lp" -- scripts tests
  CLAUDE.md`: the only hits are negative assertions, in `test_spec_solve.py`, `test_features_generate.py` and the new
  test.
- Every `scripts/*.py` has a module-map row. This was checked inline, because `test_revision_done` is still ignored.

## Left open

- `README.md`, `docs/capability-format.md`, `docs/design-model/*.md` and
  `skills/checking-spec-consistency/SKILL.md` still describe telingo. That is S9's task.
- `tests/scripts/test_revision_done.py:75` still has a docstring about telingo's horizon. S8 rewrites it.
- `$SLOW` now has to ignore only `test_spec_guarantees`, `test_revision_done` and `tests/scenarios/test_supervision`.
  The other test files it ignored are either deleted or rewritten.
