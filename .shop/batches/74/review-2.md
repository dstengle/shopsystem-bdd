---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-74/review-2
kind: review
batch: batch-74
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/98
head: 352ce9ca9c2e810c51516ae9575a9b343aa2789a
range: 65c3f3eab258bb8c4c8afa636cdc37f6004325de..352ce9ca9c2e810c51516ae9575a9b343aa2789a
result: clean
---

# batch-74 review 2

## Verdict

Both fixes hold. With no domain model, an accepted term proposal is now written in the capability term form that `spec_lexicon` reads. `tools check` exits 0 at Head and at the base. One hardening observation, which does not hold the merge.

## Findings

### f5 Minor observation: the capability term form drops what the model element gave, and the refusal in `term_entry` almost never fires
- item: b42
- where: scripts/request_terms.py:92
`term_entry` keeps only the text after the element reference (`ref.group("rest")`). The `→ <element>` part is thrown away. With no domain model, that loses two kinds of entry:

- **An entry with no definition after the reference.** `- **shelf** (noun) → object shelf.` passes `check`, because REF's `rest` group is optional. It is then written as `- **shelf** (noun): ` with an empty gloss.
- **A verb or attribute entry.** `(verb, action)` and `(attribute)` entries were meant to get their frame or values from the element. In a capability term they need `Frame:` or `Values:` instead, and nothing writes them.

The guard that is supposed to catch this does not. `spec_lexicon.ENTRY` (scripts/spec_lexicon.py:27) accepts an empty text, so `spec_lexicon.entry(term, capability)` returns an entry for any bullet `term_entry` builds. The Refused branch is effectively unreachable. These entries become lexicon problems (v_t7, v_t11, v_t4) at the readiness bar, after `work accept` has already committed the item.

Reproduction: in a context with no `spec/model/`, accept the proposal `- **shelf** (noun) → object shelf.` The item's block then holds `- **shelf** (noun): `.

Hardening: refuse the accept, naming the proposal, when the definition is empty or the part of speech needs a frame or values the entry cannot give. No client sends such a proposal today, and no line names this case.

## Earlier findings
- f1: fixed
- f2: fixed
