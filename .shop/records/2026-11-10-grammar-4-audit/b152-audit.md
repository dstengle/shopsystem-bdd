# Audit: can grammar 4 say design-model-check? (b152, with the gap items)

Scope: 149 lines. design-model-check has 115: b152's 105 rewordings (91 of the original lines, and r265–r278, which reword the gap items' r160–r173), the 5 lines kept unchanged (r50, r54, r55, r56, r156), and the ready items b238 (2) and b239 (3). The other 34 are the lines the gap items b197, b215–b222 and b234–b237 added in feature-file-tools, readiness and batches. I laid b152 over a copy of `spec/` with `backlog_lines.lay` and ran `model parse --form` on all 110 of design-model-check's grammar-4 lines. All of them parse, and none is refused. I also parsed 13 alternative wordings to test whether a construct was really missing or only avoided. The rows are in `audit.tsv`.

## Counts

| verdict | all | design-model-check | gap items, other capabilities |
|---|---|---|---|
| fine | 52 | 47 | 5 |
| distortion | 44 | 44 | 0 |
| unsayable | 3 | 3 | 0 |
| coined | 50 | 21 | 29 |

Two thirds of b152's own rewordings are fine or close to it. The grammatical-construct lines (r209, r212, r229, r233–r245, r252, r255, r256, r258, r259) say what the old adjective said, using a standard linguistic noun ("a requirement that uses a whose clause"). The conformance lines (r189, r195, r196) and the written-out lines (r190, r198, r264) are fine too.

## Missing constructs, and how many lines rest on each

| construct (what is hidden or bent) | lines | example |
|---|---|---|
| A rule code stands for the rule's condition (catalogue reference) | 24 | r175 "While a capability violates `v15a`, ... exit with an error naming `v15a`" |
| An adjective that quotes another line's construct (the gap items' fixtures) | 26 | b197 r35 "a capability that is distributing"; b236 "reframing", b237 "refraining", b238 "screening" |
| A meta-level noun whose gloss hides structure (in the rewordings) | 16 | r271 "boxed noun phrase", r278 "negated modifier", r218 "unification failure", r266 "later sense", r257 "number" |
| Identity across two lines or referents ("the same trigger and state", "another", "two others") | 12 | r276–r278, r248 and r253 dropped "under one trigger and state"; r199 "another interpreter" does not parse |
| A state verb standing for a negation | 6 | r203 lacks, r205/r206 omits, r210 mismatches, r230 disagrees, r251 adds |
| A proper noun for a path or pattern | 6 | r191 "the capability id form", r193 "the feature form", r204 "the node id form", r174 "the design model" |
| History with "unchanged since" | 3 | b239 reparsed, outdated, uncached |
| A counterfactual ("is not what `model decisions` would write") | 3 | r202, r203, r220: the rewording catches only missing entries |
| "For each slot" / an attribute with no value | 3 | r221 (v_t14), r223, r224 (v_t15) |
| Readiness-bar and id adjectives | 5 | b234 "passing" ×3 and "unparsed", b220 "nonexistent" |

The categories overlap: some lines are in two.

## Worst examples

- **r276–r278, r248, r253** (from the quantifying, thresholded, excepting, exhaustive and overcounted adjectives). The old definitions required "a line of one trigger ... in a state where ...". The new lines link the two requirements only through a shared `act`. The forms show `oblige(x1, act)` and `forbid(x5, act)`, with no trigger or state shared. As written, the line requires `L1` for any two lines that touch one act, whatever their triggers. This is a change of meaning, and the grammar cannot express sameness across lines.
- **r218**. "unification failure" and "clash" hide "two requirements share a code that check.lp cannot unify, and two *others* conflict". The response also changed, from "print a requirement" to "print the clash".
- **r202, r203, r220**. A stale index meant "not what `model decisions` would write". The rewording ("has an index entry that the index does not hold", "no index lacks an index entry") only catches missing entries, not extra or changed ones. The counterfactual has moved into the gloss of "index entry" ("as model decisions writes it now").
- **r223**. "more than one sense" dropped "whose kinds do not overlap". The line is now true of overlapping senses too, and it stands only because r224's If takes precedence.
- **r199**. "shall use an interpreter that imports `clingo`" reads under R1 as a new interpreter. "Where a python3 on PATH can" and the "0 violations" are gone.
- **r174**. The required output "0 violations" became "print no violation". The condition now lives in the gloss of "the design model".
- **b234 r21**. "While an item is `shaped`, if ... on an item that ..." uses two unrelated items.
- **r231** (a parse finding). In the form, the second case of the "or" uses `x2`, which is declared inside the first case. R2 does not treat the cases of an "or" as boxes.

## Which distortions a rewording alone could fix

Grammar 4 already parses these alternatives (probes run):

- **r207**: "While a term has no frame" parses. **r214**: "a term whose entry names no part of speech". Other rule-code lines are also sayable from structure: r177, r180, r181, r183, r184, r187, r188, r197, r217 and r226 (r226 needs "neither ... nor"). That holds only if the person reopens the catalogue decision (b123). Until then those lines are a sanctioned distortion: the meaning is in the gloss of each `v...` constant.
- **r230**: "a term that does not agree with its subject" parses. **r251**: both "a premise entails every consequence of a requirement" and "no premise entails the consequence" parse. These verbs were forced by `spec_facts` and `spec_steps` (no `not` over an image, no `every` in a condition), not by the grammar. They can be reworded once b197's successors read those forms.
- **r192, r194**: a section kind plus "or" (which parses, as r231 shows) would replace the proper nouns.
- **r174**: put back "print `0 violations`".
- The gap items' **"scenarioless"** is "a feature that has no scenario".

A rewording cannot fix these. Identity across lines (12 lines) and the counterfactual (3) need new constructs. So does "for each slot" (r224). r210's natural form ("a noun phrase that no frame of a term takes ... name the term") is refused by R2, because "the term" sits inside the no box. The quotation adjectives (26) need a way for one line to mention another line's construct, which is a quotation or mention construct. Without it, every fixture line for a grammar feature brings in one coined adjective whose gloss is the feature. That is exactly the anti-goal in the person's direction: "We should not be defining simple english terms with domain specific meaning." Most of these glosses are not plain English words, but each one carries the structure the line is about.
