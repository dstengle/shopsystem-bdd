---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-164/review-1
kind: review
batch: batch-164
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/187
head: be7f0b29fc6f8c4d53403ade4140f0463a757020
range: 57af90f7732866b34bd830540d1a6903cd256aa9..be7f0b29fc6f8c4d53403ade4140f0463a757020
result: clean
---

# batch-164 review 1

## Verdict

The batch builds both items, and nothing needs fixing before the merge. b839's chore works: `--serves` takes the job alone when `--into` is given or a line follows. It takes two words only when the first one has the form `<cap>#g<n>`. I checked each case by hand: the old order (line before `--serves`), the new order, a group pair followed by a line (refused), and `--into` with no line (refused). For b840, a `Frame:` with text after it gives a v_t13 naming the frame, and a slot that names nothing gives a v_t13 naming the slot. `spec check` reports both (checking#r158, r159), and `work line --term` refuses both through the existing v_t13 rule (drafting#r110, r111). Every check in `## Runs` exits 0, and the change is under the size limit. Four observations follow.

## Findings

### f1 Minor observation: the old order, the line before `--serves`, is no longer tested anywhere
- item: b839
- where: tests/scenarios/drafting_handlers_job.py:71
The r93 handler used to run `work line <item> --into work-queue <line> --serves start-work`. It now runs only the new order, `--serves start-work <line>`. The item asked for this change, so it is not a weakened test. But no other test runs the old order, which the docs and the module map still describe: `tests/scripts/test_backlog_serves.py` has the new order and the group form only. If `_read` breaks the old order later, nothing would catch it. Fix: add a test of the old order to `tests/scripts/test_backlog_serves.py`.

### f2 Minor observation: a slot naming a model object that no noun names is read as `thing` and not reported
- item: b840
- where: scripts/spec_vocabulary_terms.py:158
checking#r159 and drafting#r111 ask for a v_t13 when a slot "refers to no term whose part of speech is `noun`" or `proper noun`, and to no parameter. `unslotted` accepts any name in `model.objects`, through the `known` set built at `lexicon` (line 384). When `_frames` reads such a name, `_slot` fails in strict mode and falls back to `["thing"]`. So a slot like `<widget>`, where `object widget` exists but no vocabulary noun means it, is read as `thing` and not reported. Today this only affects an object whose noun is missing, which no current fixture has. Fix: if the line is meant literally, drop `*model.objects` from `known`, keeping a pack's kind that the model names.

### f3 Minor observation: the module map rows of spec_lexicon and backlog_serves do not describe the new code
- item: -
- where: CLAUDE.md:64
The spec_lexicon row does not mention its new `unended` function or the Term fields `unended` and `unslotted`; only the spec_frames row names them. The backlog_serves row still gives only `--into <cap> [--group <title>] <line> --serves <job>`. It says nothing of `--serves <job> <line>` or of `_read`'s rule that only a first word of the group form takes two words. Fix: add these to the two rows.

### f4 Minor observation: a field the reader does not know, written after a `Frame:`, now gives a v_t13
- item: b840
- where: scripts/spec_lexicon.py:313
`unended` looks for a full stop followed by more text inside a frame's field, with code spans and quoted text masked out. That works because a `Frame:` field is read up to the next field `PATTERNS` knows. Text after a frame that only looks like a field (`See: ...`, or a gloss sentence written after the frame) is read into the frame and now reported. That is what the line asks for, and I found no live entry in `spec/` or `grammar/packs/` it would catch. But a consumer whose entries carry text after the frame will see new v_t13 failures in `spec check`. This is the clean break that decision 0097 accepts, and the change log could say so.
