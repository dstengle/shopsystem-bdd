---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/a-job-names-its-actors-and-the-product-maps-them-to-each-context-s-terms
summary: "A job may have several actors; the product layer maps each product actor to the term each bounded context calls it by, and each actor triggers a line of the job's serving groups."
date: 2026-11-25
status: accepted
tier: judgement
source: [quote-95]
---

# 0141. A job names its actors and the product maps them to each context's terms

## Context

Requests and contracts have an asker and an upstream; in the notes product the same person is the owner in sharing and the person elsewhere.

## Decision

A job lists one actor or more. The product layer declares the product's actors and, per bounded context, the term (an actor of its model) that plays each. The check of a job: each of its actors, under its context's term, is the subject of a trigger of a line of the job's serving groups or its trace. Until the item that checks it is delivered this decision is a judgement; that item writes its successor at its own tier, naming its enforcer.
