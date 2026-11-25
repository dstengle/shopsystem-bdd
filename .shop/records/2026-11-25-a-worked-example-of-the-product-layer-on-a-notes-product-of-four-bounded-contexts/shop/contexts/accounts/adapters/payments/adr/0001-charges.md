---
id: design-decision/example.org/notes/accounts/adapter/payments/charges
summary: "A charge is one payco charge created with the subscription's id as its idempotency key; a refund refunds that charge whole."
date: 2026-11-25
status: accepted
tier: judgement
---

# 0001. Charges

## Decision

charge(subscription) creates a payco charge of the plan's price with the subscription's id as idempotency key, so a
retried charge is not taken twice; refund(subscription) refunds that charge whole. The answer comes back by payco's
webhook, which the adapter turns into the port request's completion or refusal.
