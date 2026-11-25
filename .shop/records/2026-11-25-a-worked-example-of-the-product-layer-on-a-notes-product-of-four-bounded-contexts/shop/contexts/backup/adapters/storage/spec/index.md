---
id: bounded-context/example.org/notes/backup/adapter/storage
title: storage port over the vault storage provider
kind: adapter
realises: [storage-port#r1, storage-port#r2]
providers: [bounded-context/example.net/vault/storage@2.0.0]
language: codified-2
imports: [request]
---

# storage port over the vault storage provider

## Purpose

The adapter that realises backup's storage port with a third-party storage provider's objects: a snapshot is one
object, stored by its key and fetched by it.

## Composition
