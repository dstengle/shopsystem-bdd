---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-81/review-1
kind: review
batch: batch-81
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/105
head: 2bd5c388f4ab9493940807b9b389b5160475142c
range: b1e82c0d98838a65d9007457995a099c3922f000..2bd5c388f4ab9493940807b9b389b5160475142c
result: fix-now
---

# batch-81 review 1

## Verdict

b545 builds r38 and r39 and passes their scenarios, but r37 is only built when the request is word for word the one the governing line is triggered on. One `fix now` finding on b545 and one observation.

## Findings

### f1 Important fix now: the chain follows a request only to lines on exactly the same key, not to every line that governs the operation
- item: b545
- where: scripts/spec_entail_chain.py:424
r37 says that while a requirement requests an operation and *another requirement that governs the operation* has a consequence that a line on the first trigger states, `spec logic` shall return `L8` and every requirement that governs the operation. The chain does not follow "governs". It follows a trigger with exactly the same key `req(O,Ps)`, parameter set included:

```
level = {M for e in events for kind in (("req", "does") if k else ("req",)) for M in by_trig.get((kind, e), ())
```

The stratum C rules do the same. `_body` rewrites the premise's trigger `ev(Q,kind,E,...)` to `evC(Q,k-1,E,...,S)` with the same `E`, so `grammar/entail.lp` joins only on that exact key.

A requirement governs an operation when its trigger requests it (adapter_annotate's `governing`, which `spec/adapters/cli.toml`'s `requirements` lists are built from). That relation is about the operation, not the key. Two cases fall through:
- "When the decisions service publishes a design-decision, the registry shall keep the design-decision." governs `publish`, but its key `req(publish,())` is not the response's `req(publish,(p(summary,"s1"),))`. So r1 (REQUESTING) beside it and r3 (ENTAILED's keep) gives no L8, though r37's precondition holds.
- A governing line that names a different parameter than the response does is missed the same way.

The scenario world `design_model_check_worlds_chain.py` passes only because KEEPING, NOTIFYING and NAMING all repeat "with the summary `s1`" word for word. Decision 0118 asks that each request the adapter makes be followed to the provider's lines. Provider lines rarely repeat the adapter's parameter values, so exact matching leaves the check doing nothing in most real cases.

Fix: fire a chain line when its trigger requests the same operation and each parameter its key names is given the same value in the request's key, a line with fewer parameters included. Do this both in `chained` and in the `evC` join (for example, a `covers(E_line, E_request)` relation written per pair of keys). Add a row to the chain world whose governing line has no parameter.

### f2 Important observation: a response request with parameters no longer clashes with a forbidden act of the same verb said without parameters
- item: b545
- where: scripts/spec_lf_facts_request.py:641
Since 3ec678f5f, `act` writes a response's request as a `resp` whose event is the key `req(O,Ps)`. A response act of the same verb with no parameters is still read as a plain event (spec_lf_request: "one with none keeps its event atom"), so spec_lf_facts' `act` writes the verb's own event id. On one trigger these two lines are now two different acts:

```
When the person enters a design-decision, the decisions service shall publish the design-decision with the summary `s1`.
When the person enters a design-decision, the decisions service shall not publish the design-decision.
```

So `spec logic` gives no L1. Before this batch both lines were `resp` of the verb's event, and the L1 was found. r39 asks only that different codes not clash, and no line of the batch names this case, so it is recorded here, not held. Reproduction: put the two lines above in the request context of `design_model_check_worlds_chain.py` and run `spec logic`: it prints no L1. Fix when picked up: key a response act of an operation verb as a request even with no parameters, so that `req(O,())` is checked against the parameterised keys under the same rule as the finding above.
