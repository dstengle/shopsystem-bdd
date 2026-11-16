---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-41/review-1
kind: review
batch: batch-41
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/63
head: c0b2a60058e88da83e179d14bead75afa0f24c33
range: ec5e40c17bede23d6621e1061b6ad0a3f3b88a67..c0b2a60058e88da83e179d14bead75afa0f24c33
result: fix-now
---

# batch-41 review 1

## Verdict

The batch builds all six lines: b65 (backlog#r43, r44), b77 (readiness#r49), b6 (batches#r40) and b286 (feature-file-tools#r131, r132). All five checks in `## Runs` exit 0, and at 635 changed lines the change is under the 1000-line limit. One finding to fix now: the batches capability's Implementation section does not cover what `work batch merged` now prints and keeps. Three observations follow.

## Findings

### f1 Minor fix now: `work batch merged` prints and keeps things neither r40 nor any Implementation section mentions
- item: b6
- where: scripts/batch_close.py:72
r40 asks for one case only: an `accepted` request whose item has a request line is resolved at the merge. The change also does two things nothing in the spec mentions:

- **A printed line.** In every other case `work batch merged` prints `<q> not resolved (<why>); run work resolve`. That covers a request that is not `accepted`, an item that records no line, and a refused resolve. `merged` also prints `<q> resolved: delivered by <item>`. `test_merged_names_a_request_it_leaves_alone` pins the first of these.
- **A new field.** The item file gains `request_lines: [<cap>#r<n>=<k>, ...]`. `work accept` writes it, and `backlog_lines.renumber` carries it to the new ids (scripts/request_accept.py:707-708, scripts/backlog_items.py:453-454).

The batches capability's Implementation section (spec/capabilities/batches.md:149-152) still describes `work batch merged` as setting the items `delivered` and the batch `merged`, removing the worktrees and deleting the branches. It says nothing about resolving the request or about what is printed. The only change to that section removed the not-yet bullet.

Fix: add a bullet to batches' `## Implementation, may change` saying three things:
- the merge resolves each request through `work resolve`'s path, each recorded line as `<cap>#r<n> <merge commit>`;
- any other request is left alone and named in the output for a later `work resolve`;
- the item records `request_lines` when `work accept` writes it.

Alternatively, drop the extra output.

### f2 Minor observation: two docs pages still show `work shape` succeeding on an idea with no note
- item: b65
- where: docs/recipes.md:158
The batch updated docs/upgrading.md:217 for r43, but two other pages still run `work shape` without `--note` on an idea that has no `## Notes`, and show it printing `shaped`:

- docs/recipes.md:158-161: `work idea "work refuse commits the item"` then `work shape b252`.
- docs/reference/capability-file.md:447-450: `work idea '`work show` prints the status too'` then `work shape b250`.

After this batch both commands are refused with `work shape: ... has no shaping note; give it one with the --note option`. test_docs only checks each `$ ` line against argparse, so it does not catch this. I read every `work shape` line under docs/, README.md and skills/. The other examples either give `--note` or shape an idea created with `--note`, so they are fine. Fix: add `--note "..."` to both `work shape` lines, or to the `work idea` before each.

### f3 Minor observation: the module map's rows of the changed modules do not name the new behaviour
- item: -
- where: CLAUDE.md:142
The batch updated the rows of readiness_bar, batch_close, backlog_items, backlog_lines and request_accept. Five rows of modules whose concern grew are unchanged:

- `scripts/backlog_moves.py`: `work shape` refusing an idea with no shaping note (r43).
- `scripts/backlog_view.py`: an idea's grooming in its "waiting on" cell (r44).
- `scripts/spec_steps4_boxes.py`: the new `bring_response`, a held thing only described with its holder brought in before the When (b286).
- `scripts/spec_lf_ordered.py`: the K the line says a collection holds becomes the order's first member (b286).
- `scripts/spec_steps4.py`: its row still says only "two Ks" are brought in before the When.

The map lists each module's concerns, so these rows are now out of date. Fix: add these behaviours to the rows.

### f4 Minor observation: the item's trace of r132 in the spec corpus names r130
- item: b286
- where: grammar/corpus/spec/feature-file-tools.md:345
The r131 block says `From: b286 r131`, but the r132 block says `From: b286 r130`. This is probably the item's id before `work batch start` renumbered it: g132 sits before g131 in spec/capabilities/feature-file-tools.md:357-361, which fits that. A reader following the trace finds no r130 among b286's lines in the brief, though. Fix: write the trace as the renumbered id, or say that it is the pre-renumber id.
