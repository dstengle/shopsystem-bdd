---
id: vocabulary/example.org/shop/payments/payments
area: payments
---

# The words of payments

## Terms

- **the payments service** (proper noun) → service payments. What answers merchants, the network and cardholders.
- **card** (noun) → object card. A payment card a cardholder pays with.
- **authorisation** (noun) → object authorisation. An amount a card's issuer has agreed to pay a merchant.
- **payout** (noun) → object payout. Money paid out to the merchant.
- **dispute** (noun) → object dispute. A cardholder's challenge to a payment.
- **standing** (attribute) → attribute card.standing. Whether the issuer still accepts the card.
- **good** (adjective) → value card.standing good.
- **blocked** (adjective) → value card.standing blocked.
- **amount** (attribute) → attribute authorisation.amount. How much is authorised.
- **currency** (attribute) → attribute authorisation.currency. The currency of the amount.
- **reference** (attribute) → attribute authorisation.reference. The merchant's own key for an authorisation.
- **status** (attribute) → attribute authorisation.status. Where an authorisation is in its life.
- **granted** (adjective) → value authorisation.status granted.
- **captured** (adjective) → value authorisation.status captured.
- **voided** (adjective) → value authorisation.status voided.
- **settled** (adjective) → value authorisation.status settled.
- **reversed** (adjective) → value authorisation.status reversed.
- **outcome** (attribute) → attribute dispute.outcome. How a dispute ended. Redefines: request.
- **open** (adjective) → value dispute.outcome open.
- **won** (adjective) → value dispute.outcome won.
- **lost** (adjective) → value dispute.outcome lost.
- **authorise** (verb, action) → operation payments.authorise. Forms: authorises, authorised. Frame: <actor> authorises <card>.
- **capture** (verb, action) → operation payments.capture. Forms: captures, captured. Frame: <actor> captures <authorisation>.
- **void** (verb, action) → operation payments.void. Forms: voids, voided. Frame: <actor> voids <authorisation>.
- **settle** (verb, action) → operation payments.settle. Forms: settles, settled. Frame: <actor> settles <authorisation>.
- **reverse** (verb, action) → operation payments.reverse. Forms: reverses, reversed. Frame: <actor> reverses <authorisation>.
- **disburse** (verb, action) → operation payments.disburse. Forms: disburses, disbursed. Frame: <actor> disburses <payout>.
- **contest** (verb, action) → operation payments.contest. Forms: contests, contested. Frame: <actor> contests <authorisation>.
- **resolve** (verb, action) → operation payments.resolve. Forms: resolves, resolved. Frame: <actor> resolves <dispute>.
