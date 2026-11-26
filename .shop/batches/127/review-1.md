---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-127/review-1
kind: review
batch: batch-127
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/150
head: 6a009f481bf71f39402becb6faa49771e7adb0dc
range: 37fd0e0a0e71b145656dc5902ed028ada11bb9a3..6a009f481bf71f39402becb6faa49771e7adb0dc
result: clean
---

# batch-127 review 1

## Verdict

The batch builds all three lines: batches#r165 (b722) and parsing#r25 and parsing#r26 (b626). Every run exits 0, as it did at the base, and the change is well under the size limit. Nothing needs fixing before the merge; there are two observations and one polish point, none of which holds the merge.

## Findings

### f1 Minor observation: the twin test leaves out the new reply-trigger section until b724
- item: b626
- where: tests/scripts/test_construct_twins.py:18
The construct twins test checks that each line in language.md's `## Constructs` is also read by the check and by the step generator. `LATER` now leaves the new section `### "completes the request to settle a line"` out of that test, so its two lines are not checked that way. No existing case is dropped and no assertion is loosened; only the new section is left out. The item's note says this part was split off, and b724 ("A reply trigger handles a port outcome, is translated and is generated as scenarios", checking#r125, consistency#r44, scenarios#r44) holds it. It is recorded so that b724 empties `LATER` when it builds the check's reading and the steps.

### f2 Minor observation: "the request to V <np>" is not held to one object (decision 0111)
- item: b626
- where: scripts/spec_rgl_ops.py:478
`replied` builds each argument of the frame as `<K>_Arg`. That type also accepts an "and" list, "only" and the plural codes form. spec_one_thing's `plural` only looks at trees whose head ends in `_Event` or `_Request`, or holds `_ActReq_` (scripts/spec_one_thing.py:49). An `rq_` fun is the object of the pack's complete, return or refuse, so the check never reaches it. A line such as "When the work service completes the request to settle the lines, ..." should therefore read with a plural object inside `request(r, O, object: x)`. Decision 0111 says a request's object slot takes one thing's noun phrase. I did not run this; it is what the code shows. No line uses such a plural today. Hardening: pass the `rq_` funs to `spec_one_thing.plural` as well.

### f3 Minor drop: the vocabulary entry says "or fail", the construct form does not
- item: b626
- where: spec/vocabulary/specification.md:333
The entry for "replied request" lists complete, return, refuse "or fail". The construct's form in grammar/constructs.md and the section in language.md list only completes, returns and refuses. The texts should give one list of verbs.
