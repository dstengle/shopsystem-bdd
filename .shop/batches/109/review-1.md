---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-109/review-1
kind: review
batch: batch-109
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/132
head: ee6f8f0fc8e22d721bdbb26f63dc9aea0a1918ac
range: f8738dc9913bb56ac53938f259970469e38b9f8d..ee6f8f0fc8e22d721bdbb26f63dc9aea0a1918ac
result: clean
---

# batch-109 review 1

## Verdict

The batch builds both items. b604's `acted` turns a response's act of a verb naming an operation, with no parameters, into an `asks` fact. b605's `_done` keeps a set inside a `not` box out of `sets` and `sets_from_any`. Each scenario's world fails before its fix and is handled by the item's handlers. The module map has a row for each change and for the new handler file. Every run exits 0, as it does at the base, and the change is well under the size limit. No test is removed or weakened, and `features generate --check` passes. I found nothing to fix now; two observations are recorded.

## Findings

### f1 Minor observation: a forbidden act of an operation's verb counts as asking for it
- item: b604
- where: scripts/model_domain_lines.py:116
`acted` is given `response`, which `_atoms` builds by walking into `not` boxes. So a line saying "the notes service shall not archive the note" now gives `asks(Q, "notes.archive", ...)`. In model.lp, `requested(O) :- asks(_, O, _)` and `core_asks(O)` then treat the operation as requested. That can hide v_m7, and on a port operation v_pb1, for an operation that only a "shall not" names.

This is the same mistake b605 fixes for sets in the same `facts` method, a few lines further down (`done = ... _done(p.body)`). The `asks` of a request atom with parameters (b543) has walked into `not` boxes since before this batch. b604 extends that to every act with no parameters. I checked model.lp: lines 498 and 522-549 read `asks` with no polarity, while spec_lf_facts_request's `asked` writes the act's polarity into `resp`.

No line of the batch names a negated request. The cheap hardening is to give both `acted` and the b543 loop the atoms of `_done` in place of `response`.

### f2 Minor observation: `acted` does not check that the context imports the request pack
- item: b604
- where: scripts/model_domain_lines.py:137
The docstring says `acted` reads the act "which spec_lf_facts keys `req(O,())`". But spec_lf_facts_request's `operated` counts such an act as a request only when `walk.ids.request` is set, that is, when the context imports the request pack. `acted` makes `asks` from any verb whose lexicon entry names an operation, whatever the imports.

So in a context with a domain model that does not import the request pack, model.lp and check.lp would disagree about whether the act is a request. No client sends such a context today: v_t21 pushes a context with a domain model to import `request`. This is recorded only for consistency.
