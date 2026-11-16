---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-42/review-1
kind: review
batch: batch-42
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/64
head: 943abf702a2a00d86d590d6133d0b61dda45f00a
range: 303795071896992ccbcf64e8361d07e9ff37dd57..943abf702a2a00d86d590d6133d0b61dda45f00a
result: clean
---

# batch-42 review 1

## Verdict

The batch builds all four items. b328 makes r318 and r133 read one way. b39 builds r104 through r111. b40 builds r112 through r115. b52 builds conversation r9. Every run in `## Runs` exits 0, the change is within the size limit (946 of 1000 lines), and I found no weakened test: the g77 scenario and the old test_request_flow case changed only because r105 retires r77. Two observations about text this change left stale, none to fix before the merge.

## Findings

### f1 Minor observation: the module map still says sync never records an unreadable comment
- item: b39
- where: CLAUDE.md:126
`CLAUDE.md`'s module map is binding. Three of its rows describe behaviour this change replaced:
- The `scripts/request_sync.py` row still says a comment `work sync` cannot read is "printed and never recorded". Since commit 980e7affc, `caught_up` records it as `unreadable` and applies nothing of it (r105, r106), so the row now says the opposite of the code.
- The `scripts/request_view.py` row (line 121) lists `work show`'s lines "with their outcomes", but `work show` now prints each line's reason too (r104).
- The `scripts/conversation_read.py` row (line 79) does not mention a queued message, which now counts as one of the person's messages (b52).

The change updated the rows for `request_steps.py` and `requests_world.py` but not these three. Fix: rewrite the three rows to match the code.

### f2 Minor observation: the offer is still described as quoting each capability whole and the glossary
- item: b40
- where: skills/taking-in-a-request/SKILL.md:17
Since commit 802d43aec, `offer_text` quotes each named capability's groups and requirements, plus only the term entries those requirements mention. Two places still describe the old offer:
- Step 2 of skills/taking-in-a-request/SKILL.md says "It quotes each capability whole and the glossary" and "none is an offer of the glossary only".
- docs/reference/commands.md:414 says the capabilities are "quoted whole under `## Offer` with the glossary".

There is also a behaviour change the skill gets wrong. With no `--capability`, `lines` is empty, so `mentioned` returns nothing and the offer posts only the note and the closing question. It no longer posts the glossary-only offer the skill tells a session to make. To reproduce: run `work offer q<n> --note x` with no `--capability`; the posted comment holds no glossary. No line asks for an offer without a capability, and the changed Implementation section of requests.md allows this, so this is not a fix-now finding.

A smaller point: the `--from` text in docs/reference/commands.md now says "this bounded context's id", but `request_moves.gate` still also accepts `internal`.

Fix: update both texts to the new offer and either drop the "none is an offer of the glossary only" guidance or say what an offer with no capability now holds.
