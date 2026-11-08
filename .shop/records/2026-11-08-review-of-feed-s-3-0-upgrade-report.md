---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-08-review-of-feed-s-3-0-upgrade-report
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-08
---

# Review of feed's 3.0 upgrade report

## What was reviewed

feed's report "shopsystem-bdd 3.0 upgrade report: feed" (2026-11-08), pasted by the person: feed upgraded from plugin
2.1.0 to 3.0.1; five open findings, and the 3.0.0 negated-recipient bug confirmed fixed in 3.0.1. Each finding was
checked against this repository's code at 3.0.1; feed's repository was not read.

## Verdicts

| # | Finding | Verdict | Where it goes |
|---|---|---|---|
| 1 | r5/r6 clash because nothing says a video is from one channel | The ask exists already: a relation row's fourth cell `one` makes it functional (`spec_logic_vocab.functional`, `fun/1` for `check.lp`). feed can write `\| video \| from \| channel \| one \|`. The gap is that the L1 gives no hint of it. | feed: add the cardinality. b109: an L1 through a row with no cardinality names the row and `one`. |
| 2 | Generated Thens drop qualifiers (a negated object's restriction, `every`, two list instances) | Holds. The generator words a negated object as a bare instance; this is the gap b7 already names. | b108, overlapping b7 (needs-input). |
| 3 | Object relative clauses ("a channel that a viewer subscribes to") do not parse | Holds. The verb-frames design lists them; b84 did not build them. feed's workaround adjective `quiet` is logically sound (quantified, no free "the") but should become a definition once relative clauses exist. | b107. |
| 4 | v_t11 on a prepositional verb whose Frame: is present | Holds, and is a defect: `spec_frames.frame` reads "to channel" as the object, against the design's own example `Frame: user subscribes to channel.` | Defect `.shop/batches/13/defect-1.md` against b82; fix b106. |
| 5 | migrate upgrade commits and pushes, unannounced | Holds in part. Committing and pushing are by design (U4; every commit is pushed, the person 2026-11-06), so no `--push` flag. The docstring ("nothing is committed") is wrong for upgrade, and nothing says before it acts. | b110. |

## Order

b106 first (a defect: a consumer's correct glossary fails `model check`), then b107 (unblocks feed's r4 without a
workaround term), then b108 with b7, b109 and b110.
