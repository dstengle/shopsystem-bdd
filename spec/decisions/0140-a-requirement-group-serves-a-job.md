---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-requirement-group-serves-a-job
summary: "The product assigns a job to a bounded context; the requirement groups of that context that are its entry point and coordination serve it, not a whole capability."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-95]
---

# 0140. A requirement group serves a job

## Context

Both product worked examples found serves: on a whole capability giving two jobs one trace (checking in this repository, the notebook in the notes product).

## Decision

serves: <job> is written on a requirement group of the capability that coordinates the job, so one capability may serve several jobs and each job gets its own trace. Every group serving a job is in the bounded context the product assigned the job to. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
