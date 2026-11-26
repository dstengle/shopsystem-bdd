---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/reviews
title: Reviews
narrator: the person
group: service
area: execution
specifies: object review, object proposed change, service batches: submit
language: codified-2
retired: []
unbuilt: []
---

# Reviews

## Purpose
A batch's change submitted for review once its tasks are done, holding only the kept changes of the items still in it.

## Behaviour

### [g1] A batch submitted keeps a change that cites its items
- [r1] While an item in a batch is `in-batch`, when the person submits the batch, the batches service shall keep a
  proposed change of the batch that cites the item.

### [g2] A batch's change holds no kept change of a parked item
- [r2] While the status of an item in a batch is `needs-input` and a kept change cites the item, when the person submits
  the batch, the batches service shall keep a proposed change of the batch that does not hold the kept change.

### [g3] A batch with a task not done is not submitted
- [r3] While a task of a batch is not `done`, if the person submits the batch, then the batches service shall refuse the
  request and name the task.

### [g4] A batch with a kept change that cites no item is not submitted
- [r4] While a workspace of a task of a batch holds a kept change that cites no item, if the person submits the batch,
  then the batches service shall refuse the request and name the kept change.

### [g5] A batch whose tasks are done is submitted for review
- [r5] While a batch is `building` and every task of the batch is `done`, when the person submits the batch, the batches
  service shall keep a proposed change of the batch and set the status of the batch to `in-review`.

### [g6] A batch is submitted with its tests run by the batch's virtual environment
- [r6] While a batch is `building` and every task of the batch is `done` and the workspace of the batch holds a virtual environment, when the person submits the batch, the batches service shall keep a proposed change of the batch and set the status of the batch to `in-review`.

### [g7] A batch whose task branches touch one file without a conflict is submitted, merged in task order
- [r7] While a batch is `building` and every task of the batch is `done` and an item in the batch is `in-batch` and a kept change that touches a file cites the item and another kept change touches the file and another item in the batch is `in-batch` and the kept change cites the item and no kept change conflicts with a kept change, when the person submits the batch, the batches service shall keep a proposed change of the batch that holds the kept change and set the status of the batch to `in-review`.

### [g8] A batch whose task branches conflict is not submitted, naming the file and both items
- [r8] While an item in a batch is `in-batch` and a kept change cites the item and another item in the batch is `in-batch` and the kept change conflicts with another kept change that cites the item and the kept change touches a file, if the person submits the batch, then the batches service shall refuse the request and name the file, the item and every item in the batch that a kept change that conflicts with the kept change cites.

### [g9] A batch awaiting its merge whose branch merged its base is submitted for review again
- [r9] While a batch is `awaiting-merge` and the workspace of the batch holds a base merge, when the person submits the batch, the batches service shall keep a proposed change of the batch and set the status of the batch to `in-review`.

### [g10] A batch awaiting its merge with no base merge is not submitted
- [r10] While a batch is `awaiting-merge` and the workspace of the batch holds no base merge, if the person submits the batch, then the batches service shall refuse the request and name the batch.

### [g11] A person's finding on a batch awaiting its merge reopens the batch
- [r11] While a batch is `awaiting-merge`, when the person reopens the batch with a review finding, the batches service shall keep a review of the batch that holds the review finding and set the status of the batch to `building`.

### [g12] A batch not awaiting its merge is not reopened
- [r12] While a batch is not `awaiting-merge`, if the person reopens the batch with a review finding, then the batches service shall refuse the request and name the batch.

### [g13] A batch whose amended line its task built is submitted with the line built
- [r13] While an item in a batch is `in-batch` and every task of the batch is `done` and the workspace of the batch holds an amendment that cites the item and a scenario of the item succeeds in the workspace of a task of the item, when the person submits the batch, the batches service shall keep a proposed change of the batch and set the status of the batch to `in-review`.

### [g14] A fix after a review of a scenario its item's change broke is accepted on submit
- [r14] While a batch is `building` and every task of the batch is `done` and a review of the batch exists and an item in the batch is `in-batch` and a scenario of the item succeeds in the workspace of the batch and the workspace of a task of the item holds a kept change that cites the item, when the person submits the batch, the batches service shall keep a proposed change of the batch and set the status of the batch to `in-review`.

