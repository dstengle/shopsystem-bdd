---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-15/review-1
kind: review
batch: batch-15
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/28
head: 78041d895cea7ab340ff43436e91e0f6ca68ed51
range: 6422e39e2663fd291c906d1793632c7443151a85..78041d895cea7ab340ff43436e91e0f6ca68ed51
result: fix-now
---

# batch-15 review 1

## Verdict

The batch builds b84's one line, design-model-check#r63. Verb funs are now generated per frame, so a noun of the wrong kind no longer parses, and the refusal names the verb's term. One finding is to fix: a glossary gloss goes against judgement decision 0067. Two more are observations: an item note left undone, and the change's size.

## Findings

### f1 Important fix now: the glossary now says how a request is kept, against design-decision 0067
- item: b84
- where: spec/index.md:132
To give `request` a kind that verb frames can take, the change rewrote its gloss as:

```
- **request** (kind): the one way work enters a bounded context, kept as a file under `.shop/requests/`: lines that its asker ... proposes to its upstream (the context asked). Kind of: file.
```

Decision 0067 (tier `judgement`) says: "The spec speaks of the request, not of its file: how `work` keeps a request ... is in the capability's Implementation section and may change." CLAUDE.md's first working rule and decision 0084 say the same: how a request is kept stays out of the spec. The gloss now fixes the storage path in the glossary. `Kind of: file` adds to this by typing a request as a file for every verb frame.

The change already types `issue`, `comment`, `request line` and `resolution` as `Kind of: text` without naming any storage. Fix: remove "kept as a file under `.shop/requests/`" from the gloss and make `request` `Kind of: text`. Text sits above file, so every frame that names text or thing still takes a request. Then check that the requirements that use a request still parse.

### f2 Minor observation: the gloss and frame of `merge` still disagree, though the item asked for them to be reworded
- item: b84
- where: spec/index.md:229
b84's Notes and its Answer say the builder "rewords a frame or a gloss that disagree (merge, show)", from batch-13 review 1 f5. The `merge` entry is unchanged:

```
- **merge** (event): `work run` merges a work-item branch into the initiative branch. Forms: merges, merged. Frame: the person merges pull request.
```

Its gloss names `work run` and a work-item branch. Its frame names the person and a pull request. `show` (role-boundaries.md:153, "a session shows the person a thing", frame `session shows file`) was not reworded either. No requirement line asks for this, so it does not hold the merge. It does leave the item's stated intention undone.

### f3 Minor observation: the change is over the size limit
- item: b84
- where: -
`## Size` gives 35 files, +780 -318 = 1098 changed lines, over the limit of 1000. All of it is b84's. Most of it is the glossary retyping: `spec/index.md`, and the glossary, generate and logic fixtures' `spec/index.md`, about 400 lines. The new `scripts/spec_typed_verbs.py` adds 234 lines, and `scripts/spec_frames.py` grows by about 140.
