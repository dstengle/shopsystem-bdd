---
id: model/example.org/notes/sharing/sharing
area: sharing
kind: core
imports: [notebook]
---

# sharing

## Purpose

The invitations an owner sends to a colleague to read a note, and their answers.

```model
object invitation
  attributes: address (text); status: sent | accepted | declined | withdrawn
  lifecycle status: sent → accepted; sent → declined; accepted → withdrawn; sent → withdrawn
  relations: has → note (one)

service sharing
  operation share(note, address)  outcomes: done → the invitation | refused: no address
  operation accept(invitation)  outcomes: done | refused: withdrawn invitation
  operation decline(invitation)  outcomes: done
  operation withdraw(invitation)  outcomes: done

actor the owner kind of agent
actor the colleague kind of agent
```
