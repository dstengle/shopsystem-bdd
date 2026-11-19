# Plan 3 of 7: operations in the logic check, the entailment check and the model checks

Implementation plan for `design.md` (this folder), phase 3. Read plan 1's "The whole branch" first.

## Goal

The check's facts, `grammar/check.lp`, `grammar/entail.lp` and the findings read a request (operation, actor,
parameter set) and the pack's response verbs; ids name qualified model elements, never words; the model checks that
need a line's facts (v_m2-v_m7) are in `model check`; the grammar's documents and corpora are rewritten in request
words. The old run/option facts and the refuse bridge stay for a `cli` context until plan 5 (bootstrap).

## Tasks, in order

1. **`scripts/spec_lf_ids.py`**: in a context with `spec/model/`, ids are model elements qualified by area
   (`specification.finding`, `decisions.enter`), read through the vocabulary of the line's area (design §5.3);
   words in a context without it, as today.
2. **`scripts/spec_lf_facts.py`, `scripts/spec_lf_facts_atoms.py`**: a `request(...)` act gives `trig(R, I, req(O,
   Actor))`, `param(R, I, P, V)`, `noparam(R, I, P)`; the pack's verbs give `resp(R, I, Pol, refused|returned|kept|
   done|failed|notified, D, X)` and `names(R, I, Thing)` (§5.2 table, §5.3). The `run`/`exit`/`print` branch kept for
   a `cli` context. `spec_lf_facts.py` is at 228: the request translation goes into `scripts/spec_lf_facts_request.py`.
3. **`grammar/check.lp`**: a trigger's equality over (operation, parameter set); a parameter absent in one line and
   given in another: two triggers; L3 reads the model's lifecycles (`scripts/spec_logic_vocab.py` reads transitions,
   kinds, values and `akind` from `Model` when it exists). The header rule kept.
4. **`grammar/entail.lp`, `scripts/spec_entail.py`, `scripts/spec_entail_rules.py`**: in a `request` context refuse
   is primitive and every refusal fires the refusal premises; `refuse_defined` and the bridge rule kept only for a
   `cli` context (deleted in plan 5).
5. **`scripts/spec_findings.py`, `scripts/model_explain.py`**: the outcome kind in place of the exit kind, worded
   with the vocabulary.
6. **`scripts/model.lp`** with its facts (`scripts/model_spec.py`, split as needed): v_m2 (a parameter the operation
   does not declare, a value outside its values), v_m3 (a requester the operation's actors exclude), v_m4 (a declared
   `refused:` reason no line states, matched by the reason's first noun, session's call §5.5), w_m5 (a transition no
   line causes), v_m6 (a set by a transition the lifecycle does not allow, today's L3 promoted through the logic
   facts), v_m7 (an operation no line requests); examples under each; `python3 scripts/model rules --write`.
7. **Grammar documents and corpora rewritten in request words** (design §9.4: rewrites, not touch-ups):
   `grammar/language.md` (107 "runs \`"; R11 "the request's own K"), `grammar/corpus/core-4.txt` (66),
   `grammar/corpus/time-4.txt` (12), `grammar/corpus/refused.txt` (5); `tests/scripts/test_spec_lf_read.py`,
   `test_spec_grammar4.py`, `test_spec_lf_time.py` follow (they read through the plan-2 fixtures).
8. Remove every `xfail(... "plan 3: request facts")` mark plan 2 listed.

## Tests to write first

- `tests/scripts/test_spec_lf_facts_request.py`: the facts of a request with params and noparams; a refusal with
  names; ids qualified by area; two areas' one word never unifying.
- `tests/scripts/test_check_requests.py` (logic check on the codified-2 fixture): an L1 between two lines on one
  operation and parameter set; no L1 when one line gives a parameter the other leaves absent; L3 from a model
  lifecycle.
- An entailment case: a refusal line's Then entailed by U17's request-words counterpart in the fixture (L8), with no
  bridge.
- `tests/scripts/test_domain_model_check.py` gains v_m2, v_m3, v_m4, w_m5, v_m6, v_m7, each caught on a broken copy of
  the fixture and the fixture clean.

## Exit check

```
python3 scripts/tools size --limit 300
python3 scripts/model check                      # as at plan 1's exit (the new rules apply to no live line yet)
python3 scripts/model logic                      # = baseline-logic.txt
python3 scripts/features generate --check && python3 scripts/features vocab --check
python3 scripts/model rules --check && python3 scripts/model forms --check && python3 scripts/model constructs --check
python3 -m pytest                                # the full suite green, no xfail left from plan 2
```
