---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/brainstorming
title: Brainstorming
narrator: the person shaping work in a conversation
group: guarantees
language: codified-1
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: []
unbuilt: []
---

# Brainstorming

## Purpose
Work comes in by a brainstorming with the person (design goal 4): a conversation that ends in shaped items whose
requirement lines are checked against the readiness bar, not in a long design document. The session writes the lines
and readies the items; the person may skim the lines in the backlog and in the pull request, and nothing waits on that
reading. The person's words an item cites keep the conversation turns around them.

## Terms
- **the brainstorming session** (actor): the session in which the person and Claude shape work into items. Kind of: session.

## Behaviour

### [g1] Lines are written and readied
- [r1] When the brainstorming session writes an item, the brainstorming session shall write a requirement proposed by
  the item and use `work ready`.

### [g2] Nothing waits on the person's reading
- [r2] When the brainstorming session runs `work ready` on an item, the brainstorming session shall not ask a
  question.

### [g3] A quote keeps its turns
- [r3] When the brainstorming session writes a quote, the brainstorming session shall use `work quote`.
