# 0004 inventory's lapse events by subscription

Status: accepted. Scope: this adapter only.

The adapter subscribes to inventory's event 'an allocation lapses' (at least once, in no fixed order), drops an event
whose entry is already lapsed, and tells ordering of the reservation.
