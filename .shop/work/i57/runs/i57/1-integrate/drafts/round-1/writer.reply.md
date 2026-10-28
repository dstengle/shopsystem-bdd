/tmp/work-run-i57-z7zn1_jh/i57-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/backlog.md
/tmp/work-run-i57-z7zn1_jh/i57-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/capabilities/migration-tools.md
/tmp/work-run-i57-z7zn1_jh/i57-1-integrate/.shop/scratch/1-integrate/drafts/round-1/spec/index.md

## Change list

| change | capability | id | line | source (request q31) |
|---|---|---|---|---|
| added | backlog | backlog#r1 | The bounded context shall have a backlog of ideas and observations, kept in the repository. | Line 1: "The bounded context shall have a backlog of ideas and observations, kept in the repository." |
| added | backlog | backlog#r2 | **When** the person gives a session an idea or an observation outside an initiative, the session shall add it to the backlog in the same turn, with its date and the person's words. | Line 2: "**When** the person gives a session an idea or an observation outside an initiative, the session shall add it to the backlog in the same turn, with its date and the person's words." |
| added | backlog | backlog#r3 | **While** an item of the backlog has had no discovery discussion with the person, the plugin shall draft no request and no proposal from it. | Line 4: "**While** an item of the backlog has had no discovery discussion with the person, the plugin shall draft no request and no proposal from it." |
| added | backlog | backlog#r4 | **When** the person and a session have held a discovery discussion on an item of the backlog, the session shall raise a request from it, naming the item as its source. | Line 5: "**When** the person and a session have held a discovery discussion on an item of the backlog, the session shall raise a request from it, naming the item as its source." |
| added | backlog | backlog#r5 | The bounded context shall have a log of temporary rules that the person gives its sessions, kept in the repository. | Line 6: "The bounded context shall have a log of temporary rules that the person gives its sessions, kept in the repository." |
| added | backlog | backlog#r6 | **When** the person gives a session a rule outside an initiative, the session shall add it to the log of temporary rules in the same turn, with its date and the person's words. | Line 7: "**When** the person gives a session a rule outside an initiative, the session shall add it to the log of temporary rules in the same turn, with its date and the person's words." |
| added | backlog | backlog#r7 | **When** the person rules that a rule of the log of temporary rules moves to the backlog, the session shall move it from the log of temporary rules to the backlog. | Line 9: "**When** the person rules that a rule of the log of temporary rules moves to the backlog, the session shall move it from the log to the backlog." |
| added | backlog | backlog#r8 | The session shall keep each rule, idea and observation of the bounded context in the repository. | Line 10: "The session shall keep each rule, idea and observation of the bounded context in the repository." |
| added | migration-tools | migration-tools#r35 | **When** a session starts, the plugin's SessionStart hook shall give the session no item of the backlog. | Line 3: "The session-start hook's text shall give no item of the backlog." |
| added | migration-tools | migration-tools#r36 | **When** a session starts, the plugin's SessionStart hook shall give the session each rule of the log of temporary rules. | Line 8: "The session-start hook's text shall give each rule of the log of temporary rules." |

Glossary:

| change | term | entry | source (request q31) |
|---|---|---|---|
| added | term/backlog | - **backlog**: the bounded context's ideas and observations that the person gives its sessions outside an initiative, kept in the repository, each with its date and the person's words. | Line 1: "The bounded context shall have a backlog of ideas and observations, kept in the repository." with Line 2: "...the session shall add it to the backlog in the same turn, with its date and the person's words." |
| added | term/log-of-temporary-rules | - **log of temporary rules**: the bounded context's rules that the person gives its sessions outside an initiative, kept in the repository, each with its date and the person's words, until the person moves one to the backlog. | Line 6: "The bounded context shall have a log of temporary rules that the person gives its sessions, kept in the repository." with Lines 7 and 9 |

Notes for the round:
- The new capability is `backlog` (title "Backlog and temporary rules", group service, rests_on design-decision/requests-written-through-work, retired: []). spec/index.md's Composition table needs a `backlog` row (narrator: a person or session keeping the bounded context's ideas, observations and temporary rules; group: service); not drafted, as instructed.
- migration-tools: only its Behaviour section changes (r35, r36 under "The session's start and compaction"); frontmatter unchanged.
- No decision files.

## Questions

1. backlog (r1, r2, r8) / glossary: "observation" is already a record kind of this context (`.shop/records/observations/`, `observation/<...>` ids). Is an observation of the backlog such a record? If yes: r2 becomes "...the session shall add it to the backlog as an observation record in the same turn, with its date and the person's words." If no: add a `Not:`-free note to term/backlog, "an observation of the backlog is not an observation record", and keep the lines as drafted.
2. backlog r2, r6: "in the same turn" uses `turn`, a glossary term for the side of a request. If it means the session's reply to the person's message: "...the session shall add it to the backlog before its reply to that message ends, with its date and the person's words." (r6 likewise). If it means the request's turn: keep as drafted (unlikely, as no request exists yet).
3. backlog r3, r4: "discovery discussion" is neither a term nor spelled out. If it is a term, the entry I would write: "- **discovery discussion**: a discussion between the person and a session on one item of the backlog, after which a request may be raised from it." If not: what marks an item as having had one (r3's state needs something observable)?
4. backlog r4: a request's origins are ids (requests r44, `--source <id>`). Does each item of the backlog have an id? If yes: "The session shall give each item of the backlog an id when it adds it." (new line r9). If no: r4 names the item in words, and `work request` needs another way to take a non-id origin (a request into requests).
5. backlog r3: does "no proposal" mean capability-proposals and glossary-proposals both? If yes: "...the plugin shall draft no request, no capability-proposal and no glossary-proposal from it." If it means only capability-proposals: "...no request and no capability-proposal from it."
6. migration-tools r36 against r24 and r28: r24 and r28 say the SessionStart hook tells the session nothing (no pending upgrade step, no open initiative; or no `.shop/`). Which wins when the log of temporary rules holds a rule? If r36 wins: r24 is retired and replaced by "[r37] When a session starts in a repository with `.shop/` for which no upgrade step is pending, whose plugin version is not above the plugin's, that has no initiative that is neither `done` nor `abandoned` and whose log of temporary rules holds no rule, the plugin's SessionStart hook shall tell the session nothing." (r28 likewise, if the log can exist without `.shop/`). If r24/r28 win: r36 becomes "When a session starts in a repository with `.shop/` for which an upgrade step is pending or that has an initiative that is neither `done` nor `abandoned`, ...".
7. backlog r7: "the person rules" sits close to `ruling`, an avoided word of term/answer (design-decision/answers-not-rulings). Reword as "**When** the person says that a rule of the log of temporary rules moves to the backlog, ..."? If no, keep as drafted.
8. backlog r8: is "each rule" only the log of temporary rules' rules, and is r8 more than r1 with r5? If it is the same: retire r8 before formulation and keep r1, r5. If "rule" reaches further (any rule the person gives, in or outside an initiative): "The session shall keep each rule the person gives it, and each idea and observation of the bounded context, in the repository."

## Cut sentences

- The request's title: "A backlog of ideas and a log of temporary rules" (used only as the capability's Purpose wording, not a line).
