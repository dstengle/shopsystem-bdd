---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-154/review-1
kind: review
batch: batch-154
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/177
head: f951539d4e6f986474e6ba0647abc06b67e1ec3b
range: 23f131d61cf3068c1f17bef9d065d2baae218264..f951539d4e6f986474e6ba0647abc06b67e1ec3b
result: fix-now
---

# batch-154 review 1

## Verdict

All three items build their requirement lines, and the generated features match `features generate`. Two things hold the merge. The `tools check` run now fails on a blind `except Exception` that b801 added. The module map was not updated for the batch's new modules, or for the modules whose behaviour changed.

## Findings

### f1 Important fix now: `tools check` fails at Head on b801's blind exception (BLE001)
- item: b801
- where: scripts/backlog_lines.py:281
The run `python3 scripts/tools check --base 23f131d61...` exits 1 at Head and 0 at the base:

```
== ruff ==
scripts/backlog_lines.py:281:12: BLE001 Do not catch blind exception: `Exception`
Found 1 error.
```

`warn_terms` wraps the copy, the lay and both lexicon reads in `except Exception: found = set()`. This also hides a real bug in the warning path: a NameError, a wrong argument to `lay_onto`, or a change to the shape of the problem tuple would make r94's warning disappear without a sound, and only the r94 scenario would catch it. Fix: catch only the failures a lay onto the copy can raise (`Refused`, `OSError`, the grammar's `GrammarError` if the lexicon read can raise it) and let anything else propagate. `tools check` should then exit 0.

### f2 Minor fix now: no module-map row for b801's new handler module, and backlog_lines' row not updated
- item: b801
- where: CLAUDE.md:1
CLAUDE.md's module map is binding: "A new concern gets a new module and a row here." The batch adds `tests/scenarios/drafting_handlers_actor.py` (drafting r94's world: the actor `the initiative` written with `work line --term`) and gives it no row. The `scripts/backlog_lines.py` row does not mention `warn_terms`: the v_t6 warning that `work line --term` prints on stderr after laying the item on a temporary copy of `spec/`. Since `grammar/rules.md` now says v_t6 is implemented in `scripts/backlog_lines.py`, that row should say so too. Fix: add the new row and extend the backlog_lines row.

### f3 Minor fix now: no module-map row for b802's new handler module, and migrate_init's row not updated
- item: b802
- where: CLAUDE.md:1
The batch adds `tests/scenarios/upgrades_handlers_branch.py` (upgrades r46: founding on `master`) and gives it no row. The `scripts/upgrades/migrate_init.py` row does not mention the new behaviour: a founding on a branch other than the base branch `main` warns on stderr, naming the branch, and still founds. The `migration_tools_handlers.py` change (every migrate scenario's repository is now renamed with `git branch -M`, to `main` by default) is not described anywhere either. Fix: add the row and extend migrate_init's row.

### f4 Minor fix now: product_layer, product_assign and product_assign_cli rows do not describe b798's refusals
- item: b798
- where: CLAUDE.md:1
These rows no longer say what the code does:
- `scripts/product_layer.py` lists the job refusals, but not the two new ones: a statement whose actor the product does not hold (r42), and a statement whose actor is not one of the job's `--actor`s (r43).
- `scripts/product_assign.py` says only that a product actor the product does not hold is refused. It now also refuses an id out of the context id form (r41) and, in this bounded context, an actor its domain model does not hold (r40).
- `scripts/product_assign_cli.py` does not mention `here`, which reads this context's id and its model's actors.

Fix: update the three rows.

### f5 Minor observation: product#r5's scenario now passes through r42's check, not the actor check
- item: b798
- where: tests/scenarios/product_handlers.py:800
In r5's scenario (the job's actor is not the product's, and no statement is given), the handler now writes the default statement so that it mentions `the p1 user` (`mentioned` falls back to the When's actor). The new check at `scripts/product_layer.py:451` (r42) therefore refuses first, naming `--actor`.

I verified that for a single `--actor` the loop `for actor in actors: if actor not in product["actors"]` can no longer be reached. Reaching it needs the statement's actor to be in the product and to equal the job's actor, so that actor is in the product as well. Deleting the loop would not fail r5's scenario. The behaviour r5 states still holds, because r42's refusal names the same option, so this is not a lost guarantee. But r5 no longer tests its own code, which goes against the handler's own rule ("so that only what the line says is wrong"). A unit case with two `--actor`s, one outside the product, would cover the loop again.

### f6 Minor observation: `spec plays` in a context with no domain model refuses every actor, and one whose index gives no id refuses for an unrelated reason
- item: b798
- where: scripts/product_assign_cli.py:408
`here()` returns this context's id and `set(domain_model.load(root).actors)` whenever `spec/index.md` exists. In a context with no `spec/model/` (its actors defined in the glossary), the set is empty. A mapping with `--in` set to its own id is then refused with "it holds no actor", whatever actor is given.

Separately, `shop_files.context_path` raises `Refused` when the index gives no `bounded-context/...` id. Every `spec plays` there is refused with that message, even with `--in` naming another context. No line names either case, and today's clients are all domain-model contexts. A guard would fix both: no check unless `spec/model/` exists, and `None` on an index with no id.

### f7 Minor observation: r94's warning misses a v_t6 problem the spec already had
- item: b801
- where: scripts/backlog_lines.py:341
`found = _v_t6(copy) - before` keeps only the problems the lay adds. Suppose the spec already has a v_t6 problem for a word, for example an actor in another layer that already reads as a kind, and the term written repeats that word. Then the same (code, term, message) tuple is in `before`, and no warning is printed, although the term written violates v_t6. To reproduce: write `--term` with an actor entry whose word an existing v_t6 problem already names. Nothing is printed. No client today hits this.
