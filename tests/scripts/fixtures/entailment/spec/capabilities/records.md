---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/records
title: Records
narrator: the person
group: service
area: specification
specifies: service records
language: codified-2
retired: []
unbuilt: []
---

# Records

## Purpose
Reports and research kept beside the specification, filed with a title, a summary and what they are about; nothing of
the system cites one.

## Behaviour

### [g1] `work record` writes and commits a record
- [r1] When the person files a record, the records service shall keep the record.

### [g2] `work record` refuses an `--about` that identifies nothing
- [r2] If the person files a record with a text that does not conform to the node id form, then the records service
  shall refuse the request and name the text.
