## Coverage

| id | line | scenario |
|---|---|---|
| r34 | "**When** `work list` is run, `work` shall print each initiative, each request and each work-item under `.shop/work/` with its status." | list prints each initiative, each request and each work-item under .shop/work/ with its status |
| r35 | "**Where** `--json` is given, `work list` shall print its result, each initiative, request and work-item with its status, as one JSON object." | list with --json prints each initiative, request and work-item with its status as one JSON object |
| r39 | "**While** a request that an initiative raised into an upstream is not `delivered`, `work list` shall print the initiative as waiting on that request." | list prints an initiative as waiting on a request it raised into an upstream while that request is not delivered |
| r36 | "**When** `work show <initiative>` is run, `work` shall print the initiative's status, each of its capability-proposals with its status, each of its work-items with its status and its open questions, the initiative branch and whether the remote has every commit of it, each tracked file of the checkout with uncommitted changes and each untracked file of the checkout that git does not ignore, the last ten lines of the initiative's ledger, and the ledger's last line whose note, the text given to `work note` after the date `work note` writes, begins `next:`." | show of an initiative prints where it stands, for a session to start from |
| r37 | "**When** `work show <work-item>` is run, `work` shall print the work-item's status and its open questions." | show of a work-item prints its status and its open questions |
| r38 | "**Where** `--json` is given, `work show` shall print its result as one JSON object." | show of <target> with --json prints its result as one JSON object (outline: i1, w1) |

r3, r11, r16, r17, r18 are retired; no scenario was written for them.

## Questions

None. Every new line has one reading.

## Cases no line mentions (no scenario written)

- r34/r35: whether `work list` prints capability-proposals. The line names only initiatives, requests and work-items. The retired r3 pinned "nothing about p1"; no new line says either way.
- r34: requests kept anywhere other than under `.shop/work/`, such as a request this context raised that is kept by its upstream.
- r35: whether the JSON of `work list --json` gives r39's "waiting on" a request. r35 names only each node with its status.
- r39: a request the initiative raised that is `refused` or `withdrawn`. It is not `delivered`, so read literally the initiative is printed as waiting on it for good.
- r39: a request the context raised to itself as its own upstream. By the Glossary's **request**, the context itself is then the upstream. The drafted scenario uses another context, ctx-up.
- r39: an `abandoned` initiative with a request upstream that is not delivered.
- r36: open questions on the initiative's capability-proposals. The line gives only each proposal's status.
- r36: an initiative with no initiative branch yet, no ledger, or no ledger line whose note begins `next:`.
- r36/r37: `work show` given a name that is neither an initiative nor a work-item, or that names both.
- r37: a work-item whose question has been answered. It has no open question, but the line does not say what is printed in that case.

## Drafts

- /home/vscode/shopsystem-bdd/.shop/worktrees/work-queue-9-formulate/.shop/scratch/9-formulate/drafts/round-1/work-queue.feature
