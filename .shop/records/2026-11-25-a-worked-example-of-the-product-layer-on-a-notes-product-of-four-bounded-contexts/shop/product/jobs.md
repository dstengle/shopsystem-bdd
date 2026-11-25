---
id: jobs/example.org/notes
---

# Jobs to be done

Each job: its id `job/example.org/notes/j<n>`, its actor (one of ## Actors of product/index.md), its statement "When
<situation>, <actor> wants <motivation>, so they can <outcome>", the subdomains it needs (product/domain.md) and the
bounded context the product assigns it to. The capability that serves it says `serves:` in its own frontmatter.

## [j1] Jot a thought down
- actor: the person
- statement: When a thought comes up in the middle of other work, the person wants to add it as a note under a tag,
  so they can let it go and find it later.
- subdomains: [s1]
- assigned: bounded-context/example.org/notes/notebook

## [j2] Pick a topic up again
- actor: the person
- statement: When they come back to a topic, the person wants every note under its tag, so they can carry on where
  they left off.
- subdomains: [s1, s5]
- assigned: bounded-context/example.org/notes/notebook

## [j3] Let a colleague read a note
- actor: the person, the colleague
- statement: When a colleague needs what the person wrote, the person wants to let that colleague read one note and
  the colleague wants to take it up or turn it down, so they can work from the same text without copying it.
- subdomains: [s2, s1]
- assigned: bounded-context/example.org/notes/sharing

## [j4] Keep the notes safe
- actor: the person
- statement: When their device could be lost or break, the person wants the notes kept somewhere else, so they can
  get them back.
- subdomains: [s3, s1, s6]
- assigned: bounded-context/example.org/notes/backup

## [j5] Get more room
- actor: the person
- statement: When the free allowance is used up, the person wants to pay for a larger plan, so they can keep adding
  notes, and not to pay when the room is not given.
- subdomains: [s4, s7, s1]
- assigned: bounded-context/example.org/notes/accounts

## [j6] Carry on on a new device
- actor: the person
- statement: When they start on a new device, the person wants the notes they kept on the old one, so they can carry
  on there.
- subdomains: [s3, s1, s6]
- assigned: bounded-context/example.org/notes/backup
