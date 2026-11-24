---
id: bounded-context/example.org/shop/ordering-stock-ledger
title: stock over the stock ledger
kind: adapter
realises: bounded-context/example.org/shop/ordering port stock
providers: [legacy stock ledger, described by the adapter's owners, assumed]
language: codified-2
imports: [request, time]
---

# stock over the stock ledger

## Purpose

The adapter that realises ordering's stock port with the legacy stock ledger, which only decrements and increments a
stock line: the holds, their lapse and their idempotency are the adapter's own.

## Composition

| area | kind | capabilities |
|---|---|---|
| port | port | stock-port |
| provider | provider | ledger |
| adapter | adapter | realisation |
