---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-16/review-1
kind: review
batch: batch-16
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/29
head: 876ec7cdeb9cd8a796e679f28dd5b52c47bec2d6
range: d15ecc2776e82f9a1b70c09a97594b58add2e9cf..876ec7cdeb9cd8a796e679f28dd5b52c47bec2d6
result: clean
---

# batch-16 review 1

## Verdict

The batch builds both items. design-model-check#r66 (addressed), #r64 (verbal) and #r65 (agentless) each have a typed grammar fun or a refusal, a corpus line, and a scenario fixture in `FRAMED` that drives `model parse`. Every run exits 0. No test was removed or weakened, and the change is well under the size limit. Nothing needs fixing before the merge; there are three observations.

## Findings

### f1 Minor observation: the passive refusal can misname why a clause failed
- item: b85
- where: scripts/spec_frames.py:261
`refusal` now falls back to `passive` every time no verb frame explains where GF stopped. `passive` then scans the whole clause around the stopping token for `is`/`are` followed by an event's participle. It leaves out participles that are condition terms, but not ones that are attribute values. For example, a status value `merged` is also the participle of the event `merge` in `spec/index.md`. Take a clause that says `... is merged ...` and fails to parse at some other token in the same clause. Its hint would read "the verb merge takes a subject, which a passive leaves out", which is not the real cause. I checked that `passive` only filters with `lexicon.of("condition")`. Fix: also leave out attribute values, or check only when the participle is at the stopping token or right before it.

### f2 Minor observation: participle fallback gets doubled consonants wrong
- item: b85
- where: scripts/spec_frames.py:252
For a verb with no second `Forms:`, `participle` adds `-ed` or `-d`. So `commit` becomes `commited` and `stop` becomes `stoped`. A passive of such a verb is then not recognised, and the refusal gives no hint naming the verb. Today every event in `spec/` I looked at gives `Forms: <s3>, <participle>`, so no current line is affected. The risk is only for a consumer glossary that leaves out `Forms:`.

### f3 Minor observation: the module map's spec_frames row does not name `passive`
- item: b85
- where: CLAUDE.md:1
The `scripts/spec_frames.py` row names `refusal` (the verb and the role a line breaks) and the guard. It does not name the new refusal of a passive with no agent (`passive`, `participle`). The rule "a new concern gets a new module and a row here" is met loosely, because the concern stays in its module. Fix: add the passive refusal to the row's text.
