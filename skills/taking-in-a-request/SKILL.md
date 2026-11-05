---
name: taking-in-a-request
description: Use when a request from a peer bounded context or the product is open or awaiting the upstream in this repository's `.shop/requests/`, and is to be answered here. Not for this repository's own requests to its upstream, which are kept in the same folder and taken in there. Also use when a peer's request is to become an item of the backlog, or when its asker has answered a counter-proposal.
---

# Taking In a Request

## Overview

Work from outside the bounded context comes in by a negotiation with another system, not with a person. A peer or the product proposes lines; this session answers each one: accept it into a capability of the item, refuse it with a reason, or counter-propose a line. The exchange repeats until the item is ready or refused. No person is asked.

Scripts: `<this skill's base directory>/../../scripts/`. The request's lines are judged against `spec/` and this context's glossary (`python3 <scripts>/model lexicon`).

## Process

1. **Take it in.** `python3 <scripts>/work intake q<n>` writes a `shaped` item asked by the request's asker, and changes nothing in the request. A request already taken in names its item; carry on with that item.
2. **Answer each line**, judged against `spec/`:
   - it belongs to a capability here: `python3 <scripts>/work outcome q<n> <k> accepted --into <capability>`, which writes it into the item's lines (`--group "<title>"` for a group of its own);
   - it is not this context's to do: `python3 <scripts>/work outcome q<n> <k> refused --reason "<why>"`;
   - it is nearly right: `python3 <scripts>/work outcome q<n> <k> rewritten --line "<the counter-proposal>"`, written as raising-a-request's steps 1-4 say (it must parse in this context's grammar); this passes the turn to the asker. The rewritten line is written under the request's `## Counter-proposals`, so once its counter-proposal is settled `work turn` can close the request.
3. **Pass the turn** with `python3 <scripts>/work turn q<n>` when every line has an answer and no counter-proposal did so already.
4. **Ready the item** once every line is settled: `python3 <scripts>/work ready <b>`. On a refusal, answer the lines it names, or reword the accepted lines it names by editing their `- [r<n>]` bullets in the item's `## Requirements` (same id) and committing the item (no command rewords a line yet, and `work line` only adds one), and run it again.
5. **When every line is refused**, the item has no requirement line and is never passing: refuse it with `python3 <scripts>/work refuse <b> "<why>"`.
6. **When the two sides cannot agree** (a counter-proposal is itself rewritten by the asker), stop: name the request and the line, `line <k> of request q<n>`, to the person in the session's last message.

## Red Flags

| Seen | Fix |
|---|---|
| `work intake` on this repository's own request to its upstream | It is refused: the upstream takes it in |
| A question put to the person about a line | Judge it against `spec/`: accept, refuse with a reason or counter-propose |
| A line accepted with no `--into` | It goes into one capability of the item |
| A refusal with no reason | `--reason`: the asker reads it |
| A counter-proposal that does not parse | Write it as raising-a-request says; `work outcome` refuses it otherwise |
| `work ready` run while a line is unanswered | Answer every line first (step 2) |
