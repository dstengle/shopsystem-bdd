---
id: bounded-context/example.org/shop/ordering-stock-inventory
title: stock over inventory
kind: adapter
realises: bounded-context/example.org/shop/ordering port stock
providers: [bounded-context/example.org/shop/inventory@1.4.0]
language: codified-2
imports: [request]
---

# stock over inventory

## Purpose

The adapter that realises ordering's stock port with inventory's operations: where ordering's words and inventory's
words meet. It realises stock-port r1-r6.

## Composition

| area | kind | capabilities |
|---|---|---|
| port | port | stock-port |
| provider | provider | holding |
| adapter | adapter | realisation |
