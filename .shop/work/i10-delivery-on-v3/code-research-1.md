---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/code-research-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-code-research
status: done
wkind: capability
under: code-research
accepts: [code-research#r1, code-research#r3-r6, code-research#r8-r12]
blocked_by: [work-item/supervision-1]
risk: none
---

# code-research-1

## Observable
`code-scout` researches a drafted work-item from a brief and writes its notes and a result with the file set, for
`work run`'s research stage.

## Unknown
Whether Haiku at low effort finds the whole file set on the shelf fixture (it found most of Lands' files, never all,
in kb).

## What changes
`agents/code-scout.md` rewritten for the researcher stage: the brief and result file, the notes in work-item terms,
the file set, module sizes; the Lands probe and the batch consequence sweep go. Its description says it is started
by `work run`.

## Fixture cases
Each starts the researcher on a drafted lend-items work-item, the real `claude`, with the fixture harness outside
this repository (formulation-1 is deferred).
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r4, r5, r9, r10, r11, r12 | research | lend-items formulated, its work-items drafted |
| r3 | research-changed-line | an item accepting the changed keep-items#r3 |
| r8 | research-defect | a store that crashes on a title of spaces |
| r6 | research-skipped-stage | an item adding an import that skips the duplicate check |

## Files, roughly
`agents/code-scout.md`, the fixture cases.
