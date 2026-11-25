---
id: bounded-context/example.org/notes/accounts/adapter/payments
title: payments port over the payco provider
kind: adapter
realises: [payments-port#r1, payments-port#r2]
providers: [bounded-context/example.net/payco/payments@1.0.0]
language: codified-2
imports: [request]
---

# payments port over the payco provider

## Purpose

The adapter that realises accounts' payments port with a third-party payment provider's charges and refunds.

## Composition
