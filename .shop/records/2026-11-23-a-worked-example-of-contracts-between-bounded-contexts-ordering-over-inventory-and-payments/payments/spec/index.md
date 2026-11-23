---
id: bounded-context/example.org/shop/payments
title: payments
language: codified-2
imports: [request]
---

# payments

## Purpose

Card payments for merchants: an amount authorised on a card, captured or voided, settled or reversed later by the
card network; and the merchant's payouts and the disputes cardholders open.

## Composition

| area | kind | capabilities |
|---|---|---|
| payments | core | charging, payouts |
