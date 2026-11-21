---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-65/review-1
kind: review
batch: batch-65
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/89
head: fa889afde983f54d2949f6b447037900f93b7509
range: 919bdaeb6d928240e217c0826e24d3110f5885f8..fa889afde983f54d2949f6b447037900f93b7509
result: fix-now
---

# batch-65 review 1

## Verdict

The batch builds the lines of b472 (drafting#r51, r52, batches#r95), and the chores of b471 and b476 meet their checks. Every run exits 0, and the change is under the size limit (+702 -36, against 1000 changed lines). There is one finding to fix: a test assertion that b472 loosened. The others are observations.

## Findings

### f1 Minor fix now: test_json_is_one_object loosens its kinds assertion from == to <=
- item: b472
- where: tests/scripts/test_model_forms.py:72
Commit 4ae78d544 changes this assertion:
```
assert {f["kind"] for f in forms} == {"command", "item", "hand"}
```
to:
```
assert {f["kind"] for f in forms} <= {"command", "item", "hand"}
```
The `<=` passes on any subset, including an empty set or `{"command"}`, so the test no longer catches a form whose kind is wrongly worked out. In the tree, `model_forms.FORMS` has no writer left that resolves to `hand`. It still has forms of kind `command` and forms of kind `item` (b398's and b475's "plugin item ... (no command yet)" rows). So the exact set is known. Fix: assert `== {"command", "item"}`. This keeps the check exact and records that the term pack, the last form written by hand, now has its command.

### f2 Minor observation: a docstring's blank lines are kept in the item but still dropped once the block is laid into a capability
- item: b476
- where: scripts/spec_read_given.py:44
The risk: f4 is meant to keep a docstring given block's blank lines. b476 keeps them in `backlog_forms.given_block` and in the item reader (`backlog_section._Reader.given`). I checked whether they survive the lay. They do not: `spec_read_given.GivenLines.given_line` still skips every blank line inside a ```given fence (`elif not line.strip(): return`). So a blank line written by the item and laid into `spec/capabilities/<cap>.md` is dropped again when spec_read reads the file, and the docstring in the generated scenario loses it. The chore's files do not include spec_read_given.py, so the chore is met as written. If the blank line should reach the scenario, an item should carry the fix through to the spec reader.

### f3 Minor observation: work line --pack ignores --group and --in instead of refusing them
- item: b472
- where: scripts/backlog_cli.py:221
`cmd_line` sends `--pack` to `backlog_pack.cmd` before `backlog_forms.refuse_beside` runs. `backlog_pack.cmd` refuses `--into`, `--retires` and the other pieces, but not `--group` or `--in`. So `work line b1 --pack household --term "<entry>" --group X` succeeds and drops `--group` without a word. This is the kind of gap b476's f5 closes for the other pieces. Reproduction: run that command on a shaped item; it exits 0 and the item has no group X. Fix: call `refuse_beside(args, "pack")` in `backlog_pack.cmd`, or check `args.group` and `args.in_group` there.

### f4 Minor observation: the pack unlay can leave an import it added and lists files it did not change
- item: b472
- where: scripts/backlog_pack.py:522
Two edge cases in `unlay`:
- **Import left behind.** Suppose `spec/packs/<name>.md` exists before the lay but `spec/index.md` does not import it. `lay` adds the import. `unlay` only removes the import when it deletes a pack the lay made, so the import stays after a park or a review unlay. The index then differs from the base, and no item's line asked for that.
- **Unchanged files listed.** `unlay` appends the pack's path to `files` whenever the file exists, even when none of the block's terms was in it, so callers may stage a file that did not change.

Neither case comes up in today's scenarios. Fix: record in `lay` whether the import was added and undo that in `unlay`, and append the path only when the text changed.

### f5 Minor observation: the batches pack handler indexes the step's parts before checking it is its own step
- item: b472
- where: tests/scenarios/batches_handlers_pack.py:876
`keeps` is registered for seven ThenDoes verbs (`write`, `commit`, `post`, `keep`, `make`, `rewrite`, `publish`) on both the backlog and batches features. It evaluates `parts(step)[1][0]` before `step.context.get("packing")`. A Then of one of those verbs with fewer than two things, in any scenario that reaches this chain first, would raise IndexError instead of returning False. The suite passes today, so no current step hits it. Fix: check `packing` first, then `len(parts(step)) > 1`. Separately, the "in the lay's commit" check only finds the last commit on the branch that touched the file, which may not be the lay's commit.
