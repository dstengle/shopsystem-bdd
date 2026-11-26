---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-146/d1
kind: defect
batch: batch-146
item: b760
date: 2026-11-26
---

# batch-146 d1

Reinstating a requirement id that one of the item's own lines retires (work line <item> --remove <cap>#r<n>, the id in retired: with a pair under retires: whose line the item holds) takes the id out of retired: but keeps the pair (backlog_reword._unretiring keeps a pair whose line is the item's), so the item still holds the id against drafting#r90. Reproduce: work line b1 --retires work-queue#r1 '<line>'; work line b1 --remove work-queue#r1; the block's retires: still pairs the new line with r1.
