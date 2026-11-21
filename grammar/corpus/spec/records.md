# records: every live line with its intended reading (the domain contract, 0.38.0)

## r1
From: design-model-check#r56, reworded in request words (0.38.0).

```reading
When the person files a record, the records service shall keep the record.
shall [x1: agent the person (constant), x3: service the records service (constant)]
  when [x2: record]
    request(e1, records.file, subject: x1, object: x2)
  response
    keep(e2, subject: x3, object: x2)
```

## r2
From: design-model-check#r204, reworded in request words (0.38.0).

```reading
If the person files a record with a text that does not conform to the node id form, then the records service shall refuse the request and name the text.
shall [x1: agent the person (constant), x4: artifact the node id form (constant), x5: service the records service (constant), x6: request "the request the trigger makes" (indexical)]
  if [x2: record, x3: text]
    not
      conforms(x3, x4)
    request(e1, records.file, subject: x1, object: x2)
    param(e1, text, x3)
  response
    refuse(e2, subject: x5, object: x6)
    name(e3, subject: x5, object: x3)
```

## r3
From: b49 r3.

```reading
When the person files a record with a text that denotes an item, the records service shall keep the record that concerns the item.
shall [x1: agent the person (constant), x5: service the records service (constant)]
  when [x2: record, x3: text, x4: item]
    denote(subject: x3, object: x4)
    request(e1, records.file, subject: x1, object: x2)
    param(e1, text, x3)
  response
    concern(subject: x2, object: x4)
    keep(e2, subject: x5, object: x2)
```

## r5
From: b49 r5.

```reading
While a text denotes no node and the text denotes no item and the text denotes no batch, if the person files a record with the text, then the records service shall refuse the request and name the text.
shall [x5: agent the person (constant), x7: service the records service (constant), x8: request "the request the trigger makes" (indexical)]
  while [x1: text]
    not [x2: node]
      denote(subject: x1, object: x2)
    not [x3: item]
      denote(subject: x1, object: x3)
    not [x4: batch]
      denote(subject: x1, object: x4)
  if [x6: record]
    request(e1, records.file, subject: x5, object: x6)
    param(e1, text, x6)
  response
    refuse(e2, subject: x7, object: x8)
    name(e3, subject: x7, object: x6)
```

## r6
From: b49 r6.

```reading
When the person files a record with a text that denotes a batch, the records service shall keep the record that concerns the batch.
shall [x1: agent the person (constant), x5: service the records service (constant)]
  when [x2: record, x3: text, x4: batch]
    denote(subject: x3, object: x4)
    request(e1, records.file, subject: x1, object: x2)
    param(e1, text, x3)
  response
    concern(subject: x2, object: x4)
    keep(e2, subject: x5, object: x2)
```
