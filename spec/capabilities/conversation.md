---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/conversation
title: Conversation
narrator: the person reading why a piece of work was asked for
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g2, r2, g3, r3, g4, r4, g1, r1, g6, r6, g7, r7, g8, r8, g9, r9, g16, r16, g10, r10, g11, r11, g12, r14, g13, r12, g14, r13, g15, r15]
---

# Conversation

## Purpose
A quote of the person links to the conversation it came from, and the turns around it can be shown: the person's and
the session's words, without tool output (design goal 9). A few turns around each quote are copied into `.shop/` and
committed, so that any clone or session can show them. The person reads names, not opaque ids: a hook gives the title
of every item and batch a session names (design goal 10).

## Terms

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Relations

Moved to `spec/vocabulary/` and `spec/model/` (the domain contract, 0.38.0).

## Behaviour

## Implementation, may change

- A quote is the file `.shop/quotes/<n>.md`, named `quote-<n>`: its frontmatter holds the session id, the cited
  message's id and its date, and its body the person's words and then each message in a fence longer than any
  backtick run in its text.
- The words are matched, whitespace collapsed, against the person's messages of the session's transcript, the newest
  holding them cited, with the two messages before it and the two after it, of either side; a message is the
  person's prompt, a queued message (Claude Code's `attachment` row of a `queued_command` whose `commandMode` is
  `prompt` and whose origin is `human`, closing the session's turn as a prompt does; a subagent's hand-back or a task
  notification of that shape is none) or the session's text of one turn, without tool uses, tool results, thinking, reminders,
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
- A directive is the file `.shop/directives/<n>.md`, named `directive-<n>`: its frontmatter holds its status, its
  date, the quote it cites and, once promoted, `promoted_to` (`b<n>`, a design-decision's id or `CLAUDE.md`); its body
  the person's words and, once dropped, the reason under `## Why dropped`. `work directive "<words>"` writes the
  quote as `work quote` does and the directive in one commit; `work directive --quote quote-<n>` one of a kept quote.
- `work directives` prints the live directives with id, date, age and words (`--all` every one); the SessionStart hook
  runs `scripts/conversation_hook directives`, the same as `work directives --hook`, which prints each live
  directive's quote and words under one line telling the session to follow them and pass them on in every brief,
  prints nothing with none, and never fails. A live directive is shown until it is reviewed; none expires.
- `work promote directive-<n> --to <target>` is refused when the directive is not live or the target does not exist;
  `work drop directive-<n> --why "<reason>"` when it is not live.
- `scripts/conversation_hook` imports only the standard library and the conversation's modules, so the hooks run under
  any `python3`, and exits 0 whatever goes wrong.
## Moved

Every line moved to a new capability with a new id (the domain contract, 0.38.0).

| old | new |
|---|---|
| g1 | quotes#g1 |
| r1 | quotes#r1 |
| g6 | quotes#g2 |
| r6 | quotes#r2 |
| g7 | quotes#g3 |
| r7 | quotes#r3 |
| g8 | items#g29 |
| r8 | items#r29 |
| g9 | quotes#g4 |
| r9 | quotes#r4 |
| g16 | directives#g1 |
| r16 | directives#r1 |
| g10 | directives#g2 |
| r10 | directives#r2 |
| g11 | directives#g3 |
| r11 | directives#r3 |
| g12 | directives#g4 |
| r14 | directives#r4 |
| g13 | directives#g5 |
| r12 | directives#r5 |
| g14 | directives#g6 |
| r13 | directives#r6 |
| g15 | directives#g7 |
| r15 | directives#r7 |
