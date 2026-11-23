---
id: capability/example.org/shop/payments/payouts
title: Payouts and disputes
narrator: a merchant
group: service
area: payments
specifies: service payments
language: codified-2
retired: []
unbuilt: []
---

# Payouts and disputes

## Purpose

The merchant's money paid out, and the disputes cardholders open over payments.

## Behaviour

### [g1] A payout disbursed is kept
- [r1] When the merchant disburses a payout, the payments service shall keep the payout.

### [g2] A payment contested opens a dispute and tells the merchant
- [r2] When the cardholder contests an authorisation, the payments service shall keep a dispute on the
  authorisation and notify the merchant of the authorisation.

### [g3] A dispute resolved completes the request
- [r3] When the merchant resolves a dispute, the payments service shall complete the request.
