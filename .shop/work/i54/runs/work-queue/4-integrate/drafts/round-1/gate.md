# Gate, round 1 (q20, initiative i54)

## work-queue
- Added [r59] **When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution.
- Added [r60] **When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status.
- Added [r61] **Where** `--json` is given, `work list` shall print its result, each initiative and work-item with its status, as one JSON object. (the person's answer 2026-10-29, reading (a); numbered r61 as r50 to r58 are drafted elsewhere)
- Removed [r34] (retired; replaced by r60), it was: **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.
- Removed [r35] (retired; replaced by r61), it was: **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object.

## supervision
Nothing: line 3 of q20 is already in spec as r187.

## Glossary: none. Decisions: none.

## Questions
None.
