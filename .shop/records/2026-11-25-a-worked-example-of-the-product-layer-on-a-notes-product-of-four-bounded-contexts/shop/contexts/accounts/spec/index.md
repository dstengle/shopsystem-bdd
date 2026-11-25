---
id: bounded-context/example.org/notes/accounts
title: accounts
language: codified-2
imports: [request]
---

# accounts

## Purpose

The person's plan and its subscription: a larger plan charged through a payment provider outside the product and,
once paid, the notebook's allowance enlarged; a charge refunded when the allowance cannot be enlarged.

## Composition

| area | kind | capabilities |
|---|---|---|
| accounts | generic | plans |
| payments | port | payments-port |
| notebook | port | notebook-port |

## Upstreams

- bounded-context/example.org/notes/notebook: github: ex/notes-notebook
