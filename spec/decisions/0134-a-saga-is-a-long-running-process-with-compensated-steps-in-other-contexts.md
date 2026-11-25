---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-saga-is-a-long-running-process-with-compensated-steps-in-other-contexts
summary: "Not every core activity that calls another context is a saga: a port request, a long-running process and a saga are told apart, derived from the model and the lines, never labelled by hand."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-79]
---

# 0134. A saga is a long-running process with compensated steps in other contexts

## Context

The person asked whether every core activity that calls other subdomains or contexts is a saga; b546's saga checks need the terms.

## Decision

Three terms: a port request is one request of the core through a driven port, its outcomes told apart by the core's statuses (decision 0121); a long-running process is an object of the core whose lifecycle waits on replies to its requests (DDD's process manager); a saga is a long-running process with two or more state-changing requests to other contexts, each compensated when a later one fails. Which one an activity is, is derived from the domain model (lifecycles, compensated by, followed by) and the lines, not declared. Opening a batch stays one commit and is no saga (decision 0131).

## Alternatives

Every cross-context activity a saga: rejected, most are single port requests. A kind label on the model: rejected, it can disagree with what the lines say.
