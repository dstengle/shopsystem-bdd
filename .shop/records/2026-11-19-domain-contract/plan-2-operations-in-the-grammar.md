# Plan 2 of 7: operations with parameters in the grammar, the logical form and the steps

Implementation plan for `design.md` (this folder), phase 2. Read plan 1's "The whole branch" first: the branch, the
directives, the bootstrap rule, the size limit and the module-map rule hold here too.

## Goal

A line can say a request in domain words: "When the person enters a design-decision with the tier `check`, the
decisions service shall ...", "If the person enters a design-decision without a tier, then the decisions service
shall refuse the request and name the tier". The domain-request pack replaces the CLI pack in `imports:` for a context
with `spec/model/`; grammar 4 generates an act per operation and its parameters from the model; the logical form,
the example-data reader, `features generate`'s steps and the step grammar read it. **The old run/option reading stays
beside it** (bootstrap) so the live spec, its features and every test still read as today.

## Tasks, in order

1. **`grammar/packs/request.md`** (design §4.3): request, parameter, service (Kind of: agent), reason, refuse, name,
   return, notify, complete, fail, check, keep, change, conform, start, the outcome values `done`, `returned`,
   `refused`, `passed`, `failed` of `outcome`. `grammar/packs/cli.md` gets the header `Deprecated: 0.38.0` (read only
   by plan 7's upgrade report); `grammar/packs/time.md` and `spec.md` headers say `[request, time]`, `[request, spec]`.
   `spec_vocabulary`'s v_t21 is switched on for a context with `spec/model/`.
2. **`scripts/spec_lexicon.py`** (`CORE_VERBS`, v_t6): the request pack's verbs plus hold, become, set, be for a
   context importing `request`; `{run, print, exit, ...}` kept for one importing `cli` (bootstrap).
3. **`scripts/spec_rgl_ops.py`** (new; `spec_rgl.py` calls it): per operation O of service S bound to a verb V,
   `V_O_Act : Actor -> Obj -> Params -> Event` (an object slot of O's object, or the thin frame's fixed phrase), per
   parameter `O_p_Is`, `O_p_Some`, `O_p_No`, a boolean parameter's `O_p_Flag`/`O_p_NoFlag`, `Params` an and-list
   ("without a summary and a tier": both absent). The exact GF signature is the builder's (design §11); a Params list
   only in a trigger and in a history Given (`S_Done`). `OPTION`/`k_option_SetTo` stay in `spec_rgl.py` for a `cli`
   context until plan 5.
4. **`scripts/spec_lf_request.py`** (new, beside `spec_lf_option.py`, which stays until plan 5): the form's
   `request(e, O, actor, object)`, `param(e, p, v)`, `noparam(e, p)`, its `--form` line (`show`), R2's "the request"
   bound to the trigger's request (`spec_lf_read`'s `the`; `grammar/language.md`'s R11 sentence rewritten "the
   request's own K" in plan 3). `scripts/spec_lf_clause.py`/`spec_lf_core.py` dispatch to it for an operation act.
5. **`scripts/spec_example.py`**: a value after "with the <parameter>" is example data unless a declared value of
   the parameter; no code names an operation in a `request` context.
6. **`scripts/spec_steps4.py`, `scripts/spec_steps4_boxes.py`**: the When "When the person enters the design-decision
   d1 with the tier `check`" from `request(...)` and its params, the Givens of things a parameter names; the Thens of
   the pack's verbs (refuse with its names, return, complete, fail, notify, keep). `spec_steps4.py` is at 298 lines:
   the request's step building goes into `scripts/spec_steps4_request.py`.
7. **`scripts/spec_rgl_steps.py`** and `grammar/Steps4.gf`/`Steps4Eng.gf` if needed: a request step per operation
   with its params (the step grammar reads what `spec_steps4` writes).
8. **`scripts/features_vocab4.py`**: `WhenRequests` (Call with `operation`, `params` each with its value or None,
   `without`) when the verb names an operation, else `WhenHappens`; `ThenReturns`/`ThenReturnsNot`, `ThenRefuses`
   (with its names), `ThenCompletes`, `ThenFails`, `ThenNotifies`, `ThenKeeps`; `ThenChangesNothing` stays.
   `WhenRuns`, `ThenPrints`, `ThenExitsErr`, `ThenExitsOk` stay for a `cli` context (bootstrap). Split into
   `features_vocab4_request.py` if it passes 300.
9. **`scripts/model_constructs_table.py`**: construct #12 becomes `request-params` (its example a request with two
   parameters, read in a `request` context); the old #12 kept under a bootstrap code until plan 5. `python3
   scripts/model constructs --write` regenerates `grammar/constructs.md` and `grammar/corpus/constructs/`.
10. **Fixtures re-spelled into the new forms**: `tests/scripts/fixtures/codified-2/` and `codified-2-time/` get
    `spec/model/`, `spec/vocabulary/`, `imports: [request]` (time: `[request, time]`) and lines in request words;
    `tests/scenarios/codified2_world.py`'s `LINES`, `REQUIREMENTS`, `UNIVERSAL`, `GENERATED` and
    `codified2_constructs.py`, `codified2_given.py` follow. The inline "runs \`" lines of `tests/scripts/` that read
    through these fixtures are rewritten into request words. **Session's call**: a test that exercises only the old
    run/option reading is kept and listed in a module-level `BOOTSTRAP = True` marker comment, so plan 5 can find and
    delete it (`grep -rln "BOOTSTRAP = True" tests`).

## Tests to write first

- `tests/scripts/test_spec_rgl_ops.py`: the generated functions for the domain-model fixture's operations (an object
  slot, a fixed object, a valued, a some, a no, a flag parameter); "without a X and a Y" parses to both absent.
- `tests/scripts/test_spec_lf_request.py`: the form and `--form` line of a request with two parameters, one absent;
  "the request" bound to the trigger's; a value outside the parameter's values left for v_m2 (plan 3).
- `tests/scripts/test_spec_steps4_request.py`: the When and Givens written for a request; the step grammar reads them
  back (`features_vocab4` gives `WhenRequests` with the operation and params).
- A request-pack case in `tests/scripts/test_spec_lexicon*.py` (v_t6) and in `test_spec_vocabulary.py` (v_t21).
- `features generate` on the domain-model fixture (with one request line added) writes a feature whose steps all read.

## Exit check

```
python3 scripts/tools size --limit 300
python3 scripts/model check                      # as at plan 1's exit
python3 scripts/model logic                      # = baseline-logic.txt
python3 scripts/features generate --check && python3 scripts/features vocab --check   # live features byte-identical
python3 scripts/model rules --check && python3 scripts/model forms --check && python3 scripts/model constructs --check
python3 -m pytest                                # the full suite green
```

Nothing is skipped or xfailed. A test of `model logic` or the entailment check on the re-spelled codified-2 fixture
whose expected findings need plan 3's facts may be marked `xfail(strict=True, reason="plan 3: request facts")`; each
one is listed in this phase's last commit message and plan 3 removes every such mark.
