---
id: model/example.org/shop/ordering-stock-ledger/adapter
area: adapter
kind: adapter
imports: [port, provider]
---

# The adapter's own things

## Purpose

The adapter's store: for each order, its entry (the reservation, the ledger line it decremented, whether it was
taken) and the deadline at which an entry not taken lapses.

```model
object entry kind of request
  attributes: progress: decremented | taken | returned
  relations: of → order | reservation (one); has → line (one); has → reservation (one)

object deadline kind of moment
  relations: of → entry (one)
```
