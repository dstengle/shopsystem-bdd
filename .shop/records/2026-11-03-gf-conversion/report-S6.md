---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-gf-conversion-report-s6
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-04
status: done
---

# Report S6: Gherkin from the facts

## What changed

- `scripts/spec_trace_steps.py` was moved with `git mv` to `scripts/spec_steps.py` (233 lines).
  - `Reader`, `LETTERS`, `TraceError` and the helpers are unchanged and still importable from it.
  - It gains `read(facts, logic, steps)`, which applies the rules of design-r3 §5 in the order the plan gives.
- `scripts/spec_steps_facts.py` (new, 130 lines) turns one requirement's facts into the atoms `Reader` reads:
  - `own`: the first way through a split requirement, less the literals of a defined condition's definition;
  - `instances`: a role as `o(K,V)`, a named code as its string, and a later requirement's role as the first
    requirement's role of the same kind and rank;
  - `fluent`, `trigger`, `response`: one fact each;
  - `contrast`: the extra instance for an `every` role.

  It is a separate module because `spec_steps.py` would otherwise go over 300 lines.
- `scripts/features_generate.py` (96 lines) is rewritten.
  - It no longer has `context()`, `spec_solve`, `spec_trace` or multiprocessing.
  - `scenario_text(v, ctx, cap, group)` reads `spec_context.load`'s `facts`.
  - A requirement in `ctx.refused` raises `GenerateError("<cap>#<rid>: <refusal>")`.
- `scripts/spec_trace.py` now imports `Reader` from `spec_steps`, so it still imports until S7 deletes it.
- `CLAUDE.md`: the `spec_trace_steps.py` row is now `spec_steps.py` with `spec_steps_facts.py`. The
  `features_generate.py` row says "read off their facts by `spec_steps`, with no solver".
- `tests/scripts/test_spec_steps.py` (new, 13 tests) uses the generation fixture copied to `tmp_path` and grown per
  test. It covers the plan's ten tests, plus:
  - the negative-response rule;
  - a defined condition worded once;
  - a split requirement.
- `tests/scripts/test_features_generate.py`: every fixture test is kept, with the expected texts updated:
  - g2 of `WORK_QUEUE` is now `Given an initiative i1` / `And … is not \`proposed\``;
  - `G1` is a list of lines checked in order. The Then from r2 (`interleaves`) follows them, and no `i3` appears;
  - the renamed test is `test_an_if_group_states_the_restriction_it_excludes`;
  - `test_byte_stable_under_two_hash_seeds` and `test_generation_imports_no_solver` are added.

  This file is off `$SLOW` from now on.
- `tests/scripts/fixtures/generate/e2e/work_queue_handlers.py.in`: the toy world now gives a thing with no stated
  status the default status `` `none` `` instead of `None`.
  - g2 now introduces the initiative with `Given an initiative i1` and no value, which the old handler could not
    print.
  - This follows design §10: the fix goes in the world.

## Test runs

- Before the implementation, `test_spec_steps.py` failed with `No module named 'spec_steps'`.
- `timeout 600 python3 -m pytest -q -n 4 tests/scripts/test_spec_steps.py tests/scripts/test_features_generate.py tests/scripts/test_supervise_formulate.py tests/scripts/test_features_vocab.py --durations=5`
  gives 65 passed in 7.4 s.
  - The slowest test is `test_check_on_the_live_repo_runs_to_its_end`, at 6.0 s. It now has no solver.
  - Every other test takes under 0.5 s.
- `python3 scripts/tools size --limit 300` exits 0.
- `ruff check` passes on the changed files.
- **Live spec, generation only:** `features generate --check` takes 6.2 s and exits 1.
  - It prints `differs` for 5 files: analysis-tools, design-model-check, requests, supervision and work-queue.
  - stderr is empty. Every group has a scenario, so there are no warnings.
  - `--preview spec/capabilities/supervision.md` under `PYTHONHASHSEED=1` and `=2` gives identical bytes, with 80
    scenarios as before.
- Not run: `test_e2e_codified.py` (S8 owns it) and the old solver tests.

## Calls made (design intent over the letter)

1. **A defined condition is one Given, not its definition.** S3 emits a positive `ccond` of a `Def` condition
   followed by its definition's literals. `own` drops those literals by translating the definition again, over each
   way through it, with the same role count.
   - Without this, "an initiative that is open" would also say "is not `done`" and "is not `abandoned`".
   - The scenario states the requirement's own words, as revision 2 did.
2. **The object restrictions of a negative response are not Thens.** For example, r27 says "`work run` shall not
   start a stage for the work-item".
   - Read literally, rule 3 gives "does not start the stage s1" followed by "the stage s1 is for the work-item w1".
     The second line asserts a stage that does not exist.
   - Only "does not start the stage s1" is kept. `oattr`/`orel` follow positive responses only.
3. **A contrast for a defined-condition restriction.** "every open work-item" has a `ccond` and, after call 1, no
   `cond`. Its contrast is another work-item with the condition negated: "a work-item w2" / "the work-item w2 is not
   open". The plan names only the `cond` case. Without this, `every` over a condition would get no contrast.
4. **A contrast's Given** comes after every pre-state Given, including for a later requirement's `every`. Its `does
   not` Thens are one for each positive `resp` of that requirement whose object is the role. They come after that
   requirement's Thens. A positive `set` response gives "the K x is not `v`".
5. **`only(R,I,K)` gives no Then.** S3's fact carries neither the event nor the other object, so "give the stage only
   a brief" cannot be worded. Supervision fixture g3 is just its When.
6. **A hold response** (`resp(…,hold(Res),D,none)`) is read as the fluent `holds(D,Res)`. With an actor as doer,
   `Reader` refuses it, and the group is left out with a line on stderr. The live spec has no such case.

## For the gate and the next tasks

- **An anaphor after a response's object does not pick out that object.** This is in S3's `spec_facts`, not in S6.
  - `Walk.objects` restores the bindings after `a K`. A later "the K" is then a fresh role.
  - Example, supervision r39: "start a `branch review` stage …, give the stage a review brief …, commit the stage,
    push the commit and log the stage". It now reads as four stages, s1 to s4.
  - Example, requests r1: "write a request that is `open` and commit the request". It reads as `commits the request
    q2`.
  - Revision 2's solver could unify these, but a reading of the facts cannot. This also weakens `model logic`.
  - Suggested fix in `spec_facts_np`/`spec_facts.objects`: bind the kind to the new object after its restrictions.
    It belongs to S5's or S10's owner, because it changes facts that `check.lp` reads.
- **Speed:** `features generate --check` on the live spec takes 6.2 s against design §2's 5 s. Almost all of it is
  `spec_context.load`'s pgf parsing, which S3 measured at about 5.8 s. Generation itself is milliseconds. The
  cross-process parse cache that S3's report proposes would bring it under 5 s.
- **For S10:** the regenerated features drop revision 2's extra Givens. Examples are "the stage s1 holds a worker
  slot", "the stage s1 holds the claim" and "the work-item w1 is blocked by the work-item w1".
  - They gain negative-print Thens that were empty before, such as design-model-check g44–g46's "`model` does not
    print `v_d1`".
  - They gain contrasts by rule.
  - A relation restriction before a value restriction now gives "an initiative i1 / … part of … / the initiative i1
    is `started`" in fact order, instead of `an initiative i1 that is \`started\``.
  - The checked-in `features/` are not regenerated here. S10 does that.
