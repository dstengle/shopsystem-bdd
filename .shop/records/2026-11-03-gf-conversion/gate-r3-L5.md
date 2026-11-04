---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-gate-r3-l5
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Revision 3, layer 5 gate

The gate passed on `gf-conversion`, apart from the speed acceptance test that is S12's. Base 96b1f209.

## Merged

- `gfr3/S11` (head f56f165a), `--no-ff`, no conflicts. Its report was refused by the harness; the gate wrote
  `report-S11.md` from the task's notes.

## Review

- **Outside the file list.** S11 changed `grammar/check.lp`, which the plan does not list for S11. Accepted: the three
  changes are misreadings of the check, not of the spec (135 of 174 L1s), each is pinned by a test in
  `test_check_lp.py` that fails against the old encoding, and the plan's intent (findings cleared or named) needs
  them. The Named-code canonicalisation and the "change nothing but its own events" rule follow design-r3 §3 and the
  spec's wording directly.
- **The `If` exception (check.lp change 2) is a judgement call for the person.** It makes every EARS
  unwanted-behaviour line win over the normal lines on its trigger, so a true clash between a refusal and a normal
  line is hidden by design. It contradicts design §4's claim that no live line needs an exception form; the spec's
  practice shows that claim was wrong. Kept, and named as the first open question in the report.
- **Spec edits.** Six, each a dropped condition or a missing exception, ids kept (unreleased codified spec), one
  commit each with the plan's message form, features regenerated. Within design §9 call 6.
- **`EXPECTED`.** 32 entries, 7 question constants, each in `report-S11.md`. Keys are full finding texts including
  the witness pre-state, so they are brittle to unrelated fact changes (left for S12).
- Size and module map: no new module; `test_check_lp.py` 286 lines, `conftest.py` 153; every file within 300.

## Fixed by the gate

Nothing beyond writing `report-S11.md`.

## Runs on gf-conversion after the merge

- `python3 scripts/tools size --limit 300`: exit 0.
- `timeout 600 python3 -m pytest -n 8 -q` (the full suite, `live_logic` included): 918 passed, 1 skipped, 129
  subtests, 1 failed, 27.7 s. The failure is `test_revision_done.py::test_model_logic_on_the_live_spec_is_fast`
  (4.1 s against 2 s), the speed acceptance that is S12's task; not caused by the merge.
- `timeout 600 python3 -m pytest -n 8 -q -m "not fixture and not live_logic"`: 906 passed, 1 skipped, 21.4 s.
- `python3 scripts/features generate --check`: exit 0. `features vocab --check`: OK. `ruff check` on the changed
  files: clean.
- Slowest: the speed test 8.2 s (two live runs), e2e 6.5 s; nothing over 10 s.

## Left for S12 and the person

- The live check takes ~4 s; the time is one focused re-grounding solve per L1 pair in `spec_solve._clashes`.
- The 7 questions of `report-S11.md` and the `If`-exception rule.
- Design §3.2 is wrong about opaque conditions (they give false hits here); `rnone` is emitted but unread by
  `check.lp`.
