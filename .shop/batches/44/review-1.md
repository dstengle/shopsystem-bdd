---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-44/review-1
kind: review
batch: batch-44
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/67
head: add4f211ceb99c7842182fc638f7b7d82cb5c9a5
range: aad56240e26d1254c09eca55b34f71a0f98fa4c1..add4f211ceb99c7842182fc638f7b7d82cb5c9a5
result: fix-now
---

# batch-44 review 1

## Verdict

The batch builds the requirement lines of all four items (b20, b315, b316, b317). Every run exits 0, as it did at the base. I found one thing to fix now: b316 adds visible behaviour that no line asks for and no Implementation section records. The other findings are observations, plus the size, which is over the limit.

## Findings

### f1 Minor fix now: b316's chore behaviour beyond its lines is in no Implementation section
- item: b316
- where: scripts/backlog_chore.py:211
b316 adds behaviour you can see that no line of the batch asks for, and that no Implementation section names:
- `work chore` refuses a `--file` under `spec/`, `features/` or `.shop/`, or outside the repository (`_path`).
- Run again, `work chore` replaces the chore.
- The readiness bar gives the reason "it holds a chore and requirement lines" (`unlined`).
- `work batch resume` prints the chore's files and check in place of ids (`batch_tasks.resume_said`).
- The brief `work batch brief` writes for `pr-reviewer` holds the chore's lines (`batch_brief._items`).

None of these is in a line among readiness r51-r54 or batches r41-r43. b316's commits change only the Terms, Relations and Behaviour of `spec/capabilities/readiness.md` and `spec/capabilities/batches.md`, not their `## Implementation, may change` sections. b20 did this step for its own extras (`--quote`, `--all`, `work show directive-<n>`) in conversation.md. Fix: add Implementation bullets to readiness.md and batches.md for these behaviours, or remove the ones the item does not want.

### f2 Minor observation: `work batch done` checks only the commits that cite the chore's own item
- item: b316
- where: scripts/backlog_chore.py:299
batches#r43 is about "a commit of the git branch of the task". `touched` reads only the commits whose `Item:` trailer names the chore's item, and leaves out merges (`--no-merges`). `uncited` lets a commit on the task's branch cite an earlier in-batch item (`citable`). So a commit on a chore task's branch that cites another item and touches a file outside the chore is not refused. This batch does that legitimately: d52c23f69 merges b315's shared catalogues into b316's branch. Leaving those commits out looks deliberate, but it is narrower than the line says. Either state the exception in batches' Implementation section, or also refuse a non-merge commit that cites another item and touches an unnamed path.

### f3 Minor observation: two items that make the same new capability overwrite each other's lines
- item: b317
- where: scripts/backlog_capability.py:114
`check` refuses `--capability` only when `spec/capabilities/<name>.md` exists or the same item already holds a block for it. Two items can each run `work line --capability shelf`. Then, when the readiness bar lays them together (`others`, which `batch_pick` passes) or `work batch start` lays them, the second item's `lay` rewrites the file with `write_text`. That drops the first item's groups, which `lay_onto` had already written, and adds a second Composition row. No line covers this case. Hardening: refuse in `lay` when the file already exists, or refuse the second `--capability` when another open item holds a block of that name.

### f4 Minor observation: `docs/reference/capability-file.md` calls its `model forms` listing verbatim, but it lacks two rows
- item: b317
- where: docs/reference/capability-file.md:522
The page says "This is its output at b317, verbatim". After the merge, `FORMS` also holds `item's chore` (b316) and `directive` (b20), and neither row is in the listing (from line 522, the rows around line 530 go straight from `quote` onwards with no `directive`). `test_docs` does not compare this block against the real output, so nothing catches the drift. Fix: paste the current `model forms` output.

### f5 Minor observation: conversation.md lost its `unbuilt:` key
- item: b20
- where: spec/capabilities/conversation.md:8
Commit 634b40f92 deleted the line `unbuilt: [r16, r10, r11, r14, r12, r13, r15]` instead of leaving `unbuilt: []`. Every other capability keeps the key, and `spec_unbuilt.without_unbuilt` keeps it too. `with_unbuilt` puts it back when it is missing, so nothing breaks. It is a hand edit out of line with the form. Fix: put back `unbuilt: []`.

### f6 Minor observation: the change is over the size limit
- item: -
- where: -
The range changes 61 files, +2397 -137, against a limit of 1000 changed lines. b20 makes the most of it: `scripts/directive.py` and `scripts/directive_cli.py`, about 350 lines; their scenario handlers and test, about 290; and the conversation spec, feature and corpus. b316 is next (`backlog_chore.py` and its handlers, docs and skills), then b317 (`backlog_capability.py`, the section reader, docs).
