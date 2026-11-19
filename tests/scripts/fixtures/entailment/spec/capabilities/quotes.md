---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/quotes
title: Quotes
narrator: a session
group: service
area: tracking
specifies: object quote, service conversation: quote, prompt, read
language: codified-2
retired: []
unbuilt: []
---

# Quotes

## Purpose
The person's words quoted from a session's transcript, with the messages they cite.

## Behaviour

### [g1] A message quoted is kept as a quote
- [r1] When a session quotes a message, the conversation service shall keep a quote from the session that cites the
  message.

### [g2] A prompt keeps the session's transcript for quoting
- [r2] When the person prompts a session, the conversation service shall keep the transcript of the session.

### [g3] A quote read gives the messages it cites
- [r3] When the person reads a quote, the conversation service shall return every message that the quote cites.

### [g4] A queued message quoted is kept as a quote
- [r4] When a session quotes a queued message, the conversation service shall keep a quote that cites the queued message
  and return the quote.
