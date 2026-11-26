---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/batches
title: Batches
narrator: the person
group: service
area: execution
specifies: object batch, object task, service batches
language: codified-2
retired: [g69, r69, g82, r82, g88, r88, g53, r53, g59, r59, g51, r51, g103, r103, g50, r50, g54, r54, g55, r55, g57, r57, g58, r58, g65, r65, g89, r89, g93, r93, g94, r94, g97, r97, g101, r101, g107, r107, g138, r138, g140, r140, g139, r139, g136, r136, g137, r137, g145, r145, g146, r146, g152, r152, g149, r149, g154, r154, g160, r160, g166, r166, g108, r108, g106, r106, g60, r60, g130, r130, g71, r71, g72, r72, g73, r73, g74, r74, g75, r75, g113, r113, g114, r114, g115, r115, g157, r157, g164, r164, g167, r167, g169, r169, g64, r64, g95, r95, g128, r128, g132, r132, g76, r76, g124, r124, g129, r129, g151, r151, g79, r79, g80, r80, g92, r92, g126, r126, g87, r87, g116, r116, g120, r120, g121, r121, g117, r117, g118, r118, g127, r127, g133, r133, g134, r134, g142, r142, g81, r81, g90, r90, g156, r156, g91, r91, g119, r119, g155, r155]
unbuilt: []
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

### [g77] A task finishes with its tests run by the workspace's virtual environment
- [r77] While a task of an item is `running` and the workspace of the task holds a virtual environment and a scenario of the item succeeds in the workspace of the task, when a session finishes the task, the batches service shall set the status of the task to `done`.

### [g78] A task finishes while a scenario its change does not reach breaks
- [r78] While a task of an item is `running` and a scenario breaks in the workspace of the task and the scenario has a capability and the item holds no requirement id that is in the capability and no kept change in the workspace of the task touches the feature of the capability, when a session finishes the task, the batches service shall set the status of the task to `done`.

### [g83] Amending an item that is not in a batch is refused
- [r83] While an item is not `in-batch`, if the person amends the item, then the batches service shall refuse the request and name the item.

### [g84] `work settings set` writes a setting in its own table
- [r84] When the person configures a setting with a setting value, the batches service shall keep a settings file that holds the setting, keep the settings file that conforms to the delivery settings form and complete the request.

### [g85] `work settings set` refuses a setting the plugin does not read
- [r85] If the person configures a setting that does not conform to the delivery settings form, then the batches service shall refuse the request and name the setting.

### [g86] `work settings set` refuses a value of the wrong type
- [r86] If the person configures a setting with a setting value that does not conform to the delivery settings form, then the batches service shall refuse the request and name the setting value.

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

### [g109] A ready item whose new line's scenario passes on the lay is reopened
- [r109] While an item is `ready` and the item meets the readiness bar and a requirement of the item retires no requirement id and a scenario of the item refers to the requirement id of the requirement and the scenario succeeds in a workspace of a batch, if the person opens the batch, then the batches service shall reopen the item and name the scenario.

### [g125] An item amended with a review finding keeps a change for the finding, which its review accepts
- [r125] While an item in a batch is `in-batch` and a review of the batch holds a review finding, when the person amends the item with the review finding, the batches service shall keep a kept change for the review finding.

### [g131] A ready item whose change would take the batch past the review limit is not allocated, whether or not it meets the bar
- [r131] While an item is `ready` and the item exceeds the review limit, when the person opens a batch, the batches service shall not allocate the item.

### [g141] A batch whose every task is done asks the driver to submit it
- [r141] While a batch is `building` and every task of the batch is `done`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `submit batch`.

### [g135] A batch awaiting its merge tells the driver to stop
- [r135] While a batch is `awaiting-merge`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `stop`.

### [g143] A batch with a failed task of an in-batch item asks the driver to park the task's item
- [r143] While a batch is `building` and a task of an item in the batch is `failed` and the item is `in-batch`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `park item` and the task.

### [g144] A batch with a built running task and no failed task asks the driver to finish the task
- [r144] While a batch is `building` and a task of an item in the batch is `running` and the item is `in-batch` and the workspace of the task holds a kept change that cites the item and no task of the batch is `failed`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `finish task` and the task.

### [g147] A batch in review asks the driver to review its change with the review folder and its findings file
- [r147] While a batch is `in-review`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `review change`, a review folder of the batch and a findings file in the review folder.

### [g148] A batch with a finding to fix now that no kept change is for asks the driver to fix the finding
- [r148] While a batch is `building` and a review of the batch holds a review finding whose triage is `fix now` and no kept change for the review finding exists, when the driver polls the batch, the batches service shall return a batch step whose instruction is `fix finding` and the review finding.

### [g150] A running task whose only kept change citing its item is an amendment asks the driver to build it
- [r150] While a batch is `building` and a task of an item in the batch is `running` and the item is `in-batch` and the workspace of the task holds an amendment that cites the item and the workspace of the task holds exactly one kept change that cites the item and no task of the batch is `failed`, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `build task`, the task and the batch brief of the batch.

### [g153] A batch with pending tasks and no failed or running task asks the driver to prepare every pending task
- [r153] While a batch is `building` and two tasks of items in the batch are `pending` and no task of the batch is `failed` and no task of the batch is `running`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `prepare task` and every task of the batch whose status is `pending`.

### [g158] A batch whose task branches conflict is polled for the later item's task and the file
- [r158] While a batch is `building` and every task of the batch is `done` and a kept change that cites an item in the batch touches a file and the kept change conflicts with another kept change, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `fix task`, the task of the item and the file.

### [g159] A batch with running tasks none of which is built asks the driver to build every running task with its brief
- [r159] While a batch is `building` and two tasks of items in the batch are `running` and no task of the batch is `failed` and no workspace of a task of the batch holds a kept change that cites an item in the batch, when the driver polls the batch, the batches service shall return a batch step whose instruction is `build task`, every task of the batch whose status is `running` and the batch brief of the batch.

### [g163] A batch whose failure has a fix is polled for its submit
- [r163] While a batch is `building` and every task of the batch is `done` and a scenario breaks in the workspace of the batch and a fix exists, when the driver polls the batch, the batches service shall return a batch step whose instruction is `submit batch`.

### [g161] A batch whose item's scenario breaks with no fix is polled for the item's task
- [r161] While a batch is `building` and a task of an item in the batch is `done` and every task of the batch is `done` and a scenario of the item breaks in the workspace of the batch and no fix exists, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `fix task` and the task.

### [g162] A batch whose other scenario breaks with no fix is polled to look at the failure
- [r162] While a batch is `building` and every task of the batch is `done` and a scenario breaks in the workspace of the batch and no scenario of an item in the batch breaks in the workspace of the batch and no fix exists, if the driver polls the batch, then the batches service shall return a batch step whose instruction is `look at failure` and the scenario.

### [g165] A building batch whose every item is parked is polled for its abandonment
- [r165] While a batch is `building` and the status of every item in the batch is `needs-input`, when the driver polls the batch, the batches service shall return a batch step whose instruction is `abandon batch`.

### [g168] An item whose port outcomes were unhandled before it is allocated at the opening
- [r168] While an item is `ready` and the item meets the readiness bar and the item has no dependency on an item whose status is not `delivered` and the item does not exceed the review limit and the item holds a port line that governs an operation and another port line that governs the operation is not in the item and the operation has an operation outcome and no core line handles the operation outcome and no port line excludes the operation outcome, when the person opens a batch, the batches service shall allocate the item.

### [g170] An in-batch item amended has its features written by the generator its batch's workspace holds
- [r170] While an item in a batch is `in-batch` and a task of the item is `running` and the item holds a requirement and the workspace of the batch has a feature generator, when the person amends the item, the batches service shall keep a workspace of the batch that holds a feature of the feature generator.

### [g171] An in-batch item amended with no review finding given keeps a change for the review finding its batch holds open
- [r171] While an item in a batch is `in-batch` and a review of the batch holds a review finding, when the person amends the item, the batches service shall keep a kept change for the review finding.

### [g172] An in-batch item amended keeps a corpus that conforms to the corpus form
- [r172] While an item in a batch is `in-batch` and a task of the item is `running` and the item holds a requirement and this corpus holds the requirement, when the person amends the item, the batches service shall keep a corpus that conforms to the corpus form and keep a workspace of the batch that holds the corpus.

### [g173] A batch opened supersedes each accepted decision a laid line's retirement leaves unenforced
- [r173] While an item is `ready` and the item meets the readiness bar and the item holds a requirement and the requirement retires the requirement id of a requirement that enforces a design-decision whose status is `accepted`, when the person opens a batch, the batches service shall set the status of the design-decision to `superseded`, keep a design-decision that supersedes the design-decision and name the design-decision.

### [g174] A parked item's superseding decision leaves the batch and the decision it superseded is accepted again
- [r174] While an item in a batch is `in-batch` and the item holds a requirement and the requirement retires the requirement id of a requirement that enforces a design-decision whose status is `superseded`, when the person parks the item, the batches service shall set the status of the design-decision to `accepted` and keep no design-decision that supersedes the design-decision.

### [g175] An in-batch item amended while its batch's feature generator is unresponsive is refused, naming the generator
- [r175] While an item in a batch is `in-batch` and a task of the item is `running` and the workspace of the batch has a feature generator and the feature generator is `unresponsive`, if the person amends the item, then the batches service shall refuse the request, name the feature generator and change nothing.

### [g176] An in-batch item parked while its batch's feature generator is unresponsive is refused, naming the generator
- [r176] While an item in a batch is `in-batch` and a task of the item is `running` and the workspace of the batch has a feature generator and the feature generator is `unresponsive`, if the person parks the item, then the batches service shall refuse the request, name the feature generator and change nothing.

### [g177] A batch opened with two items retiring ids of one decision supersedes it by one decision every retiring line enforces
- [r177] While an item is `ready` and the item meets the readiness bar and the item holds a requirement and the requirement retires the requirement id of a requirement that enforces a design-decision whose status is `accepted` and a requirement that enforces the design-decision has a requirement id and another item that meets the readiness bar holds another requirement and the requirement retires the requirement id, when the person opens a batch, the batches service shall keep a design-decision that the requirement enforces.

### [g178] A park of one of two items retiring ids of one decision keeps the decision superseded by the other item's line
- [r178] While an item in a batch is `in-batch` and the item holds a requirement and the requirement retires the requirement id of a requirement that enforces a design-decision whose status is `superseded` and a requirement that enforces the design-decision has a requirement id and another requirement retires the requirement id, when the person parks the item, the batches service shall keep a design-decision that the requirement enforces.

### [g179] An item allocated to a batch is laid in the batch's workspace
- [r179] While an item is `ready` and the item meets the readiness bar and the item has no dependency on an item whose status is not `delivered` and the item does not exceed the review limit, when the person opens a batch, the batches service shall allocate the item, keep a batch that holds the item, keep a batch plan of the batch and lay the item in the workspace of the batch.

### [g180] An item the laying service has laid is checked in the workspace
- [r180] When the laying service completes the request to lay an item in a workspace, the batches service shall check the item in the workspace.

### [g181] An item whose check the laying service fails is reopened naming the rules it violates
- [r181] When the laying service fails the request to check an item in a workspace, the batches service shall reopen the item and name every rule that a requirement of the item violates.

### [g182] An item parked is lifted from the batch's workspace
- [r182] While an item in a batch is `in-batch` and the workspace of the batch holds a requirement of the item, when a session parks the item, the batches service shall lift the item from the workspace of the batch.

### [g183] An item the laying service has lifted is kept out in a change that cites it
- [r183] When the laying service completes the request to lift an item from a workspace, the batches service shall keep a kept change that cites the item.

### [g184] An item whose check the laying service completes is kept in a change that cites it
- [r184] When the laying service completes the request to check an item in a workspace, the batches service shall keep a kept change that cites the item.

### [g187] A ready item that no longer meets the readiness bar at opening is reopened naming each bar check it does not meet
- [r187] While an item is `ready` and the item does not meet the readiness bar and the item does not exceed the review limit, when the person opens a batch, the batches service shall reopen the item and name every bar check that the item does not meet.

### [g188] A workspace in which an item of a batch is laid is prepared for the batch
- [r188] While a batch holds an item, when the laying service completes the request to lay the item in a workspace, the batches service shall prepare the workspace for the batch.

### [g189] Each item of a batch is checked again once the laying service has prepared the workspace for the batch
- [r189] While a batch holds an item, when the laying service completes the request to prepare a workspace for the batch, the batches service shall check the item in the workspace.

### [g185] An amended item is lifted from the workspaces of its batch and task and laid there again
- [r185] While an item in a batch is `in-batch` and a task of the item is `running`, when the person amends the item, the batches service shall lift the item from the workspace of the batch, lift the item from the workspace of the task, lay the item in the workspace of the batch and lay the item in the workspace of the task.

