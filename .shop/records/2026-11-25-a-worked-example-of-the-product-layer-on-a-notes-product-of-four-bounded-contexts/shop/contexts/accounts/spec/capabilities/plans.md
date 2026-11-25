---
id: capability/example.org/notes/accounts/plans
title: Plans
narrator: the person
group: service
area: accounts
specifies: service accounts
serves: [job/example.org/notes/j5]
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Plans

## Purpose

The person subscribes to a larger plan: charged, then the allowance enlarged, the charge refunded when it cannot be.

## Behaviour

### [g1] Subscribing to a plan charges a subscription
- [r1] When the person subscribes to a plan, the accounts service shall charge a subscription that has the plan.

### [g2] A charge completed makes the subscription charged and entitles it
- [r2] While a subscription is `requested`, when the payments service completes the request, the accounts service shall set the status of the subscription to `charged` and entitle the subscription.

### [g3] A charge refused is told to the person
- [r3] While a subscription is `requested`, if the payments service refuses the request, then the accounts service shall notify the person of the subscription.

### [g4] An entitlement completed makes the subscription active
- [r4] While a subscription is `charged`, when the notebook service completes the request, the accounts service shall set the status of the subscription to `active`.

### [g5] An entitlement refused refunds the charge
- [r5] While a subscription is `charged`, if the notebook service refuses the request, then the accounts service shall refund the subscription and set the status of the subscription to `refunded`.

## Dropped
