# 0002 The entry store, and inventory's reference as a second guard

Status: accepted. Scope: this adapter only.

The adapter keeps one entry per order (the reservation, the allocation, inventory's product, the reference) in its own
store, written before the hold. The hold is sent with the order's number as inventory's reference, so a hold retried
after a crash returns the same allocation (inventory holding#r2).
