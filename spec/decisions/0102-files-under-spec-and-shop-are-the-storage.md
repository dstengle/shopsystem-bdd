---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/files-under-spec-and-shop-are-the-storage
summary: "Each kind of object is stored as the file form spec forms lists; the forms are the store adapter's schema."
date: 2026-11-19
status: accepted
tier: judgement
---

# 0102. Files under spec/ and .shop/ are the storage

## Decision

Each kind of object of the domain model is stored as a file under spec/ or .shop/ in the form `spec forms` lists, with the command that writes it; the forms are the store adapter's schema, so no requirement names a path.
