---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/final-layout-batch-measurement
kind: capability-proposal
part_of: initiative/i11
status: formulated
date: 2026-10-19
argues: [batch-measurement]
changes: [batch-measurement#r10, batch-measurement#r16]
---

# Batch measurement: two words, nothing else

batch-measurement stays as it is until initiative i12 (the person, 2026-10-19). Two of its lines use words the
glossary now avoids, and `model check` would report them under v_t1: r10 ("however many transcript rows
carry it" → "it appears in") and r16 ("the tasks the batch plan held" → "had"). Nothing in `scripts/measure`
changes. Four scenario steps follow at formulation: "the repository holding one living plan", "a repository
holding <plans> … files", "held 5 tasks … the 7 held", "is carried by three transcript rows". Their titles,
which bind the tests, do not change.

The alternative is to leave the words and accept v_t1 rows until i12; NOTES.md recommends this proposal.
