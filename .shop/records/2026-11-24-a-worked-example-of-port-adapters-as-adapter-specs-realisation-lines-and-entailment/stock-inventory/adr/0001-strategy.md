# 0001 Hold at reserve, consume at take, release at free

Status: accepted. Scope: this adapter only.

A reservation is an inventory allocation held when ordering reserves, consumed when ordering takes it and released when
ordering frees it. inventory's own lapse is the reservation's lapse; the adapter keeps no timer.
