---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-173/review-1
kind: review
batch: batch-173
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/195
head: 7dfc41c72dfc52d578e1f510b4eb05535e646215
range: 4229d7ab7f5f5e4a2d684554ea85cf193b8cda5f..7dfc41c72dfc52d578e1f510b4eb05535e646215
result: fix-now
---

# batch-173 review 1

## Verdict

The batch builds applying#r1-r25. It moves the laying handlers of the retired laying lines to applying handlers whose When calls spec_apply's `apply`, retires laying's lines in `retired:`, and updates the module map. Two Minor findings to fix now, both test changes made during the move: one loosens an assertion and one gives a scenario a world in which its "exactly once" check can no longer fail. There is also a size observation.

## Findings

### f1 Minor fix now: applying's operation-table Then no longer checks the table's command or positional parameter
- item: b872
- where: tests/scenarios/applying_handlers_model_then.py:31
The old laying Then (g28/g31) checked that the whole table text `M.table("o1")` (its `command = "notes archive"`, `positional = 1` and `example = "o1"`) is in the contract. The new `_contract` only checks the parameter's `example == "o1"` and that the header appears once. The comment says the apply annotates the table, which explains why the exact-text match broke. But the replacement dropped the checks on `command` and `positional`, so a table applied with the wrong command or parameter kind would now pass g10 and g13. That loosens an assertion. Fix: read the table with `tomllib` as the new code does, and also assert `["command"] == "notes archive"` and `parameters["note"]["positional"] == 1`.

### f2 Minor fix now: g13's world no longer holds a table to replace, so "holds the table once" cannot fail
- item: b872
- where: tests/scenarios/applying_handlers_model.py:72
Laying's g31, which this group replaces, ran on the domain-model fixture. That fixture's `spec/adapters/cli.toml` already holds `[operations."notes.archive"]` (line 39), so `count(...) == 1` checked that the item's table took the old one's place. The new `_tabled` gives g13 a contract of only `[programs]`, so the count is 1 whatever the apply does with an existing table. Dropping the fixture is needed: the work-queue line does not read under the request pack, and the apply now checks it. But batches_handlers_renumbered's g191, cited for this world, writes a contract that already holds `M.table("o2")`. Fix: write `'[programs]\nnotes = "notes.py"\n\n%s\n' % table("o2")` as g191 does, so g13 still shows the item's table replacing the one held.

### f3 Minor observation: the change is over the review size limit
- item: b872
- where: -
`## Size` gives 20 files, +1250 -1198, against a limit of 1000 changed lines. Most of it is b872 moving 25 lines from laying to applying. That brings in the regenerated `features/applying.feature` (+331) and `grammar/corpus/spec/applying.md` (+438) and removes their laying counterparts (about -660 in `features/laying.feature` and `grammar/corpus/spec/laying.md`). The handlers are mostly renames. The hand-written code that needed review was about 230 new lines (`applying_handlers.py`, `applying_handlers_areas.py`) plus the edits to the renamed modules.
