---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-capability-that-contributes-to-no-job-is-reported
summary: "The product check reports a capability that serves no job, is reached by no job's trace and specifies no port; a guarantees capability is a participant of the jobs whose lines it constrains."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-95]
---

# 0144. A capability that contributes to no job is reported

## Context

In the notes product 8 of 9 'serves no job' findings were port capabilities or capabilities other jobs' traces reach; only the planted orphan was real.

## Decision

Each capability is an entry point (a group serves a job), a participant (a job's trace reaches it), a port (it specifies a driven port), or an orphan, which the product check reports. A guarantees capability's universal conditions constrain the lines of the jobs whose traces they bear on, which makes it a participant. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
