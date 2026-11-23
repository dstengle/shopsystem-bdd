---
id: vocabulary/example.org/shop/ordering/orders
area: orders
---

# The words of orders

## Terms

- **the ordering service** (proper noun) → service ordering. What answers the shopper and runs each order's saga.
- **order** (noun) → object order. What a shopper asks the shop to sell them: a quantity of one product.
- **product** (noun) → object product. A thing the shop sells.
- **quantity** (attribute) → attribute order.quantity. How many units of the product the order is for.
- **card** (attribute) → attribute order.card. The token of the card the shopper pays the order with.
- **total** (attribute) → attribute order.total. What the order costs, in the shop's currency.
- **status** (attribute) → attribute order.status. How far the order's saga has gone.
- **placed** (adjective) → value order.status placed.
- **held** (adjective) → value order.status held.
- **rejected** (adjective) → value order.status rejected.
- **charged** (adjective) → value order.status charged.
- **confirmed** (adjective) → value order.status confirmed.
- **cancelled** (adjective) → value order.status cancelled.
- **withdrawn** (adjective) → value order.status withdrawn.
- **expired** (adjective) → value order.status expired.
- **paid** (adjective) → value order.status paid.
- **unpaid** (adjective) → value order.status unpaid.
- **place** (verb, action) → operation ordering.place. Forms: places, placed. Frame: <actor> places <order>.
- **withdraw** (verb, action) → operation ordering.withdraw. Forms: withdraws, withdrawn. Frame: <actor> withdraws <order>.
- **view** (verb, action) → operation ordering.view. Forms: views, viewed. Frame: <actor> views <product>.
