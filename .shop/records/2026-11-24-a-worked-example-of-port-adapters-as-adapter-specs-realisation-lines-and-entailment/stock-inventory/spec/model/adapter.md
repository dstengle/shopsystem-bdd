---
id: model/example.org/shop/ordering/adapters/stock-inventory/adapter
area: adapter
kind: adapter
imports: [port, provider]
---

# The adapter's own things

## Purpose

What only the adapter knows, kept in its store: for each order, its entry: the reservation ordering knows, the allocation
inventory knows, which of inventory's products is the order's product, and the reference it held them with.

```model
object entry kind of request
  attributes: reference (text)
  relations: of → order | reservation (one); has → allocation (one); has → stocked-product (one); has → reservation (one)
```
