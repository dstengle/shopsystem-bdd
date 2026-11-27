# laying: every live line with its intended reading

## r2
From: b611 r2.

```reading
While a workspace holds a requirement of an item, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
shall [x4: service the batches service (constant), x5: service the laying service (constant)]
  while [x1: workspace, x2: requirement, x3: item]
    of(x2, x3)
    in(x2, x1)
  when
    request(e1, laying.lift, subject: x4, object: x3, from: x1)
  response [x6: workspace]
    not
      in(x2, x6)
    keep(e2, subject: x5, object: x6)
```

## r5
From: b755 r5.

```reading
While an item holds a requirement that retires the requirement id of a requirement of a requirement group and a workspace holds another requirement that retires the requirement id of another requirement of the requirement group, when the batches service lifts the item from the workspace, the laying service shall keep a workspace that does not hold the requirement.
shall [x10: service the batches service (constant), x11: service the laying service (constant)]
  while [x1: item, x2: requirement, x3: requirement, x4: requirement group, x5: requirement id, x6: workspace, x7: requirement, x8: requirement, x9: requirement id]
    of(x3, x4)
    of(x5, x3)
    retire(subject: x2, object: x5)
    in(x2, x1)
    distinct(x7, x3)
    distinct(x8, x3)
    of(x8, x4)
    of(x9, x8)
    retire(subject: x7, object: x9)
    in(x7, x6)
  when
    request(e1, laying.lift, subject: x10, object: x1, from: x6)
  response [x12: workspace]
    not
      in(x8, x12)
    keep(e2, subject: x11, object: x12)
```

## r43
From: b747 r43.

```reading
While an item holds a model line that restates an operation and the domain model holds the model line, when the batches service lifts the item from a workspace, the laying service shall keep a domain model that holds the operation.
shall [x4: domain model "the domain model of this bounded context" (indexical), x5: service the batches service (constant), x7: service the laying service (constant)]
  while [x1: item, x2: model line, x3: operation]
    restate#2(subject: x2, object: x3)
    in(x2, x1)
    in(x2, x4)
  when [x6: workspace]
    request(e1, laying.lift, subject: x5, object: x1, from: x6)
  response [x8: domain model]
    in(x3, x8)
    keep(e2, subject: x7, object: x8)
```

## r44
From: b747 r44.

```reading
While an item holds a model line that holds a member line and another item holds a model line that restates an element and the element does not hold the member line, when the batches service lifts the item from a workspace, the laying service shall keep the member line in the domain model and keep a domain model that does not hold the model line.
shall [x7: service the batches service (constant), x9: service the laying service (constant), x10: domain model "the domain model of this bounded context" (indexical)]
  while [x1: item, x2: model line, x3: member line, x4: item, x5: model line, x6: element]
    in(x3, x2)
    in(x2, x1)
    distinct(x4, x1)
    restate(subject: x5, object: x6)
    in(x5, x4)
    not
      in(x3, x6)
  when [x8: workspace]
    request(e1, laying.lift, subject: x7, object: x4, from: x8)
  response [x11: domain model]
    in(x3, x10)
    keep(e2, subject: x9, object: x3)
    not
      in(x5, x11)
    keep(e3, subject: x9, object: x11)
```

## r45
From: b747 r45.

```reading
While the kind of an area is `port` and the area holds a capability that an item holds and the area imports an area whose kind is `supporting`, when the batches service lifts another item from a workspace, the laying service shall keep the area.
shall [x5: service the batches service (constant), x8: service the laying service (constant)]
  while [x1: area, x2: capability, x3: item, x4: area]
    kind(x1) = `port`
    in(x2, x3)
    in(x2, x1)
    kind(x4) = `supporting`
    import#3(subject: x1, object: x4)
  when [x6: item, x7: workspace]
    distinct(x6, x3)
    request(e1, laying.lift, subject: x5, object: x6, from: x7)
  response
    keep(e2, subject: x8, object: x4)
```

## r46
Retires: r42. From: b765 r46.

```reading
While the kind of the `registry` area is `port` and an item holds a capability that the `registry` area holds and the `registry` area imports the `tracking` area, when the batches service lifts the item from a workspace, the laying service shall keep the `registry` area and keep an area that does not import the `tracking` area.
shall [x1: area `registry` (parameter), x4: area `tracking` (parameter), x5: service the batches service (constant), x7: service the laying service (constant)]
  while [x2: item, x3: capability]
    kind(x1) = `port`
    in(x3, x1)
    in(x3, x2)
    import#3(subject: x1, object: x4)
  when [x6: workspace]
    request(e1, laying.lift, subject: x5, object: x2, from: x6)
  response [x8: area]
    keep(e2, subject: x7, object: x1)
    not
      import#3(subject: x8, object: x4)
    keep(e3, subject: x7, object: x8)
```

## r47
From: b761 r47.

```reading
While an item holds a requirement that retires the requirement id of a requirement of a requirement group and a workspace holds another requirement that retires the requirement id of another requirement of the requirement group and the requirement supports a requirement id, when the batches service lifts the item from the workspace, the laying service shall keep a requirement of the requirement group that does not support the requirement id.
shall [x11: service the batches service (constant), x12: service the laying service (constant)]
  while [x1: item, x2: requirement, x3: requirement, x4: requirement group, x5: requirement id, x6: workspace, x7: requirement, x8: requirement, x9: requirement id, x10: requirement id]
    of(x3, x4)
    of(x5, x3)
    retire(subject: x2, object: x5)
    in(x2, x1)
    distinct(x7, x3)
    distinct(x8, x3)
    of(x8, x4)
    of(x9, x8)
    retire(subject: x7, object: x9)
    in(x7, x6)
    support(subject: x8, object: x10)
  when
    request(e1, laying.lift, subject: x11, object: x1, from: x6)
  response [x13: requirement]
    of(x13, x4)
    not
      support(subject: x13, object: x10)
    keep(e2, subject: x12, object: x13)
```
