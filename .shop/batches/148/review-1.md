---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-148/review-1
kind: review
batch: batch-148
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/171
head: 7902de545bf58e76bf9003f6ba6852fb15500cc4
range: 5ba3754d516f3a7ecbe6bcda0f714ff5e5fa6eba..7902de545bf58e76bf9003f6ba6852fb15500cc4
result: clean
---

# batch-148 review 1

## Verdict

The batch builds all three lines of b764 (batches#r190, r191, r192), and it changes `laying_handlers_model_then`'s Then dispatch as the item's notes ask. No laying check was lost in that change. There is nothing to fix now; two minor points are recorded.

For each of the three new scenarios, `work batch start` runs on an item whose group and requirement ids collide with its capability's (`colliding` sets them to `g1` and `r1`). The Thens then read the batch's branch:
- **The line was renumbered:** `renumbered` checks that the item's line appears once under an id other than `r1`, and that the capability still holds its own `r1`.
- **r190:** the `household` pack term is under `spec/packs/household.md`'s `## Glossary`.
- **r191:** the item's table `o1` is in `spec/adapters/cli.toml`, and the contract has exactly one `[operations."notes.archive"]`. The world wrote a different table `o2` there beforehand, so this checks that the item's table replaced it.
- **r192:** `the person` is held once in notes' layer and is gone from shared's.

The other checks:
- `unbuilt:` is empty on the branch.
- The new handler is 144 lines.
- `CLAUDE.md` has a module-map row for it, and the row for `laying_handlers_model_then` is updated.
- The feature was generated (`features generate --check` exits 0), and every run exits 0, as at the base.
- The size is 316+25 changed lines, under the 1000 limit.
- No judgement decision is touched.

The risk in the `laying_handlers_model_then` change was that a laying scenario could lose a check it used to run. I compared every Then of g28 to g41 in `features/laying.feature` with the new `THENS` table. Each scenario still has at least one Then that runs its full check:
- g28 and g31: `holds (adapter contract, operation table)` → `_contract`.
- g29: `does not keep the operation table` → `_withheld`.
- g30: `has (operation, operation table)` → `_contract`, in its g30 branch.
- g32 to g35: `holds (model, model line)`, `keep model line` and the negated `domain model` holds → `_restated`.
- g36 to g38: `holds (area, …)` and `keep area` → `_moved`.
- g39 to g41: the negated holds and `keep area` → `_retired`.

The only Thens that now merely read their file are the plain `keeps the adapter contract` and `keeps the domain model`. Each sits beside a Then of its scenario that runs the full check, so this is not a weakened test.

## Findings

### f1 Minor observation: the new handler accepts any Given of its groups without checking it
- item: b764
- where: tests/scenarios/batches_handlers_renumbered.py:263
`given` returns None for every Given step of g190 to g192, so the step passes, while the world is built separately by `build` before `work batch start`. A Given added to one of these groups later, or one whose wording changes, would pass silently without the world matching it. The item makes `then` refuse a Then it does not know for exactly this reason. This holds no merge today, because every Given in the three generated scenarios is one that `build` writes. Hardening: let `given` take only the template and kinds those scenarios say, and refuse any other.

### f2 Minor drop: KEEPS is copied in the new handler
- item: -
- where: tests/scenarios/batches_handlers_renumbered.py:206
The new handler keeps its own copy of the keep verbs ("requested.py's"), while `laying_handlers_model_then` reads `L.KEEPS`. If the list in one place changes, the copies drift apart. Polish: read the shared list instead of copying it.
