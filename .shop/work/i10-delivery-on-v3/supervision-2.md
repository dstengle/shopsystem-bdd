---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/supervision-2
kind: work-item
part_of: capability-proposal/delivery-on-v3-supervision
status: withdrawn
wkind: capability
under: supervision
accepts: [supervision#r8-r15, supervision#r28]
blocked_by: [work-item/supervision-1]
risk: concurrency
---

# supervision-2

## Observable
A ready item's implementer works in its own worktree; on DONE the branch is rebased, tested there and merged
fast-forward, or the item goes to awaiting-ruling; PARTIAL continues; a refused claim sends the item back to ready.

## Unknown
How a worktree gets a working environment in a consuming Python project (`[worktree] setup`), and whether the
suite's interpreter resolves the worktree's sources rather than the main checkout's (an editable install points at
the main checkout).

## What goes green
supervision#r8-r15, r28, in a fixture git repository with a small pytest project, the stub claude committing in the
worktree as its script says.

## Files, roughly
`scripts/supervise.py` (implementer stage, worktrees, rebase, test, merge, suite record), `scripts/work`,
`.gitignore` (`.shop/worktrees/`, `.shop/scratch/`), step definitions; delivery.toml reading (the `[tests]` and
`[worktree]` tables) in `scripts/workqueue.py` or a small `scripts/delivery_config.py`.

## Notes
Driven with `$SHOPSYSTEM_WORK_CLAUDE` pointing at `tests/scripts/stub_claude.py` (from supervision-1), so no model runs.

Withdrawn 2026-10-19: folded into work-item/supervision-1, the skeleton (initiative notes)
