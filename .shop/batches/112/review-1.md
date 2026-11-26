---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-112/review-1
kind: review
batch: batch-112
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/135
head: 40313bb40ba8ff101373dcd3eb8cbab6eef839c3
range: f7ef0a76cda159677fe329a78a5b1338c4cc33b0..40313bb40ba8ff101373dcd3eb8cbab6eef839c3
result: clean
---

# batch-112 review 1

## Verdict

The batch builds both items. b675's `spec assign` and `spec plays` keep the job, or the product actor with the actor it is called by, under the bounded context in the product file, in one commit. They refuse a job some bounded context already holds, naming the job (r22, r23), and a product actor the product does not hold, naming it (r24, r25). b644's `spec trace` returns:
- the lines of the groups whose `serves:` names the job (r26);
- the lines that the serving lines' requests reach through spec_entail_chain's `triggers` and `fired`, up to DEPTH hops (r27);
- the adapter specs under `adapters/*/` whose `realises:` names a port line in the trace (r28);
- the traces of the jobs it needs, joined (r29).

It refuses a job no group serves, naming the job (r30). Every run exits 0 at head and at base. `features generate --check` is clean, so no scenario was written by hand. No test is removed or weakened. The four new modules have rows in the module map, and each file stays under 300 lines. The change is +885 -6, under the 1000-line limit. What I found is three observations and no finding that holds the merge.

## Findings

### f1 Minor observation: the assign Then of a refusal does not check that nothing was committed
- item: b675
- where: tests/scenarios/product_handlers_assign.py:848
The module docstring and the item's notes say a refusal is "an error exit, nothing committed, the value named". The `name` branch of `then` only checks a non-zero exit and that the value is named:
```python
if step.term == "name":
    assert done.returncode != 0 and value(w, name) in said, said
    return None
```
It does not compare HEAD with `step.context["head"]`, and it does not rule out a usage error. product_handlers_trace's `then_does` checks both. A `spec assign` that wrote the product file and then failed would pass r23's scenario. Fix: assert the exit is 1, that `usage:` is not in the output, and that `git rev-parse HEAD` still equals `step.context["head"]`, as the trace handler does.

### f2 Minor observation: `assign` does not check that the bounded context serves the job, though the docs and the module map say it does
- item: b675
- where: scripts/product_assign.py:354
The docstring, the module-map row and `docs/reference/commands.md` all say a job is assigned "to the one bounded context whose capabilities serve it". `assign` checks only that no bounded context holds the job yet. It keeps any job id under any bounded-context id, including one the product does not hold (`held.get(context, {})` makes a new entry with no `addresses`) and a job that is no job of the product. No line of b675 asks for these refusals; the item's note puts the refusal of an unknown bounded context in b677. So this is hardening, but the docs claim more than the code does. Reproduction: in a product with no contexts, `spec assign nojob --to example.org/zzz` exits 0 and writes `[contexts."example.org/zzz"]` with `jobs = ["nojob"]`. Fix: reword the docs to say "assigns a job to a bounded context" until b677 adds the refusals.

### f3 Minor observation: the trace follows only the requests a line's response makes, not the operation its trigger requests
- item: b644
- where: scripts/product_trace.py:499
`reached` starts from `f["resp"]` events of the form `req(...)` alone. Suppose a serving line is triggered on a request of operation O and does not ask for O again in its response. Then other lines governing O, such as a refusal of the same request in another group, are not in the trace. The risk I checked was whether r27 is built wrong. The vocabulary's `use` ("a thing draws on another") could also cover a line's trigger. But b644's technical call says "every line reached through the requests they make", so the build matches the item's intent. Recorded for b637 and the product check, which read the trace: an entry-point group's sibling refusal lines are not in it.
