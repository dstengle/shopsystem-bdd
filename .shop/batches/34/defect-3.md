---
id: defect/missingmass.io/shopsystem/shopsystem-bdd/batch-34/d3
kind: defect
batch: batch-34
item: b273
date: 2026-11-16
---

# batch-34 d3

Found shaping b296 (2026-11-16): a count with an upper bound over a relation of a response's object gets no counter-example, though feature-file-tools r119 defines an upper bound as a count in the response. 'When the person runs `notes export`, `notes` shall write a file that holds at most three notes' generates only the When, 'writes the file f1' and 'the file f1 holds at most three notes', with no Givens, so a tool writing every note passes. Fixed by b296.
