---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/brainstorming
title: Brainstorming
narrator: the person shaping work in a conversation
group: guarantees
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g3, r3]
unbuilt: []
---

# Brainstorming

## Purpose
Work comes in by a brainstorming with the person (design goal 4): a conversation that ends in shaped items whose
requirement lines are checked against the readiness bar, not in a long design document. The session writes the lines
and readies the items; the person may skim the lines in the backlog and in the pull request, and nothing waits on that
reading. The person's words an item cites keep the conversation turns around them.

## Terms
- **the brainstorming session** (proper noun): the session in which the person and Claude shape work into items. Kind of: session.
- **shape** (verb, action): a session writes an item's requirement lines with the person. Forms: shapes, shaped. Frame: session shapes item.
- **quote** (verb, action): a session takes words of a message into a file it writes, as said in the message. Forms: quotes, quoted. Frame: session quotes message.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| message | of | agent | one |

## Behaviour

### [g2] Nothing waits on the person's reading
- [r2] When the brainstorming session runs `work ready` on an item, the brainstorming session shall not ask a
  question.

### [g4] Lines are written and readied
- [r4] When the brainstorming session shapes an item, the brainstorming session shall write a requirement that the item proposes and run `work ready` on the item.

### [g5] A quote keeps its turns
- [r5] When the brainstorming session quotes a message of the person, the brainstorming session shall run `work quote` on the message.
