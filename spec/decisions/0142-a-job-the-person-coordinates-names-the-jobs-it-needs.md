---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-job-the-person-coordinates-names-the-jobs-it-needs
summary: "When the person, not a capability, runs a job's steps in order, the job names the jobs it needs first and their traces join its own."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-95]
---

# 0142. A job the person coordinates names the jobs it needs

## Context

The notes product's j6 and this repository's shaping are coordinated by the person; their serving capability's trace missed the capability that runs first.

## Decision

A job lists needs: [<job>, ...] when the person carries it through other jobs (shaping runs drafting, then readying). Its trace is its serving groups' trace joined with the needed jobs' traces; a cycle of needs is refused. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
