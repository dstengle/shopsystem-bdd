---
id: domain/example.org/notes
---

# The domain map

## Subdomains

| id | subdomain | type | purpose |
|---|---|---|---|
| s1 | note keeping | core | the notes, their tags and who may read them |
| s2 | collaboration | supporting | letting another person read a note |
| s3 | data safety | supporting | copies of the notes kept apart from the device |
| s4 | plans and billing | generic | what the person pays and the room it gives |
| s5 | search | core | finding a note by what it says |
| s6 | object storage | generic | bytes kept by a key outside the product |
| s7 | card payments | generic | taking and giving back money |

## Bounded contexts

| bounded context | subdomains | shop |
|---|---|---|
| bounded-context/example.org/notes/notebook | s1 | shop/example.org/notes/main |
| bounded-context/example.org/notes/sharing | s2 | shop/example.org/notes/main |
| bounded-context/example.org/notes/backup | s3 | shop/example.org/notes/main |
| bounded-context/example.org/notes/accounts | s4 | shop/example.org/notes/main |
| bounded-context/example.net/vault/storage | s6 | third party |
| bounded-context/example.net/payco/payments | s7 | third party |

## Relations

Derived, not written: each adapter spec's `providers:` under a hosted context is a relation from that context
(downstream) to the provider (upstream); `job_trace.py --relations` prints them.
