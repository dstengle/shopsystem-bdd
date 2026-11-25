---
id: model/example.org/notes/accounts/accounts
area: accounts
kind: generic
imports: [payments, notebook]
---

# accounts

## Purpose

The plans the product offers and the person's subscriptions to them, each waiting on its charge and its allowance.

```model
object plan

object subscription
  attributes: status: requested | charged | active | refunded
  lifecycle status: requested → charged; charged → active; charged → refunded
  relations: has → plan (one)

service accounts
  operation subscribe(plan)  outcomes: done → the subscription

actor the person kind of agent
```
