---
id: design-decision/example.org/notes/backup/adapter/storage/object-store
summary: "A snapshot is one object in the provider's bucket, keyed by the snapshot's id, written and read over the provider's HTTPS object API."
date: 2026-11-25
status: accepted
tier: judgement
---

# 0001. Object store

## Decision

store(snapshot) is a PUT of the bundle as one object keyed by the snapshot's id; fetch(snapshot) is a GET of it. A
4xx answer to the PUT is the port's refusal; a 5xx is retried three times, then a refusal.
