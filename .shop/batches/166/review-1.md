---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-166/review-1
kind: review
batch: batch-166
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/189
head: dbc15d66aeb954fb0cb5ea874aeb00494e15f360
range: e2aca5605008f612686838a89d94cb4bcdbfb128..dbc15d66aeb954fb0cb5ea874aeb00494e15f360
result: fix-now
---

# batch-166 review 1

## Verdict

The batch builds b851's line. It also builds b847's four lines as their scenarios state them. But b847's new `packed` check in the bound check counts a verb's senses differently from grammar 4: the pack's sense is first in grammar 4 and is not counted at all in `Lines`. So in a context that keeps a pack verb beside its own, the bound check reads each sense as the other. One finding to fix, two observations.

## Findings

### f1 Important fix now: the bound check reads the context's sense and the pack's sense the wrong way round
- item: b847
- where: scripts/model_domain_lines.py:150
`Lines.packed` decides whether an event atom is the request pack's sense of a verb or the context's operation sense. It looks the atom up as `self.operations.get((a.args[1], a.args[2]))`, where `a.args[2]` is the sense number `spec_lf_clause.sense` gives. That number is the verb's place among its word's entries in grammar 4's vocabulary (`spec_rgl_vocab.read`). With this change, that vocabulary keeps the pack's entry beside the context's (`spec_rgl_vocab.lexicon`, the `layer == "pack request" and sense in beside` branch). It keeps them in `spec_packs.layers` order, packs first, so the pack's `return` is sense 1 and the context's `return` is sense 2.

`Lines.operations` (scripts/model_domain_lines.py:95-99) is numbered over `spec_lexicon.read(root)` instead, and that lexicon holds only the context's own terms. All three callers (model_domain.py:115, adapter_annotate.py:53, product_coordination.py:33) build it that way. So there the context's `return` is sense 1, naming `notes.return`, and sense 2 is missing.

The result is that `packed` gets it backwards:
- The pack's `return`, `refuse` or `name` (sense 1) is taken for the context's operation, and the call returns False.
- The context's sense (sense 2) is taken for the pack's, and the call returns True.

What this breaks:
- `model_bound.line_facts` misses the `on_outcome` and `denies` facts of a core or port line on the pack's sense.
- `Lines.refused` and `Lines.reasons` lose the refusal reasons a line states, which v_m4 and v_pb2 read.
- Line 142's `asks` reads a response's act of the pack's `return`, such as r31's "the notes service shall return every note", as a request of `notes.return`.

The new scenarios do not reach this: r162's world uses the redefined verb only in a trigger, which gives a `request` atom, not an `event` atom. Fix: number the senses in `Lines` over the same terms grammar 4 reads, for example from `spec_rgl_vocab.read(root).verbs` or the layered lexicon with the pack's entry kept beside. Then add a case to the bound or annotate tests where a line uses the pack's `return` or `refuse` beside a redefined one.

### f2 Minor observation: a frame whose subject names an actor now takes that actor alone, in every context
- item: b847
- where: scripts/spec_lf_clause.py:57
`_actor` applies to every verb's frames, not only to a verb kept beside the request pack's. Any frame written with an actor as its subject (for example `the person archives <note>`) now gives no reading of a line whose subject is another actor of the same kind, or a referent of a kind below it. Before this change such a line was read through the actor's kind. No line of b847 asks for this outside the beside case. I checked: no `Frame:` in this repository's `spec/vocabulary/` starts with a named actor, so nothing here changes. A consumer's lines could stop parsing after the upgrade, with nothing reported. A possible fix is to limit the check to verbs whose entry is `spec_lexicon.beside`, or to report such frames in the 0.45.0 upgrade step.

### f3 Minor observation: the 0.45.0 report rewrites a hyphenated term's word
- item: b851
- where: scripts/upgrades/migrate_upgrade_stricter.py:23
`word` turns every `-` of a term's id into a space. A term whose word itself has a hyphen, such as `design-decision` or `pull-request`, is reported as `design decision`, which is not the entry the session has to reword. To reproduce: give a term `follow-up` (verb, action) a `Frame:` with no slot in angle brackets and upgrade from 0.44.0. The report line names `follow up`. A possible fix is to name the term by the word its entry writes (the lexicon's `Term.term`), not by its id.
