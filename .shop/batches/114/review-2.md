---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-114/review-2
kind: review
batch: batch-114
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/137
head: b7a5e73bf586345c7292844c481136a018b7827a
range: b6b03e10d88d008e10e0e2933260a9beb3ff5201..b7a5e73bf586345c7292844c481136a018b7827a
result: clean
---

# batch-114 review 2

## Verdict

The fix closes f1: r31 no longer holds in r33's saga world, and the code now returns `port request` only for an operation that a port line governs and that has no `compensated by` property. One observation remains about traces that mix kinds.

## Findings

### f3 Minor observation: r31 and r33 can still both hold in one trace, through different operations
- item: b680
- where: scripts/product_coordination.py:70
The reworded r31 excludes the operation that has a property that refers to an operation. It does not exclude a trace whose other operations make it a saga. Take a trace whose lines use three port operations:
- `stock.reserve`, which a port line governs, with no property and no line on its outcomes;
- `stock.allocate` and `stock.hold`, each `compensated by release`.

r31's condition holds through `stock.reserve`, so r31 obliges `port request`. r33's holds through the other two, so r33 obliges `saga`. `coordination` takes one value only. The code returns `saga` from line 63 before it reaches line 70, so the precedence still comes from the code and not from a line.

r32 has the same gap against r33. r32's condition does not exclude a saga's operations, so a saga world in which an outcome handler uses an operation that performs a transition meets both r32 and r33. The code returns `saga`.

No client builds such a world today, and neither the scenario world nor the fixture holds one. Fix it when b689 ("product#r32 excludes a saga's compensated operations, as r31 does") is taken up. That item should also say the exclusion at the job's level ("and the job's trace does not use two operations in a driven port that have a property that refers to an operation"), for r31 as well as r32, and then check that `spec logic` reads the pair clean.

### f4 Minor observation: a code docstring cites a review finding
- item: b680
- where: scripts/product_coordination.py:12
The docstring says "(r31 as reworded by f1, so that a saga's operations are no port request)". A review finding is batch bookkeeping, and the number means nothing once the batch is merged. The requirement id alone (`r31`) says it. Fix: drop "as reworded by f1".

## Earlier findings
- f1: fixed
