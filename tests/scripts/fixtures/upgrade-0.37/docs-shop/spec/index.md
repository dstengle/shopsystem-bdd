---
id: bounded-context/example.org/acme/shop
title: shop
language: codified-2
imports: [cli]
---
# shop

The toy shop of docs/upgrading.md after its step 3: the 4.0 upgrade's fixture (tests/scripts/test_migrate_upgrade_cnl4.py)
with the four glossary edits the page names, and the item's lines r9 and r10 laid in group g2 of buy.

## Glossary
- **the person** (proper noun): the human who shops. Kind of: agent.
- **`shop`** (proper noun): the shop's tool. Kind of: tool.
- **cart** (noun): the goods a shopper picks.
- **shopper** (noun): a person who buys.
- **till** (noun): where a shopper pays.
- **command** (noun): what a shopper types. Redefines: cli.
- **pick** (verb, action): a shopper puts goods in a cart. Forms: picks, picked. Frame: shopper picks cart.
- **own** (verb, state): a shopper has a cart. Forms: owns, owned. Frame: shopper owns cart.
- **watch** (verb, action): a shopper looks at a till. Forms: watches, watched. Frame: shopper watches till.
- **guard** (verb, state): a shopper keeps a cart. Forms: guards, guarded. Frame: shopper guards cart.
- **load** (attribute of cart): how much a cart holds. Values: `empty`, `full`.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| till | for | shopper | one |
| cart | of | shopper | one |
