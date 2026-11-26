---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-116/review-1
kind: review
batch: batch-116
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/139
head: 67d7b1424a48eea64346291b265291946074e64b
range: 2e26568e0de1d4987d704b1fe4a824fe47514a64..67d7b1424a48eea64346291b265291946074e64b
result: clean
---

# batch-116 review 1

## Verdict

The batch builds all ten lines of b688. The three `work line` options do what drafting r79-r84 ask, refusing with a name when the item holds no such piece. The readiness bar counts imports and retirements as lines (items r68, r69). The lay accepts a term retirement whose entry the item's own model line retirement already took out (batches r142). The lexicon reads an object that an imported pack's noun spells as that kind (checking r113). Every run exits 0 at the head. The `.feature` files are what `features generate` writes. The change is 859 changed lines, under the 1000 limit, and the module map has rows for the new modules. No tests were removed or weakened. I found nothing to fix now, and two observations.

## Findings

### f1 Minor observation: v_t4 now takes an imported pack's actor as a kind
- item: b688
- where: scripts/spec_lexicon_problems.py:53
To read r113's object as its pack's kind, the change checks a term's kinds against `known = kinds | outer`. But `outer` (spec_rgl_vocab.outer, scripts/spec_rgl_vocab.py:80) holds the base kinds and every kind *and actor* of each imported pack. So an attribute, condition or relation entry whose kind is a pack's actor, such as the time pack's clock, no longer gets v_t4 "is not a kind". Before this change it did. No line asks for that. Reproduction: in a codified-2 context importing `time`, write an attribute entry of the clock; `spec check` reports no v_t4. Fix: check only against `kinds` plus the imported packs' kinds (spec_packs.kinds), not their actors.

### f2 Minor observation: a reinstate option given with a retire option drops the retire option silently
- item: b688
- where: scripts/backlog_reinstate.py:486
`cmd` refuses a reinstate option next to the PIECES and `retires`/`reword`/`remove`/`group`/`in_group`/`into`. Its list leaves out the other edit modules' flags (`--retire-model`, `--retire-term`, `--import`, `--move-model`, `--remove-model`, ...). backlog_cli tries `backlog_reinstate` before `backlog_retire` in `EDITS`. So `work line b1 --reinstate-term x --retire-term y` reinstates x and does nothing with y, and prints no refusal. Sibling modules let the same thing through, so this is hardening, not a wrong answer against a line. Fix: add the other EDITS modules' flags to `others`.
