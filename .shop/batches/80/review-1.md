---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-80/review-1
kind: review
batch: batch-80
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/104
head: e4956254bc509cf154e78efa1524544e469e729f
range: 69f2455914ff1c4664e68476a783078e4c298ee4..e4956254bc509cf154e78efa1524544e469e729f
result: fix-now
---

# batch-80 review 1

## Verdict

The batch builds all five lines of b543: parsing#r23 and r24, consistency#r36, and checking#r71 and r72. All runs exit 0, as they do at the base. The change is 592 changed lines, under the 1000 limit. Two findings need fixing now. First, a response's request skips the one-thing rule of design-decision 0111. Second, the new `% pass` examples in `scripts/model.lp` hide the original passing examples of v_m4 and v_m7. Three findings are observations.

## Findings

### f1 Important fix now: a response's request takes a plural object, against design-decision 0111
- item: b543
- where: scripts/spec_one_thing.py:42
Design-decision 0111 (a-request-acts-on-one-thing) says the object slot of a request, a verb naming an operation, takes one thing's noun phrase. b543 makes a response's act of such a verb with its parameters a request. The new fun is `<D>_ActReq_<S>` over the same `q_<verb>_<n>_<m>` tree, and `request(e, O, ...)` in the form. But `plural` only treats a tree as a request below `_Event` or `_Request`:
```python
trigger = trigger or tree[0].endswith(("_Event", "_Request"))
```
The `q_` tree under `_ActReq_` is never checked. So "the notes service shall add every note with a text" parses as one request on every note. In a trigger the same request is dropped and refused. The docstring is now stale too: it still says "A response's act of such a verb is no request (spec_lf_request) and keeps its plurals". That is true now only of an act with no parameters.

Fix:
- Also treat a tree whose fun holds `_ActReq_` as a request in `plural`.
- Fix the docstring and the module-map row of `scripts/spec_one_thing.py`.
- Add a case to tests/scripts for the refusal of a plural response request.

### f2 Minor fix now: the new `% pass` examples hide the original passing examples of v_m4 and v_m7
- item: b543
- where: scripts/model.lp:423
`model_rules` keeps one example of each kind per rule. It reads `examples.get(("pass", c))` from a dict, so the last `% pass` line wins (scripts/model_rules.py:19, 55). Adding a second `% pass` line for v_m4 (line 423) and for v_m7 (line 433) drops the original ones from what `spec rules` runs and from the catalogue. Those were `states_reason` for v_m4 and `requester` for v_m7. You can see it in grammar/rules.md: both rules' "Passes on" now show only the response-request path.

So the main ways a line meets v_m4 and v_m7 are no longer checked by the catalogue. The old lines stay in model.lp, but nothing runs them. This is a dropped case.

Fix:
- Keep the original `% pass` line as the one each rule shows.
- Test the `asks` and `on_refusal` paths in tests/scripts/test_domain_model_check.py, beside `test_v_m4_a_declared_reason_no_line_states` and `test_v_m7_an_operation_no_line_requests`. Do not use a second `% pass` comment.
- Regenerate rules.md.

### f3 Minor observation: a forbidden response request counts as a request (v_m7) and as stating reasons (v_m4)
- item: b543
- where: scripts/model_domain_lines.py:91
`response` is built with `_atoms`, which goes down into `not` boxes (scripts/model_domain_lines.py:59-66). So a `request` atom under a `not` emits `asks`. A line "the notes service shall not reserve a note with the quantity `2`" would then:
- make `requested(stock.reserve)` true, so v_m7 stays silent;
- with a refusal line on a reservation, mark every reason of `stock.reserve` stated (v_m4).

No line of the batch says anything about polarity, so this is hardening. To harden it, only emit `asks` for request atoms outside a `not` box.

### f4 Minor observation: v_m4's new path matches the refusal by object kind, not by operation
- item: b543
- where: scripts/model.lp:425
```prolog
reason_stated(O, R) :- op_reason(O, R), asks(_, O, _), op_object(O, Obj), on_refusal(_, Obj).
```
Every reason of every asked operation whose object is `Obj` counts as stated as soon as any line is triggered on a refusal of an `Obj`. That holds whoever refuses and whichever operation it was. checking#r72 says "a trigger that uses a refusal and the operation". Take two operations of one service whose object is `reservation`, say `reserve` and `extend`. One line "If the stock service refuses a reservation" then states the reasons of both. Today's scenario has one operation, so it passes.

### f5 Minor observation: a response request's parameters do not stop a false L1
- item: b543
- where: scripts/spec_lf_facts_request.py:594
`act` writes the request as its verb's `resp`, with `rparam` and `rnoparam` beside it. No rule of check.lp reads them, as the module map says ("joined by no rule yet"). So these two lines give the same `resp` and an L1 that is not real:
- "shall reserve a note with the quantity `2`"
- "shall not reserve a note with the quantity `3`"

Reproduction: put both lines on one trigger in a context with the `stock.reserve` operation and run `spec logic`. When a rule follows the request, it should key a response's request by its parameters, as a trigger's `req(O,Ps)` is keyed.
