---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s4
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Report S4: `grammar/check.lp`, the fixed meta-encoding

Written by the layer 1 gate from the task's result, because the harness refused the subagent's write of this file.

## What changed

- `grammar/check.lp` (new, 164 lines): candidate pairs, the `map/4` unification, the two states, L1 clashes,
  L3 `bad_set`, L4 `unreachable`, L5 `lint`, and `pre/6` under `focus(A,B)`.
- `tests/scripts/test_check_lp.py` (new, 259 lines, 26 tests), on inline facts in the r3 schema.

## Test runs

- `pytest -q -n 2 tests/scripts/test_check_lp.py --durations=5`: 26 passed in about 0.6 s; slowest 0.04 s.
- All the example's requirements ground to 972 rules; ground plus solve take 4 ms. They show exactly
  `clash(r2,r53,pos_neg)`, `clash(r52,r72,neg_pos)`, `clash(r16,r99,set)` and `bad_set(r98,t_status,v_drafted,v_done)`.
- Mutation check: each key rule commented out in turn ("no K is v", the state-1 reading, trigger unification,
  restriction entailment, the untriggered and use candidate rows, self, focus) made at least one test fail.
- `tools size --limit 300` exits 0; ruff clean. The live spec was not solved.

## Calls made (S5 needs these)

1. **Soft pair failures.** The pre-state, trigger and "no K is v" failures derive `out(A,B)` under the current
   unification, and `clash` needs `ok(A,B)`; as hard constraints, one pair that can never fire together would make
   the whole program UNSAT and hide every other finding. Only constraints on `map` stay hard (injectivity, named
   codes, object `oattr`); leaving a role unmapped always satisfies them. Pinned by
   `test_a_pair_that_cannot_fire_hides_no_other_finding`. The `focus` constraint is still hard, so S5 should focus
   only on pairs that the brave solve reported.
2. **Candidate filter `can(A,B)`:** a pair is a candidate only if its responses could clash (opposite polarities of
   one event, two values set of one attribute, exit_ok with exit_error, change_nothing with a changing response, a
   use with a nouse). Every clash rule needs one of these, so nothing is lost.
3. **A fourth index row** pairs `uses` with `nouse`, which the design's three rows never pair.
4. **A U** is an id between `"U"` and `"V"` (`universal/1` derived in check.lp); capability names are lower case.
5. **Two states:** a triggered side at state 0; an untriggered side paired with a triggered one at state 1 (state 0
   with the triggered side's sets, plus frame); at state 1 only the untriggered side's conditions are checked, since
   two sets of one attribute are `clash(…,set)`; two untriggered sides both at state 0; `ccond`, `crel`,
   `holds`/`free` and `cnone` stateless.
6. **Object restrictions:** `pos_neg` needs B's object restrictions entailed by A's, `neg_pos` the reverse; both
   objects must unify through `map`.
7. **L3 with no pre-value:** `bad_set(R,A,none,To)` when no transition enters To. An attribute with no `trans` gives
   no L3 and no L4.
8. **Doers:** `any` matches any doer; otherwise the same constant, or roles the unification merges.
9. **L5:** an event is any response except `set(…)` and `change_nothing`; print, exit_* and hold count, so U4 and U8
   will be linted. "Reacts to E" is a requirement whose `trig` event is E.
10. **Self** also covers a requirement demanding a positive and a negative response of one event, doer and object.
11. **`pre/6`** names A's instances as they are and B's unmerged instances as `b(Y)`.

## Open

- Brave enumeration on the live spec is unmeasured until S5, S11 and S12; `can` is the main guard.
- Two untriggered requirements not involving a U are never paired (no design row); one more `cand` row if S11 finds
  the gap matters.
- check.lp is 164 lines against the plan's "about 150".
- S3's facts `onot`, `ocond`, `rnone`, `named`, `disj(Split,Base)`, `count`, `only`, `every`, `feat` are not read
  by check.lp; unread facts give no warnings, but S5 should decide whether `rnone`/`onot`/`ocond` must reach the
  rules. The CLAUDE.md `grammar/` row is left for S7.
