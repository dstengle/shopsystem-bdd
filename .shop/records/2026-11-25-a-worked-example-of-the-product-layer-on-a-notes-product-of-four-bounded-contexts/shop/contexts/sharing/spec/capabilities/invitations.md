---
id: capability/example.org/notes/sharing/invitations
title: Invitations
narrator: the owner
group: service
area: sharing
specifies: service sharing
serves: [job/example.org/notes/j3]
language: codified-2
rests_on: []
retired: [r3, r4]
unbuilt: []
---

# Invitations

## Purpose

An owner invites a colleague to read a note; the colleague accepts or declines; the owner may take it back.

## Behaviour

### [g1] A note shared with an address is kept as an invitation
- [r1] When the owner shares a note with an address, the sharing service shall keep an invitation that has the note.

### [g2] A note shared without an address is refused
- [r2] If the owner shares a note without an address, then the sharing service shall refuse the request and name the
  address.

### [g3] An invitation accepted is accepted and its note shown
- [r9] When the colleague accepts an invitation, the sharing service shall set the status of the invitation to
  `accepted` and show the note of the invitation.

### [g4] A withdrawn invitation is not accepted
- [r5] If the colleague accepts an invitation whose status is `withdrawn`, then the sharing service shall refuse the
  request and name the invitation.

### [g5] An invitation declined is declined
- [r6] When the colleague declines an invitation, the sharing service shall set the status of the invitation to
  `declined`.

### [g6] An invitation withdrawn is withdrawn
- [r7] When the owner withdraws an invitation, the sharing service shall set the status of the invitation to
  `withdrawn`.

### [g8] An accepted invitation withdrawn has its note hidden
- [r8] While an invitation is `accepted`, when the owner withdraws the invitation, the sharing service shall hide the
  note of the invitation.

## Dropped
