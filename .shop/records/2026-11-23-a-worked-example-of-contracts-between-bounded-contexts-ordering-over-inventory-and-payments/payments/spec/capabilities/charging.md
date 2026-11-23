---
id: capability/example.org/shop/payments/charging
title: Charging a card
narrator: a merchant
group: service
area: payments
specifies: service payments
language: codified-2
retired: []
unbuilt: []
---

# Charging a card

## Purpose

A merchant authorises an amount on a card, then captures or voids it; the network settles or reverses a capture
later, and the merchant is told.

## Behaviour

### [g1] A card authorised is granted
- [r1] When the merchant authorises a card with an amount and a currency and a reference, the payments service shall
  keep an authorisation on the card.

### [g2] A blocked card is declined
- [r2] If the merchant authorises a card whose standing is `blocked`, then the payments service shall refuse the
  request and name the card.

### [g3] An amount over the limit is refused
- [r3] If the merchant authorises a card with the amount `10000`, then the payments service shall refuse the request
  and name the amount.

### [g4] An authorisation captured is captured
- [r4] When the merchant captures an authorisation whose status is `granted`, the payments service shall set the
  status of the authorisation to `captured`.

### [g5] A voided authorisation is not captured
- [r5] If the merchant captures an authorisation whose status is `voided`, then the payments service shall refuse
  the request and name the authorisation.

### [g6] An authorisation voided is voided
- [r6] When the merchant voids an authorisation whose status is `granted`, the payments service shall set the status
  of the authorisation to `voided`.

### [g7] A captured authorisation is not voided
- [r7] If the merchant voids an authorisation whose status is `captured`, then the payments service shall refuse the
  request and name the authorisation.

### [g8] A capture settled tells the merchant
- [r8] When the network settles an authorisation whose status is `captured`, the payments service shall set the
  status of the authorisation to `settled` and notify the merchant of the authorisation.

### [g9] A capture reversed tells the merchant
- [r9] When the network reverses an authorisation whose status is `captured`, the payments service shall set the
  status of the authorisation to `reversed` and notify the merchant of the authorisation.
