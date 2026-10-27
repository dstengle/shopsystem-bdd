# Gate: work-queue, integrate round 5 (answers of 2026-10-27)

r33 (the earlier draft, never in spec/) is dropped; its replacement is work-queue r39.

## work-queue

Added:
- [r34] **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status.
- [r35] **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object.
- [r39] **While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request.
- [r36] **When** `work show <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`.
- [r37] **When** `work show <work-item>` is run, `work` shall print the work-item's status and its open questions.
- [r38] **Where** `--json` is given, `work show` shall print its result as one JSON object.

Removed (ids retired; r33 also listed as retired by the answer, though never in spec/):
- [r3] **When** `work show` is run, `work` shall print each work-item of every initiative under `.shop/work/` with its status.
- [r11] **Where** `--json` is given, `work show` shall print its result, each work-item with its initiative and status, as one JSON object.
- [r16] **When** `work status <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`.
- [r17] **When** `work status` is run with no initiative, `work` shall print what r16 gives for each initiative that is neither `done` nor `abandoned`.
- [r18] **Where** `--json` is given, `work status` shall print its result as one JSON object.

## requests

Added:
- [r46] **When** `work list` is run, `work` shall print each request with its status and whose turn it is.
- [r47] **When** `work list` is run, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.

Removed:
- [r13] **When** `work show` is run, `work` shall print each request with its status and whose turn it is.
- [r14] **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names.

## Glossary

No change.

## Decision

- spec/decisions/0072-work-list-and-work-show-replace-work-status.md: `work status` and `work show` are consolidated into `work list`, which lists all work (initiatives, requests and work-items) with its status, and `work show <id>`, which shows the detail of one initiative, request or work-item; `work status` is retired. source: the retired and new ids above and design-decision/the-context-runs-without-a-coordinator. by: the person's answers of 2026-10-27.

## Questions

1. `work show <request>` has no line. Is r37 the whole detail for a work-item? Readings: (A) add requests [r48] "**When** `work show <request>` is run, `work` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution." and keep r37 [recommended]; (B) the detail of a work-item is more (fields, plan, stage directories), r37 is replaced by a line naming them; (C) leave request and work-item detail to a later round.
2. migration-tools r32 (the SessionStart hook gives what `work status` prints for each open initiative; currently kept as committed). Readings: (a) retire r32, add [r35] "**When** a session starts in a repository with an initiative that is neither `done` nor `abandoned`, the plugin's SessionStart hook shall give the session what `work show <initiative>` prints for each such initiative." [recommended, keeps r32's per-initiative detail and the `next:` note]; (b) retire r32, add [r35] "... the plugin's SessionStart hook shall give the session what `work list` prints."
3. requests r47: observations are not among the things `work list` lists in the answer. Readings: (A) `work list` prints them, as r47 [recommended]; (B) retire r14 with no replacement under `work list` and name another command.
4. work-queue "Not yet" names `show --status`. Readings: (A) reword to `list --status` [recommended]; (B) leave it.
5. work-queue r34 and requests r46 both print each request's status under `work list`. Readings: (A) keep both as drafted; (B) retire r34 and add [r40] "**When** `work list` is run, `work` shall print each initiative and each work-item under `.shop/work/` with its status." [recommended].
6. The rule of the answers (a changed line is retired and replaced, never edited in place) differs from docs/capability-format.md ("A changed line keeps its id."). Readings: (A) draft a decision 0073-a-changed-line-is-retired-and-replaced [recommended]; (B) none.
