---
id: vocabulary/example.org/shop/ordering/stock
area: stock
---

# The words of the stock port

## Terms

- **the stock service** (proper noun) → service stock. What sets stock aside for ordering; inventory, behind the port.
- **reservation** (noun) → object reservation. Stock set aside for one order until it is taken or freed.
- **availability** (noun) → object availability. How many units of a product can be ordered now. Plural: availabilities.
- **units** (attribute) → attribute availability.units. The number of units that can be ordered.
- **state** (attribute) → attribute reservation.state. Whether a reservation still stands.
- **made** (adjective) → value reservation.state made.
- **lapsed** (adjective) → value reservation.state lapsed.
- **reserve** (verb, action) → operation stock.reserve. Forms: reserves, reserved. Frame: <actor> reserves stock for <order>.
- **free** (verb, action) → operation stock.free. Forms: frees, freed. Frame: <actor> frees <reservation>.
- **take** (verb, action) → operation stock.take. Forms: takes, taken. Frame: <actor> takes <reservation>.
- **count** (verb, action) → operation stock.count. Forms: counts, counted. Frame: <actor> counts <product>.
- **restock** (verb, action) → operation stock.restock. Forms: restocks, restocked. Frame: <actor> restocks <product>.
