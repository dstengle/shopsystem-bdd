---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-file-set-is-the-claim
summary: "A work-item's file set, found by its researcher and finalised by its planner, is its claim: implementers whose sets are disjoint work at once, each in its own worktree; no count of modules is refused, and a dispatch still touches at most 15 files."
date: 2026-10-19
status: proposed
supersedes: design-decision/slice-budget-refused-by-plan
source: "initiative/i10; docs/design-model/design-model.md v3 section 3, the work-item; measurement/kb-batches-32-35 (Lands exceeded in 15 of 23 slices)"
---

# 0041. The file set is the claim

## Decision

The file set names every file the work-item changes. `work run` never runs two implementers whose sets share a
path. Each implementer works in `.shop/worktrees/<work-item>/` on a branch from the initiative branch's head; `work
run` rebases it, tests it there and merges it fast-forward. A file the implementer finds it needs is claimed with
`work claim`, which refuses one a claimed item holds; the implementer then stops, and the item waits. Where a
worktree needs its own environment, `delivery.toml`'s `[worktree] setup` command makes it. Sizing scouts and the
Lands line go; the implementer's 15-file dispatch budget and `PARTIAL` stay.
