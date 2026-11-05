---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-gate-r3-l6
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: draft
---

# Gate of layer 6 (plan-r3): S12

## Merged

- gfr3/S12 (head 3a8559f3) as 4addeb18, "merge gfr3/S12 (revision 3, layer 6)". No conflicts.

Review against plan-r3 §S12 and design-r3 §2/§6: S12 may change only what a failing check needs. Its code changes
answer failing checks: `model logic` took 4.2 s against goal 6's 2 s (one grounding with an external `focus`
instead of a grounding per witness; behaviour the same, witnesses still valid models), `tools check` failed on 16
ruff findings already there, and record frontmatter gave new model-check rows. EXPECTED keyed by code and ids
follows S11's recommendation and keeps the 32 entries. Size holds; the CLAUDE.md spec_solve row was updated.

## Fixed on gf-conversion

- `tests/scripts/test_revision_done.py`: S12 inserted the `_cpu` helper between `@pytest.mark.live_logic` and
  `test_model_logic_on_the_live_spec_is_fast`, so the marker landed on the helper and the speed test (which runs
  the live solve) lost it, escaping `-m "not live_logic"` and the live_logic xdist group. Marker moved back.
- `grammar/check.lp` and `test_the_whole_context_is_one_grounding`'s docstring said the focus pair is "assumed";
  it is set with `assign_external` (S12 found assumptions UNSAT). Wording corrected.
- `report-S12.md` written from S12's notes (the harness refused it in S12's worktree).

## Results

- `python3 scripts/tools size --limit 300`: exit 0.
- `python3 scripts/tools check scripts tests`: exit 0.
- Full suite, no ignores (every old solver file rewritten by now), `python3 -m pytest -n 8 -q`, twice:
  920 passed, 1 skipped, 129 subtests, 18.8 s and 19.3 s; no test listed over the 10 s ceiling.

## Left

- Goal 6's test-seconds target (under 15) holds for the solver files alone (13.8) but not inside the full suite
  under contention (21.5).
- Two non-solver tests near the 10 s ceiling under load: the flaky-scenario test and e2e.
- An L5 text prints a raw term ("give pair(v1,n_grade)").
- logic-r3-after.json still has the old witness texts.
- S11's 7 questions, the If-exception rule, §3.2's false hits and the unread rnone are open for the person.
