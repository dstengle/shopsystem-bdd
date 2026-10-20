---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/migration-in-one-pass
summary: "A consuming repository moves from the old system to the final layout in one migration, with one gate: scripts/migrate makes every mechanical change and is the only code that knows the old layout; the session does what needs judgment."
date: 2026-10-19
status: proposed
supersedes: [model-reads-a-ledger]
source: [observation/2026-10-19-final-state-only, review-finding/2026-10-13-kb-and-bdd-assessment]
by: "the person, 2026-10-19"
---

# 0049. Migration in one pass

## Decision

There is no intermediate state in a consuming repository. `migrating-to-capabilities` takes it from whatever
it has of the old system (a decision ledger, top-level `decisions/`, `work/` or `records/`, `docs/superpowers/`,
a living slice plan, `@holding` scenarios, lines without ids) to the layout of
design-decision/final-layout in one run, committed in two commits: the mechanical move, then the tags,
work-items and observations the gate's answers allow.

`scripts/migrate` does everything that is transcription: numbering lines, rewriting ids, moving files,
splitting the ledger into decision files, renaming `@holding` to `@deprecated`, and turning a living plan's
open slices into work-items. It refuses rather than guesses. The session does what is judgment: the context
path when `spec/index.md` lacks it, mapping scenarios to lines, glossary bullets out of form, which open
slices to keep and which plan entries to leave out. All of it is shown at one gate.

`scripts/model` and every other script read only the final layout: design-decision/model-reads-a-ledger,
rejected 2026-10-19, is superseded so that no reading of the ledger is ever built.
