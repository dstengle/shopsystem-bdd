---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-20/review-1
kind: review
batch: batch-20
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/33
head: 51af33e41f584bff5a4bc0141563d8b975511d41
range: d6f50200ab7175970b5502064b07e9ad7d1b0f44..51af33e41f584bff5a4bc0141563d8b975511d41
result: clean
---

# batch-20 review 1

## Verdict

The batch builds b106's three lines: a preposition right after the verb in a `Frame:` belongs to the verb and is carried in every typed fun (r68, r69), and a `Frame:` that does not read is v_t13, naming the word it stopped at (r70). Nothing needs fixing before merge. All runs exit 0, no test is removed or weakened, the module map has a row for the new `spec_frames_refusal.py`, and the change is under the size limit. b107's lines are fully out of the net change. Three Minor observations are below.

## Findings

### f1 Minor observation: a kind whose first word is a preposition no longer reads as an object
- item: b106
- where: scripts/spec_frames.py:73
`read` treats the first word after the verb as the verb's preposition whenever it is in `PREPOSITIONS` and more words follow. It never tries the frame again without the preposition. Take a multi-word kind such as `after action review` and the entry `Frame: agent writes after action review.`:
- `prep` becomes `after`;
- `rest` becomes `action review`, which is no kind;
- the verb gets v_t13 at "action review".

Before this change the frame read with `after action review` as the object. No glossary has such a kind today. Fix: when the object after the preposition does not read, read `rest` whole as the object before giving the v_t13 reason.

### f2 Minor observation: the refusal for a missing preposition is behaviour no line names
- item: b106
- where: scripts/spec_frames_refusal.py:84
A line that leaves the preposition out is refused with "the verb subscribe takes its object after to: …". It is tested in `tests/scripts/test_spec_frames_prepositional.py`. No requirement line of b106 asks for it: r69 asks only that a prepositioned line parses. It refines b82's existing refusal that names the verb, which is why this is not `fix now`. Consider a requirement line for it, so the message is checked by a scenario and not only by a script test.

### f3 Minor drop: the v_t13 message for a frame without its verb repeats itself
- item: b106
- where: scripts/spec_frames.py:99
When the frame has no verb, or the verb comes first, the message reads 'the Frame: does not read at "…": it expects its subject, then the verb subscribes after its subject'. "after its subject" says the same thing twice. Polish only.
