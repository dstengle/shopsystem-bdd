---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/backlog
title: Backlog and temporary rules
narrator: a person or session keeping the bounded context's ideas, observations and temporary rules
group: service
rests_on: [design-decision/requests-written-through-work]
retired: []
---

# Backlog and temporary rules

## Purpose
The backlog and the log of temporary rules keep, in the repository, the ideas, observations and rules the person
gives a session outside an initiative, each with its date and the person's words. An item of the backlog becomes
work only through a request a session raises from it after a discovery discussion with the person; a rule of the
log of temporary rules is given to each session at its start until the person moves it to the backlog. Neither is
a request, an initiative or a proposal, and neither is changed by `work run`.

## Behaviour
- [r1] The bounded context shall have a backlog of ideas and observations, kept in the repository.
- [r2] **When** the person gives a session an idea or an observation outside an initiative, the session shall add it to the backlog in the same turn, with its date and the person's words.
- [r3] **While** an item of the backlog has had no discovery discussion with the person, the plugin shall draft no request and no proposal from it.
- [r4] **When** the person and a session have held a discovery discussion on an item of the backlog, the session shall raise a request from it, naming the item as its source.
- [r5] The bounded context shall have a log of temporary rules that the person gives its sessions, kept in the repository.
- [r6] **When** the person gives a session a rule outside an initiative, the session shall add it to the log of temporary rules in the same turn, with its date and the person's words.
- [r7] **When** the person rules that a rule of the log of temporary rules moves to the backlog, the session shall move it from the log of temporary rules to the backlog.
- [r8] The session shall keep each rule, idea and observation of the bounded context in the repository.

## Implementation, may change
- None given yet: where the backlog and the log of temporary rules are kept, and their form.

## Not yet
- None.
