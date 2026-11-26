---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-157/review-1
kind: review
batch: batch-157
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/180
head: 1b7c97d23bb626d61a1b99bb470f8d76b4a786d3
range: 41fc0b0ec13e48775d38f16c6c653daf4e385e78..1b7c97d23bb626d61a1b99bb470f8d76b4a786d3
result: fix-now
---

# batch-157 review 1

## Verdict

All four items are built, but there are five findings to fix before merge. b808's handler fails `tools check` (ruff B020), and the lay-only filter also leaves out v_a6, which no line asks for. b813's r62 reads as though the job has a product actor, and its handler checks something else under that Then. The module map was not updated for the changes to product_layer and product_assign.

## Findings

### f1 Important fix now: tools check fails on the b808 scenario handler (ruff B020, PLR1704)
- item: b808
- where: tests/scenarios/checking_handlers_item.py:95
`python3 scripts/tools check --base 41fc0b0ec` exits 1 at Head and 0 at the base:
```
tests/scenarios/checking_handlers_item.py:95:14: B020 Loop control variable `text` overrides iterable it iterates
tests/scenarios/checking_handlers_item.py:95:14: PLR1704 Redefining argument with the local name `text`
```
`build(repo, text=ITEM)` now takes a parameter named `text`, and the loop `for rel, text in (... (".shop/backlog/b1.md", text))` rebinds that same name. The code still works because the tuple is built before the loop starts, but the batch's own check fails. Fix: rename the parameter (for example `item_text`) or the loop variable (for example `body`).

### f2 Minor fix now: `spec check --item` also leaves out v_a6, which no line of b808 asks for
- item: b808
- where: scripts/spec_preview.py:25
`SKIPPED_RULES = {"v_s3": 0, "v_a5": 1, "v_a6": 1}`, and `lay_only` also drops v_a6 of each id the item retires. checking#r153 names only v_s3 and checking#r154 names only v_a5. checking.md has no Implementation section that gives v_a6, and the item's notes speak only of v_s3 and v_a5. So a v_a6 the check used to report is now hidden with no requirement behind it. Fix: either take v_a6 out of `SKIPPED_RULES`, `lay_only`, the module docstring, the module-map row and docs/reference/commands.md, or add a line for v_a6 to b808 with `work line` and `work batch amend`.

### f3 Important fix now: r62 reads as the job's product actor, and its handler asserts the opposite of its Then
- item: b813
- where: tests/scenarios/product_handlers.py:1002
The corpus form of product#r62 binds "the product actor" in the response to the image of the job:
```
  response [x6: product actor]
    refuse(e2, subject: x4, object: x5)
    of(x6, x2)
    name(e3, subject: x4, object: x6)
```
The line says the job has no product actor, yet the response says the service names the job's product actor. The generated scenario therefore ends with `And the job j1 has the product actor p1`. The new handler takes that step (`step.term in ("name", "has") and unsaid(...)`) and asserts that the job is kept nowhere, which is not what the step says. This is a test that asserts something other than its step, sitting on a line whose reading contradicts itself. Fix: reword r62 so that "the product actor" reads as the request's parameter (the request pack's `the p` noun phrase of kind `parameter`), and check with `spec parse --form` that the response has no `of(x6, x2)`. Then write the handler so it asserts only what the regenerated Thens say.

### f4 Minor fix now: module-map rows of product_layer and product_assign describe the behaviour before b813
- item: b813
- where: CLAUDE.md:270
The `scripts/product_layer.py` row still lists the statement checks first and cites product r43, which b813 retires. It says nothing of the new first check: a job with no product actor, or with one the product does not hold, is refused naming the product actor (r62, r60). The `scripts/product_assign.py` row still cites product r40, which is retired by r61, and does not say that the product actor is now checked before the actor. CLAUDE.md's module map is binding. Fix: update both rows to r60-r62, b813.

### f5 Minor fix now: module-map row of product_assign does not include the refusal of a job outside the product
- item: b809
- where: CLAUDE.md:271
`assign` now refuses a job the product does not declare, naming the job (product#r59, reason `job outside the product`). The `scripts/product_assign.py` row of the module map still lists only the refusal of a job a bounded context already holds. Fix: add the r59 refusal to the row.

### f6 Minor observation: no scenario covers a job statement whose situation holds a comma any more
- item: b813
- where: features/product.feature:133
The removed scenario of the retired r14 was the only one with the given block "When a change is wanted, reviewed and agreed, the developer wants it specified, so they can build it." Retiring r14 is intended, but the comma case of `conforms` is no longer driven by any scenario, since r44 covers only a one-word situation. A later line, or a script test of `product_layer.conforms` with a comma, would restore it.

### f7 Minor observation: a positional's metavar with a space reads like two positionals in usage
- item: b807
- where: scripts/product_assign_cli.py:41
With `metavar="product actor"`, argparse prints `spec plays [-h] product actor --in ...`, which a reader can take as two positionals; `spec obtain` and `spec drop context` read the same way with `bounded context`. test_cli_spelling allows this because it checks only for underscores and upper case. A form such as `<product actor>` would keep the refusal's words and read as one argument.
