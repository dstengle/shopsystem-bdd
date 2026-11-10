---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-30/review-1
kind: review
batch: batch-30
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/44
head: f7da3ddb9e148ec44cc3cb1c4d97b16f486664a0
range: 1fff68f11a38bcd25d04702bbc4952c5d13d5e0d..f7da3ddb9e148ec44cc3cb1c4d97b16f486664a0
result: clean
---

# batch-30 review 1

## Verdict

The batch builds all four items. b215 adds a recipient behind any preposition and types each sense of a verb. b217's R2 now skips the noun phrase that holds the "the". b218 adds the example-data Givens of step grammar 4. b219 reads a state verb with no object as a one-place fluent. No test is removed or weakened; the one test change makes the `term` handler raise on an unknown condition. The feature files are as `features generate --check` wants them, and the change is under the size limit. There is one observation about the module map and one about a run that already failed at the base.

## Findings

### f1 Minor observation: the module map still says codified-1 reads only a verb's first sense
- item: b215
- where: CLAUDE.md:53
The `scripts/spec_frames.py` row still ends "the codified-1 grammar reads a verb's first frame of its first sense". After 0f02f1e2, `spec_frames._of` keeps every sense of a verb, and `guard` passes a subject that fits any of them (scripts/spec_frames.py:214-248). `spec_typed_verbs.frames` also gives each later sense its own funs, `e__s2__Do` and so on. The row also does not mention the preposition before a recipient (`Frame.oblique`). The `spec_typed_verbs.py` row (CLAUDE.md:55) mentions neither the later-sense funs nor `typed` choosing the first sense the arguments fit. The `spec_frames_refusal.py` row (CLAUDE.md:54) does not say the recipient's preposition is now the frame's own. CLAUDE.md makes the module map binding, and these rows now say less than the code does, or the opposite. Fix: rewrite the three rows on b215's branch.

### f2 Minor observation: `model decisions --check` fails at the head and at the base
- item: -
- where: -
The run exits 1 at the head and 1 at the base. Decisions 0086, 0087 and 0088 report `tests/scenarios/vocab.py: exit 5` ("no tests ran"). The base has the same failure, so this batch did not cause it. It is recorded here and does not hold the merge.
