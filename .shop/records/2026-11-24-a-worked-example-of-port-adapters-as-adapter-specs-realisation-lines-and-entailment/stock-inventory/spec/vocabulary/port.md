---
id: vocabulary/example.org/shop/ordering/adapters/stock-inventory/port
area: port
---

# ordering's words (the port's), copied from ordering

## Terms

- **the ordering service** (proper noun) → service ordering. ordering's core, which requests the port.
- **the stock service** (proper noun) → service stock. The port this adapter realises.
- **order** (noun) → object order. What a shopper asks the shop to sell them.
- **product** (noun) → object product. A thing the shop sells.
- **quantity** (attribute) → attribute order.quantity. How many units the order is for.
- **number** (attribute) → attribute order.number. The order's own key.
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
