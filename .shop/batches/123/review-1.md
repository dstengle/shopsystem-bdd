---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-123/review-1
kind: review
batch: batch-123
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/146
head: ee9728dda816d95449ee4c09a7b2a33af636583a
range: dcfcfcf2533f9be32323b7749254108bc67502e1..ee9728dda816d95449ee4c09a7b2a33af636583a
result: fix-now
---

# batch-123 review 1

## Verdict

The batch builds b704's two lines and the CLAUDE.md row the item asks for. The take-out now works per item, so a park keeps the imports another item laid on the same driven port (r155), and an amend takes out an import that only the item's lines needed (r156). One finding to fix: on an amend the new unlay can drop an import that the port's model file held at the batch's base. All runs exited 0. The change is within the size limit.

## Findings

### f1 Important fix now: an amend drops a port's import that the batch's base held
- item: b704
- where: scripts/backlog_port.py:119
What is wrong: `work batch amend` takes the item out with no base. `batch_amend.py:112` calls `batch_start.unlay_lines(tree, [old], COMMAND)` with no `base`. The new `_unimport` then does two things wrong:
- it sets `before = []`, so the docstring's promise "unless the model file at the batch's base held it" does not apply on an amend;
- `_left` ignores the port's whole model fence, so another in-batch item's model lines in the port no longer protect an import.

Why this is new: the old code went through `backlog_area_move_unlay._imports(..., base=None)`, which judges against the model file as git last held it, so it kept such an import.

The case that fails: a port area that `spec/model/` holds at the base with `imports: [notes]` (needed by its own model lines, or by another item's model lines in its fence). An in-batch item lays a port capability in it whose line says "a note". That line is then reworded so it says no note, and `work batch amend` runs. The unlay takes `notes` out because no capability line left says a note and `before` is empty. The relay does not put it back. The batch branch and the task branch now hold a model file without an import its base held. The amend changes no model line of the base, so this is lost data and can raise v_m1 on lines the item never touched.

Fix: pass the batch's base in the amend's take-out, `batch_start.unlay_lines(tree, [old], COMMAND, batch_parked.base_of(root, batch))`, as park and review already do. r156 still holds with a base: `registry` imported nothing at the base, so `tracking` is still taken out. Then correct the docstrings and the CLAUDE.md row so they no longer say "an amend (no base)". Add a unit case in tests/scripts/test_backlog_port.py where a base-held import survives an unlay.

What I checked: `backlog_lines.unlay` removes the item's capability files and model lines before `backlog_port.unlay`, so `_left` reads only what is left. `batch_parked.py:61,93` and `batch_review.py:108` pass `base_of(...)`; `batch_amend.py:112` does not.

### f2 Minor observation: `_left` reads only requirement lines, not a capability's terms or relations
- item: -
- where: scripts/backlog_port.py:103
`_left` keeps only the lines of a capability file that start with `- [r`. If a word of the imported layer appears only in another capability's `## Terms` or `## Relations` in the port area, an unlay takes the import out. Today v_m1 reads the words of parsed lines only, so nothing breaks yet. The risk is if the check ever reads term or relation rows too.
