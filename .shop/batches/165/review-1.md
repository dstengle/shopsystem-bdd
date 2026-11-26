---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-165/review-1
kind: review
batch: batch-165
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/188
head: 86e9bbd944739bace5694092d9f9234f96dbe9d8
range: 377b9bc2e3fc5efeefc67bb393749cf8827d8c07..86e9bbd944739bace5694092d9f9234f96dbe9d8
result: fix-now
---

# batch-165 review 1

## Verdict

All four items are built and each new line has its generated scenario. Two findings need fixing before the merge: a lint failure in b848's change and a missed case in b850's lay. Two more are observations that do not hold the merge.

## Findings

### f1 Minor fix now: tools check fails on the import b848 adds to backlog_model_edit
- item: b848
- where: scripts/backlog_model_edit.py:229
The check exits 1 at the head and exited 0 at the base. Its output:
```
== ruff ==
scripts/backlog_model_edit.py:229:9: I001 [*] Import block is un-sorted or un-formatted
Found 1 error.
```
The failing line is the function-local `import backlog_lines        # the warnings --term prints (b848, drafting r112)` placed after the `print(...)` in `cmd`. Fix: format the import so ruff accepts it, for example with `ruff check --fix`, or by moving it to the module's imports or beside the other local import at the top of `cmd`.

### f2 Important fix now: a capability laid in an area whose service the item's own model lines declare still specifies `service <capability>`
- item: b850
- where: scripts/backlog_capability.py:375
laying#r49 says the laid capability specifies the service of the area that holds it. It does not require that area to exist before the lay. `backlog_lines.lay_onto` lays a new capability's file first (line 200, `backlog_capability.lay`) and the item's model lines only later (line 217, `backlog_adapter_ops.lay`). So when `_service` runs, `domain_model.load(root)` cannot yet see a service the item itself declares. The risk I checked is an item that makes a new capability with `--area stock` and whose `### stock model` block declares `service inventory`. For that item `held` is empty, `_service` falls back to the capability's name, and the file says `specifies: service <capability>` rather than `service inventory`. That is a wrong answer in a state the line covers. The g49 scenario passes only because its area `notes` and its service already exist in the fixture. Fix: write `specifies:` after the model lines are laid, or read the service from the item's model block for the capability's area as well as from the model on disk.

### f3 Minor observation: an area of several services, none named after the capability, specifies the first one
- item: b850
- where: scripts/backlog_capability.py:386
`held[0]` picks whichever service the model lists first when the area declares more than one and none is named after the capability. The line says "the service of the area", which assumes there is one. No current fixture has an area with two services, so nothing exercises this. Naming the choice, or refusing the lay, would make the result predictable.

### f4 Minor observation: model_product's module-map row does not list the new rule
- item: b849
- where: CLAUDE.md:208
The change adds `w_unplayed_actor` to model.lp, and model_product.py's docstring now names it among the rules its facts feed. The `scripts/model_product.py` row of CLAUDE.md's module map still lists only v_job_elsewhere through w_unserved_cap. Fix: add `w_unplayed_actor (b849)` to that row.
