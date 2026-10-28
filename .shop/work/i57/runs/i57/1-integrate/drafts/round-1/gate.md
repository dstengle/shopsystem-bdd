# Gate, round 1 (q31)

## Behaviour lines

### backlog (new capability, `spec/capabilities/backlog.md`; spec/index.md Composition needs a `backlog` row, not drafted)
- [r1] The bounded context shall have a backlog of ideas and observations, kept in the repository.
- [r2] **When** the person gives a session an idea or an observation outside an initiative, the session shall add it to the backlog in the same turn, with its date and the person's words.
- [r3] **While** an item of the backlog has had no discovery discussion with the person, the plugin shall draft no request and no proposal from it.
- [r4] **When** the person and a session have held a discovery discussion on an item of the backlog, the session shall raise a request from it, naming the item as its source.
- [r5] The bounded context shall have a log of temporary rules that the person gives its sessions, kept in the repository.
- [r6] **When** the person gives a session a rule outside an initiative, the session shall add it to the log of temporary rules in the same turn, with its date and the person's words.
- [r7] **When** the person rules that a rule of the log of temporary rules moves to the backlog, the session shall move it from the log of temporary rules to the backlog.
- [r8] The session shall keep each rule, idea and observation of the bounded context in the repository.

### migration-tools (under "The session's start and compaction")
- [r35] **When** a session starts, the plugin's SessionStart hook shall give the session no item of the backlog.
- [r36] **When** a session starts, the plugin's SessionStart hook shall give the session each rule of the log of temporary rules.

## Glossary
- added `term/backlog`: - **backlog**: the bounded context's ideas and observations that the person gives its sessions outside an initiative, kept in the repository, each with its date and the person's words.
- added `term/log-of-temporary-rules`: - **log of temporary rules**: the bounded context's rules that the person gives its sessions outside an initiative, kept in the repository, each with its date and the person's words, until the person moves one to the backlog.

## Decisions
None.

## Questions
1. backlog r2 / term/backlog: "observation" is already a record kind (`.shop/records/observations/`). Is an observation of the backlog such a record? Yes: r2 becomes "...add it to the backlog as an observation record in the same turn...". No: term/backlog notes that an observation of the backlog is not an observation record; lines as drafted.
2. backlog r2, r6: "in the same turn": `turn` is a glossary term for a request's side. Reading A (reply to the person's message): "...before its reply to that message ends...". Reading B: keep as drafted.
3. backlog r3, r4: "discovery discussion": a term? If yes, entry: "- **discovery discussion**: a discussion between the person and a session on one item of the backlog, after which a request may be raised from it." If no, what marks an item as having had one?
4. backlog r4: does each backlog item have an id (requests take ids as origins)? Yes: new line r9 "The session shall give each item of the backlog an id when it adds it." No: `work request` needs another way to take a non-id origin (a request into requests).
5. backlog r3: "no proposal" = capability- and glossary-proposals both (recommended): "...no request, no capability-proposal and no glossary-proposal from it." Or only capability-proposals.
6. migration-tools r36 against r24 and r28 (hook tells nothing when no pending step, no open initiative, or no `.shop/`): if r36 wins (recommended), r24 is retired and replaced by r37 adding "and whose log of temporary rules holds no rule" (r28 likewise); if r24/r28 win, r36 is restricted to repositories with a pending step or an open initiative.
7. backlog r7: "the person rules" is close to the avoided "ruling" (design-decision/answers-not-rulings). Reword "the person says that"? Recommended: yes.
8. backlog r8: is it more than r1 with r5? Same: retire r8. Wider (any rule the person gives): "The session shall keep each rule the person gives it, and each idea and observation of the bounded context, in the repository."
