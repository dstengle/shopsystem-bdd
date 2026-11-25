---
id: model/example.org/notes/accounts/payments
area: payments
kind: port
imports: [accounts]
---

# payments

## Purpose

What accounts needs of a payment provider: a subscription charged, and a charge refunded.

```model
service payments
  operation charge(subscription)  idempotent by subscription; compensated by refund
    outcomes: done | refused: card declined
  operation refund(subscription)  outcomes: done
```
