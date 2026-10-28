---
id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/i57-backlog
kind: capability-proposal
part_of: initiative/missingmass.io/shopsystem/shopsystem-bdd/i57
status: awaiting-answer
argues: [backlog]
adds: [backlog#r1, backlog#r2, backlog#r3, backlog#r4, backlog#r5, backlog#r6, backlog#r7, backlog#r8]
changes: []
removes: []
date: 2026-10-28
---

# backlog

The drafts of this proposal are in .shop/work/i57/runs/i57/1-integrate/drafts/round-1/.

## Questions
- Q1 (backlog r2, term/backlog): 'observation' is already a record kind (.shop/records/observations/). Is an observation of the backlog such a record?
  Line: [backlog#r2] **When** the person gives a session an idea or an observation outside an initiative, the session shall add it to the backlog in the same turn, with its date and the person's words.
  Readings: (a) Yes, recommended: r2 becomes '...add it to the backlog as an observation record in the same turn...'. (b) No: term/backlog (new: 'the bounded context's ideas and observations that the person gives its sessions outside an initiative, kept in the repository, each with its date and the person's words') notes an observation of the backlog is not an observation record; lines as drafted.
- Q2 (backlog r2, r6): 'in the same turn' - 'turn' is a glossary term for a request's side.
  Lines: [backlog#r2] (above); [backlog#r6] **When** the person gives a session a rule outside an initiative, the session shall add it to the log of temporary rules in the same turn, with its date and the person's words.
  Readings: (a) Reply to the person's message, recommended: '...before its reply to that message ends...'. (b) Keep as drafted.
- Q3 (backlog r3, r4): is 'discovery discussion' a glossary term?
  Lines: [backlog#r3] **While** an item of the backlog has had no discovery discussion with the person, the plugin shall draft no request and no proposal from it. / [backlog#r4] **When** the person and a session have held a discovery discussion on an item of the backlog, the session shall raise a request from it, naming the item as its source.
  Readings: (a) Yes, recommended: add entry '- **discovery discussion**: a discussion between the person and a session on one item of the backlog, after which a request may be raised from it.' (b) No: say what marks an item as having had one (to be answered).
- Q4 (backlog r4): does each backlog item have an id (requests take ids as origins)?
  Line: [backlog#r4] (as in Q3).
  Readings: (a) Yes, recommended: new line r9 'The session shall give each item of the backlog an id when it adds it.' (b) No: `work request` needs another way to take a non-id origin (a request into requests).
- Q5 (backlog r3): what does 'no proposal' cover?
  Line: [backlog#r3] (as in Q3).
  Readings: (a) Capability- and glossary-proposals both, recommended: '...draft no request, no capability-proposal and no glossary-proposal from it.' (b) Only capability-proposals.
- Q6 (migration-tools r36 against r24 and r28, which say the hook tells nothing when there is no pending step, no open initiative, or no .shop/):
  Lines: [migration-tools#r35] **When** a session starts, the plugin's SessionStart hook shall give the session no item of the backlog. / [migration-tools#r36] **When** a session starts, the plugin's SessionStart hook shall give the session each rule of the log of temporary rules.
  Readings: (a) r36 wins, recommended: r24 is retired and replaced by new r37 adding 'and whose log of temporary rules holds no rule' (r28 likewise). (b) r24/r28 win: r36 is restricted to repositories with a pending step or an open initiative.
- Q7 (backlog r7): 'the person rules' is close to the avoided 'ruling' (design-decision/answers-not-rulings).
  Line: [backlog#r7] **When** the person rules that a rule of the log of temporary rules moves to the backlog, the session shall move it from the log of temporary rules to the backlog.
  Readings: (a) Reword to 'the person says that', recommended. (b) Keep as drafted.
- Q8 (backlog r8): is r8 more than r1 with r5?
  Line: [backlog#r8] The session shall keep each rule, idea and observation of the bounded context in the repository.
  Readings: (a) Same: retire r8, recommended. (b) Wider (any rule the person gives): 'The session shall keep each rule the person gives it, and each idea and observation of the bounded context, in the repository.'
