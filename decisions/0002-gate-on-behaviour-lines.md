---
id: decision/gate-on-behaviour-lines
summary: "The person approves the added, changed and removed Behaviour lines of a proposal; nothing is written to spec/ before that yes."
date: 2026-09-29
status: accepted
source: "records/archive/design-notes/2026-09-29-capability-spec-design.md; 0.8.0 (d034b50)"
---

# 0002. Gate on behaviour lines

## Decision

The one human gate is on Behaviour lines: the person sees the added, changed and removed lines and the questions the proposal left open, and answers. A committed Behaviour line is an approved one; the commit says when and by whom it was approved.

## Context

0.6.0 sorted scenarios into settled and deciding, and asked approval of the deciding ones. Approval landed on transcription rather than on decisions.

## Alternatives

Approval on scenarios; approval on the whole note.

## Consequences

Under design-model v3 the gate approves the requirement ids a capability-proposal lists in `adds`, `changes`, `removes`; that change is proposed by initiative i3.
