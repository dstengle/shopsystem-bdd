---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s5
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# S5: `model logic` on facts and `check.lp`

Written by the layer-2 gate from S5's result: the harness refused the subagent's write of this file, as it did for
S2 and S4. Branch `gfr3/S5`, head ea5afb63, reset to gf-conversion f626b7f4 before any work (the worktree started
at main 96818f71).

## Changed

- `scripts/spec_solve.py` rewritten (157 lines). It loads the context with `spec_context.load` and builds one
  program from the domain, every statement's facts and `check.lp`. It runs one brave `solve`, reads the findings,
  then adds L2. `solve(program, limit, brave=True)` uses `async_` and `wait(limit)`. `ERRORS = ("L0","L1","L3")`
  and `LIMIT = 20.0`. The `groups=` parameter is gone. `_order`, `_key`, `l2` and `report` are kept. The module
  imports none of spec_engine, spec_logic or spec_trace.
- `scripts/spec_findings.py` is new (162 lines). It holds the words of the findings: an L1's trigger, merged
  pre-state and why, and the L3, L4 and L5 texts. It is split out to keep spec_solve at 200 lines or fewer, and it
  has a CLAUDE.md row. The spec_solve row is rewritten.
- `grammar/check.lp`: one line, which makes `hold(Res)` stative.
- `tests/scripts/test_spec_solve.py` is rewritten with 27 tests. They cover:
  - the cluster;
  - one seeded pair for each clash kind (pos_neg, set, exit, change, use), and a seeded "no K is v" pair;
  - a requirement that contradicts itself, and L5 naming a requirement that reacts to the event;
  - extra drafts, and a draft of a live capability (Review Focus 2);
  - an empty context (Review Focus 3);
  - the time limit and L0;
  - the number of Control builds (1 + number of L1), and timing;
  - the report tests.

  The `_seed` test, which solved the live spec, is gone.

## Calls

1. **One L1 per pair of requirements.** Split pairs of the same two requirements are one finding with one focused
   solve. If they clash in several ways, the whys are joined with " and ". A pair whose two sides are splits of one
   requirement is reported as self.
2. **`hold` is no longer linted by L5.** Design §3.1 limits L5 to an event, "not a state", and the cluster had 5
   such lines. print and exit are still linted, so U4 and U8 will show as L5 on the live spec.
3. **Wording.**
   - L1: `<A> and #<B> clash: on "<trigger>" with <pre-state>, <why>`. B is written in full when it is in another
     capability. The "on" part is left out when neither side has a trigger, and the "with" part when the pre-state
     is empty.
   - L5: `<R> obliges <doer> to <event> <object> in every state[; T reacts to it]`.
4. **L0 is kept under a capability filter** when that capability exists. The partial findings are the brave atoms
   of the last model found.
5. **A focused solve** builds one new Control per L1 pair, and only for pairs the brave solve showed.

## Tests

- Before the rewrite: 19 failed, 8 passed.
- After: `timeout 600 python3 -m pytest -q -n 4 tests/scripts/test_spec_solve.py tests/scripts/test_check_lp.py
  tests/scripts/test_model_output.py tests/scripts/test_spec_facts.py` gave 92 passed in 1.67 s. The slowest test
  took 0.80 s.
- Size: exit 0. ruff: clean.
- Smoke run: `scripts/model --root tests/scripts/fixtures/logic/cluster logic` printed one each of L1 to L5 and
  exited 1.

## Open

- The live spec was not solved. S11 will measure its L1 and L5 findings and the cost of the focused solves. Each
  focused solve grounds the whole program again; if that proves slow, use an `#external focus/2` on one Control.
- `spec_context._once` and the parse cost were not touched.
