---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batches
title: Batches
narrator: the person
group: service
area: execution
specifies: object batch, object task, service batches
language: codified-2
retired: [g69, r69]
unbuilt: [r89]
---

# Batches

## Purpose
Batches of ready items: opened, their tasks finished in workspaces of their own, items parked, abandoned or delivered
when the change is merged.

## Behaviour

### [g50] Merging a batch's change delivers its items
- [r50] While an item in a batch is `in-batch`, when the person merges the proposed change of the batch, the batches
  service shall set the status of the item to `delivered` and set the status of the batch to `merged`.

### [g51] A batch opened keeps and gives its brief
- [r51] When the person opens a batch, the batches service shall keep a batch brief and return the batch brief.

### [g52] A batch abandoned keeps no review folder
- [r52] When the person abandons a batch, the batches service shall keep no review folder of the batch.

### [g53] A ready item that meets the bar and depends on nothing open goes into the batch opened
- [r53] While an item is `ready` and the item meets the readiness bar and the item has no dependency on an item whose
  status is not `delivered`, when the person opens a batch, the batches service shall set the status of the item to
  `in-batch`, keep a batch that holds the item and keep a batch plan of the batch.

### [g54] A ready item that no longer meets the bar goes back to shaped
- [r54] While an item is `ready` and the item does not meet the readiness bar, when the person opens a batch, the
  batches service shall set the status of the item to `shaped`.

### [g55] An item a ready item depends on and that is not ready stays out of the batch
- [r55] While an item is not `ready` or `delivered` and a dependency on the item exists and another item whose status is
  `ready` has the dependency, when the person opens a batch, the batches service shall not set the status of the item to
  `in-batch`.

### [g56] A batch resumed gives its plan and asks nothing
- [r56] While a batch is `building`, when a session resumes the batch, the batches service shall return the batch plan
  of the batch and not ask a question.

### [g57] An item parked needs input and the batch goes on
- [r57] While an item in a batch is `in-batch`, when a session parks the item, the batches service shall set the status
  of the item to `needs-input`, keep a question on the item and not set the status of the batch to `abandoned`.

### [g58] A batch abandoned gives its items back as ready
- [r58] While a batch is `building`, when the person abandons the batch, the batches service shall set the status of the
  batch to `abandoned` and set the status of every item in the batch whose status is `in-batch` to `ready`.

### [g59] A batch whose change is merged keeps no review folder
- [r59] When the person merges the proposed change of a batch, the batches service shall keep no review folder of the
  batch.

### [g60] An item parked has its lines taken out of the batch's workspace
- [r60] While an item in a batch is `in-batch` and the workspace of the batch holds a requirement of the item, when a
  session parks the item, the batches service shall keep a workspace of the batch that does not hold the requirement.

### [g61] A task finishes while a parked item's scenario breaks
- [r61] While an item in a batch is `in-batch` and a task of the item is `running` and the status of an item in the
  batch is `needs-input` and a scenario of the item breaks in the workspace of the task, when a session finishes the
  task, the batches service shall set the status of the task to `done`.

### [g62] A task finishes while another item's scenario succeeds
- [r62] While an item in a batch is `in-batch` and a task of the item is `running` and another item in the batch is
  `in-batch` and a scenario of the item succeeds in the workspace of the task, when a session finishes the task, the
  batches service shall set the status of the task to `done`.

### [g63] A batch monitored gives its items, tasks and their status
- [r63] While a batch holds an item and the batch has a task, when the person monitors the batch, the batches service
  shall return the item, the task and the status of the task.

### [g64] A batch opened with a universal condition keeps the universal conditions in the language
- [r64] While `universal` does not exist and an item is `ready` and the item meets the readiness bar and a universal
  condition is in the item, when the person opens a batch, the batches service shall keep `universal` and set the
  language of `universal` to `codified-2`.

### [g65] Merging a batch's change resolves the accepted context request of its item
- [r65] While an item in a batch is `in-batch` and the item has a request line of a context request and the context
  request is `accepted`, when the person merges the proposed change of the batch, the batches service shall set the
  status of the context request to `delivered`, keep a resolution, set the side of the context request to `asker` and
  keep an entry on the context request.

### [g66] A task whose chore breaks is not finished
- [r66] While a task of an item is `running` and the item holds a chore and the chore breaks in the workspace of the
  task, if a session finishes the task, then the batches service shall refuse the request and name the chore.

### [g67] A task that touches a file outside its chore is not finished
- [r67] While a task of an item is `running` and the item holds a chore and a kept change in the workspace of the task
  touches a file that is not in the chore, if a session finishes the task, then the batches service shall refuse the
  request and name the file.

### [g68] A batch opened keeps a brief that holds each chore
- [r68] While an item is `ready` and the item holds a chore and the item meets the readiness bar, when the person opens
  a batch, the batches service shall keep a batch brief that holds the chore.

### [g70] A task finishes while a parked item's line is out of the batch
- [r70] While an item in a batch is `in-batch` and a task of the item is `running` and the status of an item in the
  batch is `needs-input` and the item has a requirement that is not in the workspace of the batch and a scenario of the
  item breaks in the workspace of the task, when a session finishes the task, the batches service shall set the status
  of the task to `done`.

### [g71] A batch opened keeps each line's logical form in the corpus
- [r71] While an item is `ready` and the item meets the readiness bar and a requirement of the item has a logical form,
  when the person opens a batch, the batches service shall keep the logical form in the corpus.

### [g72] A batch opened takes a retired requirement out of the corpus
- [r72] While an item is `ready` and the item meets the readiness bar and a requirement id is in the item and a
  requirement in the corpus has the requirement id, when the person opens a batch, the batches service shall keep a
  corpus that does not hold the requirement.

### [g73] A batch opened keeps the catalogue entry of each rule its lines use
- [r73] While an item is `ready` and the item meets the readiness bar and a requirement of the item uses a rule, when
  the person opens a batch, the batches service shall keep the catalogue entry of the rule.

### [g74] A batch opened keeps the construct catalogue its lines use
- [r74] While an item is `ready` and the item meets the readiness bar and a requirement of the item uses a construct,
  when the person opens a batch, the batches service shall keep the construct catalogue.

### [g75] A batch opened keeps no construct catalogue for lines that use no construct
- [r75] While no requirement of an item whose status is `ready` uses a construct and no construct catalogue exists, when the person opens a batch, the batches service shall keep no construct catalogue.

### [g76] A new capability is laid in 0.38's form: area:, specifies:, no empty ## Terms, one ## Composition
- [r76] While an item is `ready` and the item meets the readiness bar and the item holds a capability, when the person opens a batch, the batches service shall keep the capability that conforms to the capability form and keep an index file that conforms to the index form.

### [g77] A task finishes with its tests run by the workspace's virtual environment
- [r77] While a task of an item is `running` and the workspace of the task holds a virtual environment and a scenario of the item succeeds in the workspace of the task, when a session finishes the task, the batches service shall set the status of the task to `done`.

### [g78] A task finishes while a scenario its change does not reach breaks
- [r78] While a task of an item is `running` and a scenario breaks in the workspace of the task and the scenario has a capability and the item holds no requirement id that is in the capability and no kept change in the workspace of the task touches the feature of the capability, when a session finishes the task, the batches service shall set the status of the task to `done`.

### [g79] An operation table of an item is laid into the adapter contract
- [r79] While an item is `ready` and the item meets the readiness bar and the item holds an operation table, when the person opens a batch, the batches service shall keep an adapter contract that holds the operation table.

### [g80] An operation withheld in an item leaves the adapter contract
- [r80] While an item is `ready` and the item meets the readiness bar and the item holds an operation, when the person opens a batch, the batches service shall keep an adapter contract and keep no operation table of the operation.

### [g81] An in-batch item amended has its lines laid again on its batch's and its task's workspaces
- [r81] While an item in a batch is `in-batch` and a task of the item is `running` and the item holds a requirement, when the person amends the item, the batches service shall keep a workspace of the batch that holds the requirement and keep a workspace of the task that holds the requirement.

### [g82] An in-batch item amended has a line it no longer holds taken out of the batch's workspace
- [r82] While an item in a batch is `in-batch` and the workspace of the batch holds a requirement of the item and the item does not hold the requirement, when the person amends the item, the batches service shall keep a workspace of the batch that does not hold the requirement.

### [g83] Amending an item that is not in a batch is refused
- [r83] While an item is not `in-batch`, if the person amends the item, then the batches service shall refuse the request and name the item.

### [g84] `work settings set` writes a setting in its own table
- [r84] When the person configures a setting with a setting value, the batches service shall keep a settings file that holds the setting, keep the settings file that conforms to the delivery settings form and complete the request.

### [g85] `work settings set` refuses a setting the plugin does not read
- [r85] If the person configures a setting that does not conform to the delivery settings form, then the batches service shall refuse the request and name the setting.

### [g86] `work settings set` refuses a value of the wrong type
- [r86] If the person configures a setting with a setting value that does not conform to the delivery settings form, then the batches service shall refuse the request and name the setting value.

### [g87] A batch opened lays a model line in place of the operation it restates
- [r87] While an item is `ready` and the item meets the readiness bar and the item holds a model line that restates an operation, when the person opens a batch, the batches service shall keep the model line in the domain model and keep a domain model that does not hold the operation.

### [g88] An item parked takes its restating model line out of the domain model
- [r88] While an item in a batch is `in-batch` and the item holds a model line that restates an operation and the domain model holds the model line, when a session parks the item, the batches service shall keep a domain model that does not hold the model line.

### [g89] A ready item whose lines laid violate a rule goes back to shaped
- [r89] While an item is `ready` and the item meets the readiness bar and a requirement of the item violates a rule whose severity is `error`, if the person opens a batch, then the batches service shall set the status of the item to `shaped` and name the rule.

