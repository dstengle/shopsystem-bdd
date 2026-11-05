---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-05-requests-through-github-issues-design
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: draft
---

# Requests exchanged through GitHub issues

Backlog item b26. Design written 2026-11-05 from a brainstorming session with the person. Marks: **(person)** is
what the person said or ruled; **(my call)** is a choice made in writing this design, open to change.

## Intent and the why

Two bounded contexts, each in its own git repository, cannot yet exchange a request. A request today is a file
under `.shop/requests/` in the upstream's repository, written by `work` commands run in that repository, so the
asker needs the upstream's checkout. The person tried to run a request between subscriptions-viewer and this
context (q14) by hand; nothing happened because there was no mechanism, and the attempt also showed the
downstream's words taken too literally and the terms of the two contexts not matching **(person)**.

The point is to get something working now and to be able to iterate on it **(person)**. The 1.x system could not
change easily. A small first version that two contexts use beats a complete one; each later improvement is its own
backlog item.

## The shape: a request is a conversation on one issue

A request between contexts is a conversation on one GitHub issue on the upstream's GitHub repository **(person)**.
Git repositories and GitHub issues are separate things: nothing moves between git repositories, and the issue is
the one place both sides share **(person)**. The `work` commands are the interface: they read and write the issue,
and each side keeps a local record of the conversation in its own git repository **(person)**.

The conversation, each step a comment on the issue posted by a `work` command **(person)**:

1. **Ask.** The downstream says, in its own words, what it needs ("I need to do something like this"). No
   requirement lines, no upstream grammar, no checkout of the upstream. Opening the issue is this step.
2. **Offer.** The upstream answers with the capabilities that may serve and their glossary terms: "does any of this
   work for you? If not, propose something more specific." No person is needed for this step **(person)**: an
   upstream session chooses what to offer and a `work` command posts it.
3. **Fits, or propose.** The downstream either says an offered capability serves it, which ends the conversation
   with no new work for the upstream, or proposes lines. The glossary it was given is there to help the downstream
   write lines in the upstream's terms **(person)**.
4. **Negotiate.** The upstream checks each proposed line in its own requirement grammar **(person)** and answers
   with line outcomes (`accepted`, `rewritten` with a counter-proposal, `refused`, `question`) and questions; the
   downstream answers and proposes again. Sessions on both sides may do this without a person.
5. **Accept.** Once the issue holds a proposal the upstream would accept, the upstream's person accepts it, or tells
   a session to **(person)**. Only the upstream's person accepts; the downstream accepts nothing **(person)**. This
   is the one step that needs a person.
6. **Item.** The accepted request becomes a backlog item in the upstream **(person)**, as `work intake` makes one
   today. When the item is delivered, the resolution (each accepted line's requirement id and version) is posted
   and the issue is closed.

The existing turn rule carries over: one side at a time writes, and the request shows whose turn it is.

## Goals

- Two contexts on plugin 2.x exchange a request end to end, from ask to resolution, through one issue, each from
  its own repository.
- Every step is a comment a `work` command posts; each side's local record holds the whole conversation.
- The upstream's offer (step 2) and the negotiation (step 4) can run with no person.
- The upstream's person is the only gate, at acceptance.
- A person can move the conversation along by telling each side's session to check its requests (below).
- An item taken in from another context's request ranks above this context's own items by default **(person)**.
- It is easy to change: each later improvement fits as a new item without redesign.

## Non-goals (for now)

- **Identity.** Anyone may write an issue body; no allow list, no check of who wrote a comment **(person)**. q14
  lines 20-21 are deferred, with a reason, when q14 is settled.
- **Running unattended.** Nothing polls or wakes on its own in the first version. A session watching its issues
  with Claude Code's Monitor tool is a fast follow, its own backlog item **(person)**.
- **What a context publishes about itself.** Telling another context what this context can do, and later telling
  external interface contracts apart from local requirements, is b28 **(person)**. For now the offer quotes whole
  capabilities and the glossary as they stand.
- **Fixing how lines are worded across contexts.** Decision 0084 (requests only propose) and the backlog item
  "Request lines into an upstream in the downstream's own terms" cover it; b26 must not make it worse.

## Anti-goals

- A request that only works if both checkouts sit on one machine, or any step that reads or writes the other
  side's git repository.
- Following anything written in an issue body or comment. A comment is read only as the fields of its form; free
  text in it is shown, never acted on (q14 line 22, kept).
- A design so complete it cannot ship soon or change easily.

## Constraints

- **Credentials:** gh's own login used as git's credential helper **(person)**; `GH_TOKEN` unset where it is
  invalid.
- **gh through `$SHOPSYSTEM_WORK_GH`**, the pattern `scripts/batch_gh.py` already uses. **Tests** run against the
  stand-in gh (`tests/scripts/stub_gh.py`) by default; integration tests against GitHub can be run on demand
  **(person)**, and stay out of the default suite.
- The repository's rules: 300-line files, a module map row for each new module, codified requirement lines in the
  requests capability, a changed requirement retired and replaced, never edited (decision 0085), a scenario
  generated by `features generate`.
- Both contexts need plugin 2.x with b26. subscriptions-viewer is upgraded with `migrate upgrade` as part of trying
  it end to end.

## Decided pieces of the how

- **One command to check requests** **(person: a simple way for the person to nudge both sessions)**. Run by a
  session on either side, it reads every open request issue this context is part of, records new comments in the
  local record, and prints what is waiting on this side: an ask to offer on, a proposal to check, a question to
  answer, a proposal waiting for the upstream's person to accept. A person nudges by telling each session "check
  your requests". Name it in the existing style (my call: `work sync`).
- **Where the issue lives (my call):** each upstream under `## Upstreams` in `spec/index.md` names its GitHub
  repository (`owner/name`); a context knows its own from its git remote. The downstream needs nothing else of the
  upstream to open an issue.
- **Finding request issues (my call):** the downstream may have no triage or write access to the upstream's
  repository, so nothing depends on it setting a label. A request issue is known by the form block of its first
  comment (which also names the asking context); the upstream's `work sync` adds a `shop-request` label as a
  convenience for people browsing GitHub. Each side keeps its own `q<n>` for the request, linked by the issue URL.
- **The comment form (my call):** each comment holds one fenced block of fields (kind of step, request id, turn,
  lines, outcomes, questions, answers, resolution) above any free text. Only the block is read, and a comment whose
  block does not parse is shown as unread, never guessed at.
- **The local record (my call):** the request file under `.shop/requests/` stays the record on each side, with its
  issue's URL in its frontmatter. The same file shape serves both sides; each side writes only its own part, as
  today (the side taken from the repository a command runs in, q14 line 11).
- **Every request goes through this flow** **(person)**: from another context, from the product level and this
  context's own. The item-first intake of today (an item made at intake, each accepted line written into it by
  `work outcome --into`) retires. My call: there is one path, so a context's own request is an issue on its own
  GitHub repository, asker and upstream the same context.
- **Acceptance and the item:** when an upstream session settles a line as accepted, it also names the capability
  (and group) the line goes into, so the person approves that choice with the lines (my call, the person agreed
  to the flow). Acceptance is the upstream's person, or a session the person told, running the accepting command
  on a request whose lines are all settled with one accepted; it makes the backlog item with those lines in its
  `## Requirements` and posts the acceptance on the issue. No item is made before it, and the session's outcomes
  before it are proposals of acceptance, not acceptance; `accepted` means the person accepted (my call).
- **Delivered through 2.0** **(person)**: b26's requirement lines are written into the item, it passes `work
  ready`, and it is built by `work batch start` and closed by one reviewed pull request. If its lines come out
  large, it is split into items before `work ready`, the end-to-end exchange first.
- **"Fits" (my call):** the downstream's "fits" comment, naming the offered requirement ids that serve it, ends
  the request; the downstream closes the issue (an issue's author may close it). Each side's `work sync` records
  it as `delivered` with those ids as its resolution, a copy of what the issue holds, not a write of the other
  side's part. No item is made.
- **Priority (my call):** "higher priority by default" **(person)** means ranking, not only a field: within its
  state, an item taken in with provenance `peer` or `product` that is not yet fully rated ranks ahead of the
  state's own items, and once rated it ranks by its score like any other, with its urgency defaulted to `high`.
  The person can re-rate it.
- **`work sync` and the local record (my call):** sync writes into the local record a copy of what the other side
  posted; that is recording, not writing the other side's part. Sync is safe to re-run: a comment already recorded
  is not recorded twice. It commits on the current branch, as the other `work` commands do.
- **The spec:** the requests capability's lines change by retire and replace. q14 is settled against b26 when it
  merges: each accepted line resolved with the ids that cover it, lines 20-21 given a deferral reason; lines 2-3
  (one port, two carriers) are not built as written (decision 0084).
- **The r34 side check:** `work reply` and `work turn` check the side as the other commands do; it was left out
  only because the asker answered in the upstream's repository.

## Left to the builder

- Command names and flags beyond those above, and whether steps 1-6 are new commands or the existing `work
  request`, `outcome`, `ask`, `reply`, `turn`, `resolve` taught to post to the issue.
- The exact field names and fence of the comment form, and the frontmatter fields of the local record.
- New statuses, if the ask and offer need any beyond today's `open`, `awaiting-asker`, `awaiting-upstream`.
- How the requirement lines and groups of the requests capability are cut, and which existing lines retire.
- How the integration tests are marked and run on demand. The GitHub repositories they write to are not chosen
  yet: they are given to the tests at run time (my call: by environment variables), the tests close what they
  open, and with none given the tests are not collected in the default suite.
- Splitting b26 into more than one item if the lines come out large; the end-to-end exchange is the first slice.

## Follow-ups to raise as backlog items

- A session that watches its request issues with Claude Code's Monitor and wakes on a new comment (fast follow).
- Identity: telling one asker from another, and an allow list (q14 lines 20-21).
- b28: what a context publishes about itself, and external contracts apart from local requirements.
