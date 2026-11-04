---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s11
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# S11: the clashes the new check finds in the live spec (design-r3 §9 call 6)

The harness refused this report in the task's worktree (as it did for S10); the layer 5 gate wrote it from the task's
notes. Branch `gfr3/S11`, head f56f165a, reset to gf-conversion 96b1f209 before any work.

## Live runs

| Run | Time | Findings | Saved |
|---|---|---|---|
| first | 18.0 s | 174 L1, 6 L5; no L0, L2, L3, L4 | `logic-r3.json` |
| after the fixes | 4.3 s | 32 L1, 6 L5 | `logic-r3-after.json` |

Where the time goes: loading the context 0.9 s, the brave solve 0.14 s; the rest is one focused normal solve per L1
pair in `spec_solve._clashes` (about 0.1 s each, each grounding the whole program again). For S12: the 2 s target
needs that changed, for example ground once with the focus as an external.

## Call 1: three misreadings of the check, fixed in `grammar/check.lp` (add3b30c)

`check.lp` was not in S11's file list. These three caused 135 of the 174 L1s; each has a test in `test_check_lp.py`.

1. **A `Named` code is one thing.** The translation makes a role per mention (analysis-tools r6 has `.venv` as v1 and
   v3). The roles of one code are now canonicalised to the first, and a code both sides name must unify.
2. **The EARS `If …, then …` form (`if`, `while_if`, `where_if`) is the exception on its trigger.** It is never paired
   with a non-`if` requirement; two `if` lines, or two normal lines, still are. This cleared 127 pairs (for example
   batch-measurement r1 against r2-r6 and r10). Design §4's "no live line needs an exception form" was wrong: the spec
   states its exceptions as `If` lines. **The person may overturn this**: it hides any true clash between a refusal
   and a normal line, by design.
3. **"Do E and change nothing" changes nothing but E.** A requirement's own events are excepted from its own change
   nothing, and from the other's when the other names the same event. Nine lines say "show/write a reason … and
   change nothing". `changing/1` is deleted.

## Call 2: six spec edits, one commit each

Each edited line parses, its feature was regenerated, and its scenario test passes.

| Requirement | Edit | Clears |
|---|---|---|
| analysis-tools#r7 | "While no analysis tool is `missing`, …"; "and the Python interpreter" dropped (r1-r6 say which is printed) | r7/r8, r6/r7 |
| supervision#r15 | "and the work-item branch is not flaky" | r15/r20 |
| supervision#r2 | "no remote is unpushable" | r2/r33 |
| supervision#r39 | "no remote is unpushable" | r34/r39 |
| supervision#r79 | "no result is awaited" | r60/r79 |
| supervision#r67 | "While a session is not faulty, when the session ends …" | r67/r78 |

## Call 3: the 32 L1s left are questions

Each is in `tests/scripts/conftest.py` `EXPECTED`, keyed by the exact finding text, mapping to one of 7 questions.

| Question | Findings | Ids | The question |
|---|---|---|---|
| Q_STAGE | 2 | batch-measurement r8/r14, r12/r13 | `include` is measurement-wide, the intent is per stage: say it per stage, or drop the negative Then? |
| Q_RELEASE | 3 | migration-tools r13-r16 | a repository's version conditions are opaque prose, not tied to one repository: define its release in the controlled language? |
| Q_LINES | 3 | requests r20-r22 | "every line settled" needs `no K is not C`, which `spec_facts` refuses: allow it, or reword? |
| Q_CLOSED | 4 | supervision r26 against r27, r28, r29, r34 | should r26 say "no work-item open" and yield to r29/r34; should the check expand a Def under `no`? |
| Q_ONE | 13 | supervision r39/r40, r39/r41, r71/r72, r76/r77; work-queue r20-r24 | a condition's noun phrase is not tied to the trigger's: one per trigger, and how is that said? |
| Q_RESULT | 6 | supervision r42/r43, r46/r47, r57/r61, r57/r63, r62/r63, r73/r76 | `stage with result` and `stage for node` have no cardinality one in the facts |
| Q_COMPLETE | 1 | work-queue r5/r7 | `complete`'s "every" is not expanded |

## Listed, not edited

- 6 L5 warnings: review#r5; spec-migration#r10; U4 twice (commit, push); U7 (red-green#r7 reacts); U8.
- No L3 or L4 findings in either run. S10 left no items needing a spec change.

## Where the design is wrong against the code

- §3.2 says opaque prose conditions are "sound, no false hits". For this check it is the reverse: an opaque condition
  never refutes a merged pre-state, so it gives false hits and misses nothing.
- `rnone` is emitted by `spec_facts` but nothing in `check.lp` reads it.

## Test runs

- `pytest -n 4 tests/scripts/test_check_lp.py`: 29 passed, 0.6 s (the 3 new tests fail against the old check.lp).
- `pytest -n 4 -m "not live_logic"` over test_spec_solve, test_spec_facts, test_supervise_outputs, test_e2e_codified,
  test_model_output: 85 passed, 6.7 s.
- After each spec edit, that capability's scenario test: analysis-tools 33 passed; supervision 80 passed (~13.5 s).
- `features generate --check`: exit 0. `features vocab --check`: OK.
- `pytest -n 4 tests/scenarios`: 283 passed, 19.5 s.
- `pytest -n 0 -m live_logic test_revision_done test_spec_guarantees -k "not fast"`: 12 passed, 4.3 s; every finding
  left is in `EXPECTED`.
- `pytest -n 4 -m "not live_logic"` over the logic and generate test files: 204 passed, 8.9 s.
- `tools size --limit 300`: exit 0. `ruff check` on the changed files: clean.
- Not run: the full suite; `test_model_logic_on_the_live_spec_is_fast` fails at 4.3 s against its 2 s limit (S12's).

## For S12

- `test_model_logic_on_the_live_spec_is_fast` fails (4.3 s).
- The `EXPECTED` keys include the witness pre-state text, so they break when an unrelated fact changes the first
  model. A key by ids would be sturdier.
