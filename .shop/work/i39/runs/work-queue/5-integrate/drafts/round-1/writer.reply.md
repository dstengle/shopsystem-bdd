/home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-5-integrate/.shop/scratch/5-integrate/drafts/round-1/spec/capabilities/work-queue.md
/home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-5-integrate/.shop/scratch/5-integrate/drafts/round-1/spec/capabilities/requests.md
/home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-5-integrate/.shop/scratch/5-integrate/drafts/round-1/spec/decisions/0072-work-list-and-work-show-replace-work-status.md

## Change list

### work-queue (frontmatter and Behaviour drafted; retired: [r2, r3, r11, r16, r17, r18, r33]; rests_on gains design-decision/work-list-and-work-show-replace-work-status)

| change | capability | id | line | source |
|---|---|---|---|---|
| removed | work-queue | r3 | **When** `work show` is run, `work` shall print each work-item of every initiative under `.shop/work/` with its status. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2) |
| removed | work-queue | r11 | **Where** `--json` is given, `work show` shall print its result, each work-item with its initiative and status, as one JSON object. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2) |
| removed | work-queue | r16 | **When** `work status <initiative>` is run, `work` shall print the initiative's status, ... begins `next:`. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2) |
| removed | work-queue | r17 | **When** `work status` is run with no initiative, `work` shall print what r16 gives for each initiative that is neither `done` nor `abandoned`. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2) |
| removed | work-queue | r18 | **Where** `--json` is given, `work status` shall print its result as one JSON object. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2) |
| removed | work-queue | r33 | (the dropped draft's line, never applied) **While** a request that an initiative raised into an upstream is not `delivered`, `work status` shall print the initiative as waiting on that request. | "r33 is retired and replaced by: ..." (answer 2) |
| added | work-queue | r34 | **When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status. | "work list lists all work with its status (initiatives, requests and work-items)" (answer 2); replaces r3 and r17 |
| added | work-queue | r35 | **Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2); r11's content kept, worded for `work list` |
| added | work-queue | r39 | **While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request. | "r33 is retired and replaced by: '**While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request.'" (answer 2); also "r33: Reading (C), reworded to name the consolidated list action that replaces work status." (answer 1) |
| added | work-queue | r36 | **When** `work show <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`. | "work show <id> shows the detail of one initiative, request or work-item" (answer 2); r16's content kept |
| added | work-queue | r37 | **When** `work show <work-item>` is run, `work` shall print the work-item's status and its open questions. | "work show <id> shows the detail of one initiative, request or work-item" (answer 2); the detail is what r16 gave for each work-item (see question 1) |
| added | work-queue | r38 | **Where** `--json` is given, `work show` shall print its result as one JSON object. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2); r18's content kept, worded for `work show` |

Unchanged in work-queue: Purpose, Implementation, Not yet (see the mentions below).

### requests (frontmatter and Behaviour drafted; retired: [r6, r1, r3, r13, r14]; rests_on gains design-decision/work-list-and-work-show-replace-work-status)

| change | capability | id | line | source |
|---|---|---|---|---|
| removed | requests | r13 | **When** `work show` is run, `work` shall print each request with its status and whose turn it is. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2) |
| removed | requests | r14 | **When** `work status` is run with no initiative, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2) |
| added | requests | r46 | **When** `work list` is run, `work` shall print each request with its status and whose turn it is. | "work list lists all work with its status (initiatives, requests and work-items)" (answer 2); r13's content kept |
| added | requests | r47 | **When** `work list` is run, `work` shall print, with its date, each observation that the `source` of no initiative and of no request names. | "work status is retired, its lines retired and replaced by lines naming work list or work show." (answer 2); r14's content kept (see question 3) |

### migration-tools
Not drafted: r32's replacement has two readings (question 2). r32 stands as committed until the answer; retired list unchanged ([]).

### Glossary
No change: no entry of `spec/index.md`'s Glossary names `work status` or `work show`.

## Decision files

| path | summary | source | by |
|---|---|---|---|
| spec/decisions/0072-work-list-and-work-show-replace-work-status.md | `work status` and `work show` are consolidated into `work list`, which lists all work (initiatives, requests and work-items) with its status, and `work show <id>`, which shows the detail of one initiative, request or work-item; `work status` is retired. | capability/work-queue#r3, #r11, #r16, #r17, #r18, #r33, capability/requests#r13, #r14, capability/work-queue#r34-#r39, capability/requests#r46, #r47, design-decision/the-context-runs-without-a-coordinator | "the person's answers of 2026-10-27 to the question against spec/capabilities/work-queue.md (answers 1 and 2)" |

No `supersedes`: 0072 replaces only what 0068 says of `work status`, which it says in its Decision, the way 0068 itself replaced one sentence of design-decision/a-script-supervises-delivery. 0068 is not edited. migration-tools#r32 and its replacement are not in `source` yet; they join it when question 2 is answered.

## Mentions of `work status` / `work show` not changed

- spec/decisions/0068-the-context-runs-without-a-coordinator.md, the summary and the Decision ("The person's surface is `work status`, `work answer`, ..."): not edited; 0072 replaces it.
- spec/decisions/index.md line 75 (0068's summary): generated; it changes only when `model decisions` writes it with 0072.
- spec/capabilities/migration-tools.md r32: pending question 2.
- spec/capabilities/work-queue.md Not yet, "`show --status`": names the old `work show` listing's filter; with r34 the listing is `work list`, so it would read `list --status`. Not changed (the answers do not mention it); see question 4.
- spec/capabilities/work-queue.md Purpose, "it drafts work-items, shows them ... it prints where an initiative stands": names neither command; left as it is.
- spec/capabilities/requests.md r25, "(raise, take in, give a line outcome, ask, answer, pass the turn, resolve and show)": "show" is the verb of the command set, which `work show <request>` fills; not changed.
- features/ (formulation's to change, not this round's): features/work-queue.feature lines 105, 114, 194 (`work show`, `work show --json`), 357, 373-374, 381 (`work status i1`, `work status`, `work status i1 --json`); features/requests.feature 332 (`work show`), 342 (`work status`); features/migration-tools.feature 544, 549 (`work status` in the SessionStart scenario); features/supervision.feature 310 (`python3 {scripts}/work show` in the implementer's refused-commands table).
- docs/: none.

## Questions

1. work-queue / requests: what does `work show <request>` print, and is r37's detail for a work-item complete? Answer 2 says `work show <id>` "shows the detail of one initiative, request or work-item" but gives the detail only by way of r16 (for an initiative). r37 takes for a work-item what r16 gave for each of its work-items. For a request no line is written. If yes, add to requests: `[r48] **When** \`work show <request>\` is run, \`work\` shall print the request's status, whose turn it is, its lines with their line outcomes, its questions, its answers and its resolution.` If a work-item's detail is more (its fields, its plan, its stage directories), r37 is retired and replaced by a line naming them.
2. migration-tools r32 (SessionStart hook) has two readings. (a) The hook keeps what it gave per open initiative, now named by `work show`: retire r32, add `[r35] **When** a session starts in a repository with an initiative that is neither \`done\` nor \`abandoned\`, the plugin's SessionStart hook shall give the session what \`work show <initiative>\` prints for each such initiative.` (b) `work list` is "the consolidated list action that replaces work status" (answer 1), so the hook gives the list: retire r32, add `[r35] **When** a session starts in a repository with an initiative that is neither \`done\` nor \`abandoned\`, the plugin's SessionStart hook shall give the session what \`work list\` prints.` (Reading (a) keeps r32's "for each such initiative" and the ledger's `next:` note the session starts from; reading (b) gives every initiative, done ones included, with only its status.)
3. requests r47: answer 2's `work list` lists "initiatives, requests and work-items"; observations are not named. r47 keeps r14 (observations no initiative or request names) under `work list`. If they are not `work list`'s, retire r14 with no replacement under `work list`, and say which command prints them.
4. work-queue Not yet: "`show --status`" filtered the old `work show` listing. If it now filters `work list`, the entry becomes "`list --status`".
5. work-queue r34 and requests r46 both print each request's status under `work list` (the form asked for "work list prints every initiative, request and work-item with its status" in work-queue and "requests with their status and whose turn it is" in requests). If one capability should own a request's status, r34 is retired and replaced by `[r40] **When** \`work list\` is run, \`work\` shall print each initiative and each work-item under \`.shop/work/\` with its status.`
6. Answer 3 ("a requirement line is never edited in place; a change retires the original id ... and adds a replacement with a new id") applied in this round. It differs from docs/capability-format.md ("A changed line keeps its id."). Should it be a decision of its own, superseding that rule, e.g. `spec/decisions/0073-a-changed-line-is-retired-and-replaced.md`, summary "A requirement line is never edited in place: a change retires its id into the capability's `retired` list and adds a replacement with a new id."?

## Cut sentences

None. Answer 1's first sentence lands in work-queue r39; its second ("work show and work status are consolidated into one action listing all work with its status and one showing the detail of an individual item.") in decision 0072; answer 2 in r34-r39, requests r46-r47 and decision 0072; answer 3 in question 6.
