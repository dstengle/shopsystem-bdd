---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-05-b26-github-blackbox
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# b26 on real GitHub: the opt-in test and a black-box run

b26 "Requests exchanged through GitHub issues" was tested against GitHub before batch-1's pull request (#17) was
merged, at the person's request. Every test had run on the stand-in gh until then.

## Setup

- A private scratch repository, `dstengle/shopsystem-request-sandbox`, made for these tests at the person's choice.
  It is kept for later runs.
- The code is the batch branch `batch-1` at its reviewed head, run from the task worktree's `scripts/`, with
  `GH_TOKEN` and `$SHOPSYSTEM_WORK_GH` unset, so the real gh is used under its own login.
- There are two throwaway contexts in the session's scratch directory:
  - the upstream: a clone of `batch-1` (this context's real spec), its `origin` set to the sandbox;
  - the downstream: a minimal `bb-down` whose `## Upstreams` names shopsystem-bdd with
    `github: dstengle/shopsystem-request-sandbox`.

## The opt-in test

`SHOPSYSTEM_TEST_GITHUB_REPO=dstengle/shopsystem-request-sandbox python3 -m pytest -q -n0
tests/scripts/test_request_github.py` passed, in 11.9 s. Issue #1 holds its ask, offer, the asker's turn, the
upstream's turn, accept and resolve, and was closed.

## The black-box run, by hand

| path | issue | what was run | result |
|---|---|---|---|
| negotiation | #2 | request, sync both sides, offer `backlog`, propose two lines, turn, outcome accepted on a line outside the lexicon, outcome rewritten, ask, reply, outcome accepted, outcome refused with a reason, turn, accept, resolve, sync | as specified: the line outside the lexicon was refused with its parse hint (r38). The turn with every line settled and one accepted kept the upstream's turn (r36). `work accept` wrote a `shaped` item with provenance `peer`, `asked_by` the downstream, and only the accepted line under `backlog` (r39). Resolve closed the issue, and the downstream synced to `delivered` with the resolution (r41) |
| unreadable comments | #3 | a comment whose block has a line that is no field, and a comment with no block, posted by hand with gh; then sync | both printed with the reason and not recorded, and the record unchanged (r33) |
| sync twice | #3 | sync, then sync again | nothing recorded twice. A comment posted seconds before a sync was not listed by GitHub yet; the next sync took it |
| fits | #3 | offer, sync, `work fits --serves backlog#r15`, sync | both sides `delivered`, the issue closed (r30) |
| every line refused | #4 | propose one line, outcome refused, turn | `refused` on both sides, the issue closed (r37) |
| unhosted | none | `github:` taken out of the downstream's `## Upstreams`, then request | refused, naming the upstream and the fix, and nothing written (r28) |

Every issue the run opened (#1-#4) is closed.

## What it showed beyond the lines

- A counter-proposal passes the turn at once (intake r7), so the upstream cannot settle or ask about the other lines
  in the same turn. In the run, `work ask` on line 2 was refused after line 1 was rewritten. This is now
  b38 "The upstream settles every line in one turn, a counter-proposal included".
- These are now b39 "Requests' output: reasons shown, unreadable comments once, one-line confirmations":
  - `work show` does not print a refused line's reason, though the asker's record holds it under `## Reasons`;
  - `work sync` prints each unreadable comment again on every run, also on delivered requests;
  - `offer`, `propose`, `turn` and `reply` print nothing on success;
  - `work request --from` is required, though it can only be this context.
- `work offer` pastes the whole capability file, frontmatter and `given` blocks included, which makes one long
  comment. This is now b40 "An offer quotes a capability's lines, not its raw file".
- `work resolve` is taken right after `work accept`, before the item is built. The lines allow it; b6
  "Resolve the delivered item's request at the merge" covers doing it at delivery.
- Not tried here: a hostile comment with a well-formed block, which review 1 showed `sync` applies (b35).
