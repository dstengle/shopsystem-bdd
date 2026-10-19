---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/code-research-1
kind: work-item
part_of: capability-proposal/delivery-on-v3-code-research
status: drafted
wkind: capability
under: code-research
accepts: [code-research#r1, code-research#r3-r12]
blocked_by: [work-item/formulation-1, work-item/supervision-1]
risk: none
---

# code-research-1

## Observable
`code-scout` researches a drafted work-item from a brief and writes its notes and a result with the file set; its
scenarios pass in every run of `work step`.

## Unknown
Whether Haiku at low effort finds the whole file set on the shelf fixture (it found most of Lands' files, never all,
in kb).

## What changes
`agents/code-scout.md` rewritten for the researcher stage: the brief and result file, the notes' five parts in
work-item terms, the file set, module sizes; the Lands probe and the batch consequence sweep go (r2 retired); notes
and probes under the run directory and `.shop/scratch/`. Its description says it is started by `work run`.

## Fixture cases
Each runs `work step <item>` on a drafted lend-items work-item, the real `claude`.
| requirements | case | what the fixture holds |
|---|---|---|
| r1, r4, r5, r7, r9, r10, r11, r12 | research | lend-items formulated, its work-items drafted |
| r3 | research-changed-line | an item accepting the changed keep-items#r3 |
| r8 | research-defect | a store that crashes on a title of spaces |
| r6 | research-skipped-stage | an item adding an import that skips the duplicate check |

Bound as fixture scenarios (design-decision/fixture-scenarios-under-pytest-bdd): each Given below names the fixture case it binds, built in `tests/workflow/fixtures/shelf.py`; the When runs the case's prompt with the harness of formulation-1; each Then is a check over every run, in `tests/workflow/checks/`.

## Files, roughly
`agents/code-scout.md`, `tests/workflow/test_code_research.py`, `tests/workflow/checks/code_research.py`, fixtures.
