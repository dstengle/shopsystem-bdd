---
id: capability/example.org/notes/accounts/payments-port
title: Payments port
narrator: the accounts service
group: service
area: payments
specifies: service payments
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Payments port

## Purpose

What accounts needs of the payment provider it reaches.

## Behaviour

### [g1] A subscription charged completes
- [r1] When the accounts service charges a subscription, the payments service shall complete the request.

### [g2] A subscription refunded completes
- [r2] When the accounts service refunds a subscription, the payments service shall complete the request.

## Dropped
