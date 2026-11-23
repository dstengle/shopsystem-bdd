---
id: model/example.org/shop/payments/payments
area: payments
kind: core
imports: []
---

# Payments

## Purpose

Authorisations on cards, their capture and settlement, payouts to the merchant and disputes over payments.

```model
object card
  attributes: number (text); standing: good | blocked

object authorisation
  attributes: amount (number); currency: EUR | USD | GBP; reference (text)
  lifecycle status: granted → captured; granted → voided; captured → settled; captured → reversed
  relations: on → card (one)

object payout
  attributes: amount (number)

object dispute
  attributes: outcome: open | won | lost
  relations: on → authorisation (one)

service payments
  operation authorise(card, amount, currency, reference) by the merchant
    outcomes: done → the authorisation | refused: card declined, amount over limit
  operation capture(authorisation) by the merchant  outcomes: done | refused: voided authorisation
  operation void(authorisation) by the merchant  outcomes: done | refused: captured authorisation
  operation settle(authorisation) by the network  outcomes: done
  operation reverse(authorisation) by the network  outcomes: done
  operation disburse(payout) by the merchant  outcomes: done
  operation contest(authorisation) by the cardholder  outcomes: done → the dispute
  operation resolve(dispute) by the merchant  outcomes: done

event an authorisation settles: raised by payments.settle
event an authorisation is reversed: raised by payments.reverse
event a dispute is opened: raised by payments.contest

actor the merchant kind of agent
actor the network kind of agent
actor the cardholder kind of agent
```
