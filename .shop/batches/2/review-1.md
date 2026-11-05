---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-2/review-1
kind: review
batch: batch-2
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/18
head: 3e6ed32c06c975ca04bbd5922caabc8aedc6afef
range: a000613882c65c671a4866567fd1913c67f252fe..3e6ed32c06c975ca04bbd5922caabc8aedc6afef
result: clean
---

# batch-2 review 1

## Verdict

The batch builds all four lines of b41 (design-model-check r55 and r56, decision-tiers r7 and r8), with scenarios and script tests. Every check in `## Runs` exits 0, and the change is inside the size limit. I found nothing to fix now: three hardening observations and one drop.

## Findings

### f1 Minor observation: the rules disagree on where a design record goes
- item: b41
- where: skills/shaping-items/SKILL.md:14
The shaping-items skill now says a design record is written with `work record ... --kind design`. That command writes one file, `.shop/records/<date>-<slug>.md`. CLAUDE.md, in an unchanged rule just below the one this change edits, still puts a design or a plan under `.shop/records/<date>-<topic>/` as `design.md` and `plan-*.md`. `model forms` (scripts/model_forms.py:27-53) lists no design or plan form at all. So a session following the skill writes the design where CLAUDE.md says it does not go, and `model forms` gives it no answer. This is guidance, not a line of the batch, so it does not hold the merge. The fix: say in CLAUDE.md that a design record is written by `work record --kind design`, or add a design and a plan form to `FORMS` with what writes them.

### f2 Minor observation: leaving out another required argument hides the `--tier` error
- item: b41
- where: scripts/decision_write.py:158
`--summary` and `--decision` are `required=True` in argparse, so argparse checks them before `write()` reaches its `--tier` check. Reproduction: run `work decision "T" --decision x` with no `--summary` and no `--tier`. It exits 2 with argparse's usage error, which names only `--summary`, not `--tier`. Nothing is written, so "change nothing" still holds. Line r8 is met as its scenario states it, but a first attempt that lacks several arguments is not told about the tier.

### f3 Minor observation: `--about` is written into the frontmatter unchecked
- item: b41
- where: scripts/record_write.py:459
`about = args.about or ...` goes straight into the frontmatter text. It is not checked for line breaks as the title and summary are (`one_line`), and it is not quoted. Reproduction: run `work record T --kind analysis --summary s --body f --about $'x\nkind: other'`. The record gets a second `kind:` line, or any other field. Nothing sends such a value today. The fix: run `about` through `one_line` and check it has the form of an id.

### f4 Minor drop: a constant is copied from model_work
- item: b41
- where: scripts/record_write.py:387
`HISTORY` is a copy of `model_work.HISTORY`, and `KINDS` is written by hand from `model_work.RECORD_KINDS`. If `model`'s record kinds change, these copies drift. Importing them instead would change the dependencies between the modules, which costs more than this is worth.
