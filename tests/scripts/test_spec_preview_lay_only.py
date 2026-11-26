"""spec_preview's `lay_only` (b808, checking r153, r154): of `spec check --item`, v_s3 of a group the item lays and
v_a5 of a requirement it lays left out, and nothing else: v_a6 of an id the item retires still reported."""

import backlog_items
import spec_preview

ITEM = """---
id: item/bounded-context/example.org/fixture/b1
kind: item
status: ready
provenance: own
value: high-value
urgency: medium-urgency
size: small
depends_on: []
---

# Notes kept

## Requirements

### notebook

retired: [r1]
retires: [r10 r1]

#### [g10] A note listed is kept
- [r10] When the person lists the notes, the notes service shall complete the request.
"""
NODE = "requirement/bounded-context/example.org/fixture/"


def brought():
    return spec_preview.lay_only(backlog_items.parse(ITEM, ".shop/backlog/b1.md"))


def test_the_item_s_own_group_and_requirement_are_left_out():
    assert brought()("v_s3", (NODE + "notebook#g10",))
    assert brought()("v_a5", ("notes.list", NODE + "notebook#r10"))


def test_v_a6_of_an_id_the_item_retires_is_reported():
    assert not brought()("v_a6", ("notes.list", NODE + "notebook#r1"))
