---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/conversation
title: Conversation
narrator: the person reading why a piece of work was asked for
group: service
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: [r1, r2, r3, r4]
---

# Conversation

## Purpose
A quote of the person links to the conversation it came from, and the turns around it can be shown: the person's and
the session's words, without tool output (design goal 9). A few turns around each quote are copied into `.shop/` and
committed, so that any clone or session can show them. The person reads names, not opaque ids: a hook gives the title
of every item and batch a session names (design goal 10).

## Terms
- **the UserPromptSubmit hook** (actor): the plugin's hook that runs when the person submits a prompt, and gives the session and its transcript to `work quote`.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| message | cited by | quote | |

## Behaviour

### [g1] `work quote` keeps the turns
- [r1] When a session runs `work quote`, `work` shall write a quote from the session that cites a message and commit
  the quote.

### [g2] The prompt hook gives the session and the transcript
- [r2] When the UserPromptSubmit hook runs `work quote --session --transcript`, `work` shall write a quote from a
  session.

### [g3] `work show` on a quote prints its messages
- [r3] When the person runs `work show` on a quote, `work` shall print every message cited by the quote.

### [g4] The names table at SessionStart
- [r4] When the SessionStart hook runs `work names`, `work` shall print every item, the title of the item and every
  batch.

## Implementation, may change

- A quote keeps the person's words with its session id and its message, and the two messages before it and the two
  after it, the person's and the session's, without tool uses, under `.shop/`.
- `work quote --session <id> --transcript <path>` is how the UserPromptSubmit hook passes them.
- `work names` is the SessionStart hook's table of the items' and batches' names beside their ids.
