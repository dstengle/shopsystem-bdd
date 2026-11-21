---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-68/review-1
kind: review
batch: batch-68
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/92
head: 51c469721dd956ae39c1281f3fbd5e8d67229037
range: ff4f537585996d291d92eb7184e450f80f1b1b19..51c469721dd956ae39c1281f3fbd5e8d67229037
result: clean
---

# batch-68 review 1

## Verdict

The batch builds all twelve of b48's lines (drafting r53-r64). Each `work line --remove-<piece>` or `--replace-<piece>` changes only the item, makes one commit, and refuses a piece the item does not hold by naming it. The scenarios check the item as committed, and the script test covers the malformed replacements. Every run exits 0 at the head. The change is 730 lines, under the 1000-line limit. Both new modules have rows in `CLAUDE.md`'s module map, and the docs are updated. No test was removed or weakened. I found nothing to fix now and three observations.

## Findings

### f1 Minor observation: a piece flag next to an option that is dispatched earlier is ignored, not refused
- item: b48
- where: scripts/backlog_cli.py:198
`cmd_line` sends a run to `backlog_capability`, `backlog_adapter`, `backlog_pack` or `backlog_model_edit` before it reaches `backlog_piece_edit`. None of those modules' shape checks knows the six new flags, so the new flag is silently dropped. Reproduction:
```
work line b1 --remove-model "object x" --remove-universal U1
```
This removes the model element and leaves U1 in place, with exit 0. The same happens next to `--capability`, `--pack` and `--expose`. `backlog_piece_edit.cmd`'s own `others` list also leaves out `retirement_list`, `no_line` and `narrator`, but those are dispatched later, so those cases are not affected. b48's own notes name this kind of fault ("ignored ... rather than refused"), but no line of the batch asks for the refusal. Hardening: add `backlog_piece_edit.FLAGS` to the other modules' `others` lists, or refuse when the flags of two modules are given together.

### f2 Minor observation: removing a universal condition that retires a live one leaves the retirement with nothing in its place
- item: b48
- where: scripts/backlog_piece_edit.py:421
`_universal` deletes the condition and leaves `blocks.universal_retired` as it is. Suppose the item wrote the condition with `--universal ... --retires universal#U3`. After `--remove-universal`, the item still retires U3, so the lay takes U3 out of `spec/universal.md` with no condition replacing it. The docstring says this is deliberate, because the block keeps no pairs. That differs from `--remove` of a requirement line, which takes the retired id out by its `retires:` pair. r53 itself is met, since the item no longer keeps the condition. A fix would refuse, or name the retirement it leaves behind, when the block's `retired:` is not empty.

### f3 Minor observation: replacing a piece with the same text gives git's refusal, not the drafting service's
- item: b48
- where: scripts/backlog_piece_edit.py:470
r59-r61 say the item keeps "a different" piece. A replacement with the same statement, entry or block leaves the item file unchanged. `shop_files.committed` then runs `git commit` with nothing to commit, so the run is refused with a git failure that does not name the piece or say why. The item is left unchanged, so no data is lost. Reproduction:
```
work line b1 --replace-universal U1 "<U1's own statement>"
```
A fix would refuse up front, naming the piece, when the new text equals the old.
