---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/conversation
title: Conversation
narrator: the person reading why a piece of work was asked for
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: []
---

# Conversation

## Purpose
A quote of the person links to the conversation it came from, and the turns around it can be shown: the person's and
the session's words, without tool output (design goal 9). A few turns around each quote are copied into `.shop/` and
committed, so that any clone or session can show them. The person reads names, not opaque ids: a hook gives the title
of every item and batch a session names (design goal 10).

## Terms
- **the UserPromptSubmit hook** (proper noun): the plugin's hook that runs when the person submits a prompt, and gives the session and its transcript to `work quote`.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| message | cited by | quote | |

## Behaviour

### [g1] `work quote` keeps the turns
- [r1] When a session runs `work quote`, `work` shall write a quote from the session that cites a message and commit
  the quote.

### [g2] The prompt hook gives the session and the transcript
- [r2] When the UserPromptSubmit hook runs `work quote --hook`, `work` shall keep the session.

### [g3] `work show` on a quote prints its messages
- [r3] When the person runs `work show` on a quote, `work` shall print every message cited by the quote.

### [g4] The names table at SessionStart
- [r4] When the SessionStart hook runs `work names`, `work` shall print every item, the title of the item and every
  batch.

## Implementation, may change

- A quote is the file `.shop/quotes/<n>.md`, named `quote-<n>`: its frontmatter holds the session id, the cited
  message's id and its date, and its body the person's words and then each message in a fence longer than any
  backtick run in its text.
- The words are matched, whitespace collapsed, against the person's messages of the session's transcript, the newest
  holding them cited, with the two messages before it and the two after it, of either side; a message is the
  person's prompt or the session's text of one turn, without tool uses, tool results, thinking, reminders,
  notifications, `!` bash-mode rows or interruption markers, a slash command read as `/<name> <args>`, and one other
  than the cited message is cut at 2,000 characters.
- `work quote "<words>"` prints the quote's label, `quote-<n> "<its words>"`, and commits the quote's file alone on the
  current branch; words that match nothing write nothing.
- The UserPromptSubmit hook runs `scripts/conversation_hook quote`, the same as `work quote --hook`, which writes the session and transcript of its stdin to
  `<git dir>/shopsystem/prompt.json`, never tracked, prints nothing and never fails; `work quote` reads its transcript
  from `--transcript`, else `--session` in any project of Claude Code's store, else that pointer.
- `work show quote-<n>` prints the quote's label, its session and date, then each of its messages with who wrote it,
  its time and the cited one marked `cited`; with `--json`, one object.
- `work names` prints one table of every item and then every batch, each with its name beside its id, a batch named
  by the labels of its items; the SessionStart hook runs `scripts/conversation_hook names`, the same as `work names --hook`, which prints the table under one line
  telling the session to name things by their names, prints nothing when there is nothing to name, and never fails.
- `scripts/conversation_hook` imports only the standard library and the conversation's modules, so the hooks run under
  any `python3`, and exits 0 whatever goes wrong.
