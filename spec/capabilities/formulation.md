---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/formulation
title: Formulation
narrator: the person who approved the lines
group: guarantees
rests_on: [design-decision/a-scenario-names-one-requirement, design-decision/exits-are-successful-or-errors, design-decision/formulation-needs-no-second-approval, design-decision/spec-writers-blind-to-code, design-decision/held-scenarios, design-decision/controller-per-spec-round, design-decision/workflow-capabilities-are-guarantees, design-decision/the-context-runs-without-a-coordinator]
language: codified-2
retired: []
---

# Formulation

## Purpose
**Retired in plugin 0.31.0** (design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-old-workflow-retired): every requirement of this capability is retired, and the file is kept as the record of its ids and of where its 0.29 lines went.

Formulation is no longer a session's work. A scenario is the generated linearisation of one requirement group
(design model v5), so `work run`'s formulate round runs `features generate` as a script, with no session and no
question (supervision). What the 0.29 lines of this capability guaranteed is either said by that script, and moved to
supervision, or has no subject left: no line admits two readings once it parses to one tree, and the generator owns
every feature file, so no scenario is deprecated, rebound or reworded by hand. The capability keeps its file as the
record of where its lines went.

## Behaviour

## Implementation, may change
- None: retired in plugin 0.31.0.

## Not yet
- None.

## Dropped
- r1@0.29: moved to supervision
- r2@0.29: moved to supervision
- r3@0.29: no line has two readings: a statement that does not parse to exactly one tree is refused (v_p1, v_p2).
- r4@0.29: the generator owns feature files and `features deprecate` is gone; a group's scenario is regenerated, never deprecated.
- r5@0.29: as r4: a removed group's scenario is removed by the generator.
- r6@0.29: moved to supervision
- r7@0.29: moved to supervision
- r9@0.29: one scenario is generated for each group; a line every call must keep is a group of its own.
- r10@0.29: the formulation question is gone with the formulator: an implementer's evidence goes back as a question for the spec.
- r11@0.29: moved to supervision
- r13@0.29: design model v5's v_s1 to v_s3 say it, and design-model-check checks them.
- r14@0.29: a generated scenario uses only lexicon words, and v_t1 checks the prose that is left.
- r22@0.29: moved to supervision
- r23@0.29: no old scenario is run alone before it is replaced: nothing is deprecated.
