---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-105/review-1
kind: review
batch: batch-105
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/128
head: 52ad25cd9225061a17e29cf4790a11a7950d5239
range: 82eee6e2280c28b3b17ce650d49ce4415d3245f5..52ad25cd9225061a17e29cf4790a11a7950d5239
result: clean
---

# batch-105 review 1

## Verdict

The batch builds all three items. b648's `work ready` now runs the readiness bar on a renumbered in-memory copy of the item, and the item keeps its own ids. b660's renumber now keeps the adapter, pack and moves blocks. b645's `work line --capability --area` writes the block's `area:` line, and the lay places the capability in that area. Nothing needs fixing now. All runs exit 0, `features generate --check` among them. The change is within the size limit, and no test is removed or weakened. There are three observations.

## Findings

### f1 Minor observation: a refusal of `work ready` can name ids the item does not hold
- item: b648
- where: scripts/backlog_moves.py:143
`check` passes `renumbered`, a deep copy whose ids `backlog_lines.renumber` has moved past the capability's, to `readiness_bar.check`. Every reason the bar gives is said of that copy. So when an item whose ids collide fails the bar for another reason, the refusal can name `work-queue#r6` where the item file says `r5`. A person then searches the item for an id it does not hold. No line names what a refusal says here, so this is not a wrong answer. Hardening: map the reasons back through the pairs `renumber` returns before raising, or add the pairs to the message.

### f2 Minor observation: `--area` without `--capability` is silently ignored
- item: b645
- where: scripts/backlog_capability.py:70
`add_arguments` adds `--area` to every `work line` parser. Only `backlog_capability.cmd` reads it, and only on the `args.capability is not None` path (scripts/backlog_cli.py:198). So `work line b1 --into notes --area tracking "<line>"` writes the line, exits 0 and drops the area without a word. No line of the batch asks for a refusal, so this is hardening: refuse `--area` without `--capability`, naming the option, as `cmd` already refuses other pieces.

### f3 Minor observation: the module map row of backlog_capability has an unbalanced parenthesis
- item: b645
- where: CLAUDE.md:194
The new text "then `area:` when `--area` names the area it is placed in, an area of spec/model/ or a new one, b645)" closes a parenthesis that was never opened. Fix: write "(an area of spec/model/ or a new one, b645)".
