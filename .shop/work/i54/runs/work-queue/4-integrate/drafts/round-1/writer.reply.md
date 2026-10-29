/tmp/work-run-i54-w4h4vwrv/work-queue-4-integrate/.shop/scratch/4-integrate/drafts/round-1/spec/capabilities/work-queue.md

## Change list

| change | capability | id | line | source |
|---|---|---|---|---|
| removed | work-queue | r34 | - [r34] **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status. | replaced by r60 (request q20 line 2) |
| removed | work-queue | r35 | - [r35] **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object. | the person's answer 2026-10-29, reading (a): "retire r35 and add r50 '**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.'" |
| added | work-queue | r59 | - [r59] **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution. | request q20 line 1 |
| added | work-queue | r60 | - [r60] **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status. | request q20 line 2 |
| added | work-queue | r61 | - [r61] **Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object. | the person's answer 2026-10-29, reading (a): "retire r35 and add r50 '**Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object.'" (numbered r61, since r50 to r58 are taken by other drafts) |

Frontmatter: `retired` is now [r2, r3, r11, r16, r17, r18, r33, r34, r35]. Placement: r60 and r61 stand where r34 and r35 were, and r59 comes after r37.

No glossary change. No decision file.

## Questions

None.

## Cut sentences

None.
