# Gate, round 1: q21 (i55)

Drafts: `.shop/scratch/17-integrate/drafts/round-1/spec/capabilities/work-queue.md`. Every other accepted line and answer is already in `spec/` (requests r50-r58, r64; supervision r184-r186, r212, r213; work-queue r47, r59-r61); only the work-queue answer (r23 retired for the line with the capability-proposal condition) is not held.

## work-queue (retired gains r23)

Removed:
- [r23] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`.

Added:
- [r62] **When** a `work` command's change makes it true that an initiative has at least one work-item that is `green`, that every work-item of it is `green` or `withdrawn`, that every capability-proposal of it is `formulated` or `withdrawn` and that every request kept in this context whose asker is this context and that names the initiative is `delivered`, that command shall set the initiative's status to `done`. (answer 2026-10-29: "retire work-queue r23 ... in its place")

Implementation line "r23: a request names the initiative..." becomes "r62: ..." (no Behaviour change).

## Glossary
No entry added, changed or removed.

## Decisions
None.

## Questions
None.
