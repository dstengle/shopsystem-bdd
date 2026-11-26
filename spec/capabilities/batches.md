---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batches
title: Batches
narrator: the person
group: service
area: execution
specifies: object batch, object task, service batches
language: codified-2
retired: [g69, r69, g82, r82, g88, r88, g53, r53, g59, r59, g51, r51, g103, r103, g50, r50, g54, r54, g55, r55, g57, r57, g58, r58, g65, r65, g89, r89, g93, r93, g94, r94, g97, r97, g101, r101, g107, r107, g138, r138, g140, r140, g139, r139, g136, r136, g137, r137]
unbuilt: [r149, r150, r151]
---

# Batches

## Purpose
Batches of ready items: opened, their tasks finished in workspaces of their own, items parked, abandoned or delivered
when the change is merged.

## Behaviour

### [g52] A batch abandoned keeps no review folder
- [r52] When the person abandons a batch, the batches service shall keep no review folder of the batch.

### [g56] A batch resumed gives its plan and asks nothing
- [r56] While a batch is `building`, when a session resumes the batch, the batches service shall return the batch plan
  of the batch and not ask a question.

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

### [g90] A line removed from an in-batch item leaves its task's workspace too, not only the batch's
- [r90] While an item in a batch is `in-batch` and a task of the item is `running` and the workspace of the batch holds a requirement of the item and the workspace of the task holds the requirement and the item does not hold the requirement, when the person amends the item, the batches service shall keep a workspace of the batch that does not hold the requirement and keep a workspace of the task that does not hold the requirement.

### [g91] An item parked puts back the operation its model line restates
- [r91] While an item in a batch is `in-batch` and the item holds a model line that restates an operation and the domain model holds the model line, when a session parks the item, the batches service shall keep a domain model that holds the operation.

### [g92] A batch opened writes the operation table of an operation an item adds with none given
- [r92] While an item is `ready` and the item meets the readiness bar and the item holds a model line and the model line specifies an operation and the domain model does not hold the operation and the item holds no operation table of the operation, when the person opens a batch, the batches service shall keep an adapter contract that holds an operation table of the operation.

### [g95] A batch opened keeps each term of a pack in the pack, and the pack imported
- [r95] While an item is `ready` and the item meets the readiness bar and the item holds a term of a pack, when the person opens a batch, the batches service shall keep the pack that has the term and keep the pack that this bounded context imports.

### [g96] An in-batch item amended that does not meet the readiness bar is refused and nothing changes
- [r96] While an item in a batch is `in-batch` and the item does not meet the readiness bar, if the person amends the item, then the batches service shall refuse the request, name the item and change nothing.

### [g98] A batch opened keeps a brief that holds each batch rule of the settings file
- [r98] While a settings file holds a batch rule, when the person opens a batch, the batches service shall keep a batch brief that holds the batch rule.

### [g99] A batch opened with no batch rule keeps a brief that holds none
- [r99] While no settings file holds a batch rule, when the person opens a batch, the batches service shall keep a batch brief that holds no batch rule.

### [g102] Every batch summary states its cost and timing
- [r102] When the person merges the proposed change of a batch, the batches service shall keep no review folder of the batch and return the batch summary of the batch.

### [g104] Every batch brief holds the batch summary form
- [r104] When the person opens a batch, the batches service shall keep a batch brief that holds a batch summary form and return the batch brief.

### [g100] Merging a batch's change delivers its items
- [r100] While an item in a batch is `in-batch`, when the person merges the proposed change of the batch, the batches service shall deliver the item and set the status of the batch to `merged`.

### [g110] An item a ready item depends on and that is not ready is not allocated
- [r110] While an item is not `ready` or `delivered` and a dependency on the item exists and another item whose status is `ready` has the dependency, when the person opens a batch, the batches service shall not allocate the item.

### [g111] An item parked is suspended and the batch goes on
- [r111] While an item in a batch is `in-batch`, when a session parks the item, the batches service shall suspend the item with a question and not set the status of the batch to `abandoned`.

### [g112] A batch abandoned restores its items
- [r112] While a batch is `building`, when the person abandons the batch, the batches service shall set the status of the batch to `abandoned` and restore every item in the batch whose status is `in-batch`.

### [g105] Merging a batch's change resolves the accepted context request of its item
- [r105] While an item in a batch is `in-batch` and the item has a request line of a context request and the context request is `accepted`, when the person merges the proposed change of the batch, the batches service shall resolve the context request.

### [g106] A ready item whose lines laid violate a rule is reopened
- [r106] While an item is `ready` and the item meets the readiness bar and a requirement of the item violates a rule whose severity is `error`, if the person opens a batch, then the batches service shall reopen the item and name the rule.

### [g108] A batch opened allocates each ready item within the review limit
- [r108] While an item is `ready` and the item meets the readiness bar and the item has no dependency on an item whose status is not `delivered` and the item does not exceed the review limit, when the person opens a batch, the batches service shall allocate the item, keep a batch that holds the item and keep a batch plan of the batch.

### [g109] A ready item whose new line's scenario passes on the lay is reopened
- [r109] While an item is `ready` and the item meets the readiness bar and a requirement of the item retires no requirement id and a scenario of the item refers to the requirement id of the requirement and the scenario succeeds in a workspace of a batch, if the person opens the batch, then the batches service shall reopen the item and name the scenario.

### [g113] A batch opened keeps the index file in the index form
- [r113] While an item is `ready` and the item meets the readiness bar, when the person opens a batch, the batches service shall keep an index file that conforms to the index form.

### [g114] A batch opened leaves a capability with no requirement out of the index file
- [r114] While a capability has no requirement and an item is `ready` and the item meets the readiness bar, when the person opens a batch, the batches service shall keep an index file that does not hold the capability.

### [g115] A batch opened names a capability with a requirement in the index file
- [r115] While a capability has a requirement and an item is `ready` and the item meets the readiness bar, when the person opens a batch, the batches service shall keep an index file that holds the capability.

### [g116] A model line that restates an element is laid in place of it
- [r116] While an item is `ready` and the item meets the readiness bar and the item holds a model line that restates an element, when the person opens a batch, the batches service shall keep the model line in the domain model and keep a domain model that does not hold the element.

### [g117] A batch opened declares a moved model line in the area it moves to
- [r117] While an item is `ready` and the item meets the readiness bar and the item holds a model line that moves to an area, when the person opens a batch, the batches service shall keep the area that holds the model line.

### [g118] A batch opened writes a moved term into the area that holds its element
- [r118] While an item is `ready` and the item meets the readiness bar and the item moves a term that means an element and an area holds the element, when the person opens a batch, the batches service shall keep the area that holds the term.

### [g119] A park of an item that restates an element keeps a member line another item of the batch adds
- [r119] While an item in a batch holds a model line that holds a member line and another item in the batch holds a model line that restates an element and the element does not hold the member line and the item is `in-batch`, when a session parks the item, the batches service shall keep the member line in the domain model and keep a domain model that does not hold the model line.

### [g120] A model line that restates an event is laid in place of the event
- [r120] While an item is `ready` and the item meets the readiness bar and the item holds a model line that restates an event, when the person opens a batch, the batches service shall keep the model line in the domain model and keep a domain model that does not hold the event.

### [g121] A model line that restates an actor is laid in place of the actor
- [r121] While an item is `ready` and the item meets the readiness bar and the item holds a model line that restates an actor, when the person opens a batch, the batches service shall keep the model line in the domain model and keep a domain model that does not hold the actor.

### [g124] A batch opened keeps the job a requirement group of an item serves
- [r124] While an item is `ready` and the item meets the readiness bar and the item holds a requirement group that serves a job, when the person opens a batch, the batches service shall keep a capability that has a requirement group that serves the job.

### [g125] An item amended with a review finding keeps a change for the finding, which its review accepts
- [r125] While an item in a batch is `in-batch` and a review of the batch holds a review finding, when the person amends the item with the review finding, the batches service shall keep a kept change for the review finding.

### [g128] An item's term of a pack kept when its ids are renumbered
- [r128] While an item is `ready` and the item meets the readiness bar and the item holds a term of a pack and a capability holds a requirement id that the item holds, when the person opens a batch, the batches service shall keep the pack that has the term.

### [g126] An item's operation table kept when its ids are renumbered
- [r126] While an item is `ready` and the item meets the readiness bar and the item holds an operation table and a capability holds a requirement id that the item holds, when the person opens a batch, the batches service shall keep an adapter contract that holds the operation table.

### [g127] An item's moved term kept when its ids are renumbered
- [r127] While an item is `ready` and the item meets the readiness bar and the item moves a term that means an element and an area holds the element and a capability holds a requirement id that the item holds, when the person opens a batch, the batches service shall keep the area that holds the term.

### [g129] A new capability laid with its area is kept in that area
- [r129] While an item is `ready` and the item meets the readiness bar and the item holds a capability and the item holds an area that holds the capability, when the person opens a batch, the batches service shall keep the capability that the area holds.

### [g130] A ready item within the review limit that no longer meets the bar is reopened
- [r130] While an item is `ready` and the item does not meet the readiness bar and the item does not exceed the review limit, when the person opens a batch, the batches service shall reopen the item.

### [g131] A ready item whose change would take the batch past the review limit is not allocated, whether or not it meets the bar
- [r131] While an item is `ready` and the item exceeds the review limit, when the person opens a batch, the batches service shall not allocate the item.

### [g132] A batch opened imports each pack its items import
- [r132] While an item is `ready` and the item meets the readiness bar and the item imports a pack, when the person opens a batch, the batches service shall keep the pack that this bounded context imports.

### [g133] A batch opened takes each retired model line out of the domain model
- [r133] While an item is `ready` and the item meets the readiness bar and the item retires a model line, when the person opens a batch, the batches service shall keep an area that does not hold the model line.

### [g134] A batch opened takes each retired term out of its area
- [r134] While an item is `ready` and the item meets the readiness bar and the item retires a term, when the person opens a batch, the batches service shall keep an area that does not hold the term.

### [g141] A batch whose every task is done asks the driver to submit it
- [r141] While a batch is `building` and every task of the batch is `done`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `submit batch`.

### [g135] A batch awaiting its merge tells the driver to stop
- [r135] While a batch is `awaiting-merge`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `stop`.

### [g142] A batch opened takes out a retired term whose element a retired model line already took out
- [r142] While an item is `ready` and the item meets the readiness bar and the item retires a model line that restates an element and the item retires a term that means the element, when the person opens a batch, the batches service shall keep an area that does not hold the term.

### [g143] A batch with a failed task of an in-batch item asks the driver to park the task's item
- [r143] While a batch is `building` and a task of an item in the batch is `failed` and the item is `in-batch`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `park item` and the task.

### [g144] A batch with a built running task and no failed task asks the driver to finish the task
- [r144] While a batch is `building` and a task of an item in the batch is `running` and the item is `in-batch` and the workspace of the task holds a kept change that cites the item and no task of the batch is `failed`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `finish task` and the task.

### [g145] A batch with an unbuilt running task and no failed task asks the driver to build the task with its brief
- [r145] While a batch is `building` and a task of an item in the batch is `running` and the item is `in-batch` and the workspace of the task holds no kept change that cites the item and no task of the batch is `failed`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `build task`, the task and the batch brief of the batch.

### [g146] A batch with a pending task and no failed or running task asks the driver to prepare the task
- [r146] While a batch is `building` and a task of an item in the batch is `pending` and the item is `in-batch` and no task of the batch is `failed` and no task of the batch is `running`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `prepare task` and the task.

### [g147] A batch in review asks the driver to review its change with the review folder and its findings file
- [r147] While a batch is `in-review`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `review change`, a review folder of the batch and a findings file in the review folder.

### [g148] A batch with a finding to fix now that no kept change is for asks the driver to fix the finding
- [r148] While a batch is `building` and a review of the batch holds a review finding whose triage is `fix now` and no kept change for the review finding exists, when the driver polls the batch, the batches service shall return a batch step whose instruction is `fix finding` and the review finding.

### [g149] A batch whose submit a scenario of an item broke asks the driver to fix the item's task
- [r149] While a batch is `building` and a task of an item in the batch is `done` and every task of the batch is `done` and a scenario of the item breaks in the workspace of the batch, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `fix task` and the task.

### [g150] A running task whose only kept change citing its item is an amendment asks the driver to build it
- [r150] While a batch is `building` and a task of an item in the batch is `running` and the item is `in-batch` and the workspace of the task holds an amendment that cites the item and the workspace of the task holds exactly one kept change that cites the item and no task of the batch is `failed`, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `build task`, the task and the batch brief of the batch.

### [g151] A new capability laid with its driven port is kept in an area of kind port
- [r151] While an item is `ready` and the item meets the readiness bar and the item holds a capability and the item holds a driven port that holds the capability, when the person opens a batch, the batches service shall keep the driven port that holds the capability.

