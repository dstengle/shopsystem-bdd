---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/backlog
title: Backlog
narrator: a person or session keeping the backlog
group: service
language: codified-2
rests_on: [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-workflow-simplified]
retired: [g1, r1, g2, r2, g3, r3, g4, r4, g6, r6, g7, r7, g8, r8, g9, r9, g10, r10, g11, r11, g12, r12, g13, r13, g14, r14, g16, r16, g17, r17, g18, r18, g19, r19, g20, r20, g21, r21]
unbuilt: [r5, r15, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36]
---

# Backlog

## Purpose
`work` keeps the backlog of a bounded context in the repository, so that any session can read or change it: one item
for each piece of work, whatever its provenance, from a raw idea to its delivery (design goals 1 and 2). It writes an
item, shapes it, rates it and records what it depends on, and prints the backlog in rank order with what blocks each
item. Adding an idea starts no work. The person reads an item by its title, not by its id (design goal 10).

## Terms
- **title** (noun): the name of an item that the person reads beside its id. Kind of: text.
- **git branch** (noun): a branch of a git repository. Plural: git branches. Kind of: thing.
- **upstream branch** (noun): the branch of a remote that a git branch pushes to. Kind of: thing.
- **branch name** (noun): the name a git branch or an upstream branch is known by. Kind of: text.
- **push** (noun): one `git push` of a git branch's commits to a remote. Plural: pushes. Kind of: thing.
- **check out** (verb, state): a repository has a git branch as the one its working tree is on. Forms: checks out, checked out. Frame: repository checks out git branch.
- **reject** (verb, state): a remote declines a push made to it. Forms: rejects, rejected. Frame: remote rejects push.
- **answer** (verb, state): a remote replies to a push made to it, taking it or declining it. Forms: answers, answered. Frame: remote answers push.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| title | of | item | one |
| git branch | of | task | one |
| upstream branch | of | git branch | one |
| branch name | of | git branch | one |
| branch name | of | upstream branch | one |
| remote | of | repository | one |
| push | of | command | one |

## Behaviour

### [g5] `work depend` records a dependency
- [r5] When the person runs `work depend` on an item, `work` shall write a dependency of the item and commit the item.

### [g15] `work show` names an item by its title
- [r15] When the person runs `work show` on an item, `work` shall print the title of the item.

### [g22] `work idea` writes an item
- [r22] When the person runs `work idea`, `work` shall write an item whose status is `idea` and commit the item.

### [g23] `work shape` shapes an idea
- [r23] While an item is `idea`, when the person runs `work shape` on the item, `work` shall set the status of the item to `shaped`.

### [g24] `work shape` refuses an item that is not an idea
- [r24] While an item is not `idea`, if the person runs `work shape` on the item, then `work` shall refuse the command and name the status of the item.

### [g25] `work rate` sets an item's ratings
- [r25] When the person runs `work rate --value high-value --urgency low-urgency --size small` on an item, `work` shall set the value of the item to `high-value`, set the urgency of the item to `low-urgency`, set the size of the item to `small` and commit the item.

### [g26] `work backlog` prints an item with its dependency on an item that is not delivered
- [r26] While an item is not `delivered` and a dependency on the item exists and another item has the dependency, when the person runs `work backlog`, `work` shall print the item and the dependency.

### [g27] `work backlog --json` prints one JSON object
- [r27] When the person runs `work backlog` with the `--json` option, `work` shall print one JSON object and exit successfully.

### [g28] `work withdraw` withdraws an item that is an idea, shaped, ready or needs input
- [r28] While an item is one of `idea`, `shaped`, `ready` or `needs-input`, when the person runs `work withdraw` on the item, `work` shall set the status of the item to `withdrawn`.

### [g29] `work refuse` refuses an item that is an idea or shaped
- [r29] While an item is one of `idea` or `shaped`, when the person runs `work refuse` on the item, `work` shall set the status of the item to `refused`.

### [g30] `work answer` returns an item that needs input to shaped
- [r30] While an item is `needs-input`, when the person runs `work answer` on the item, `work` shall set the status of the item to `shaped` and commit the item.

### [g31] `work backlog` prints the question of an item that needs input
- [r31] While an item is `needs-input`, when the person runs `work backlog`, `work` shall print the item and every question on the item.

### [g32] `work idea` keeps its commit and names the remote that rejects its push
- [r32] While the remote of this repository rejects the push of the command, when the person runs `work idea`, `work` shall write an item whose status is `idea`, commit the item, print the remote and exit successfully.

### [g33] `work idea` keeps its commit and names the remote that does not answer its push
- [r33] While the remote of this repository does not answer the push of the command, when the person runs `work idea`, `work` shall write an item whose status is `idea`, commit the item, print the remote and exit successfully.

### [g34] `work idea` refuses the branch of a task
- [r34] While this repository checks out a git branch of a task, if the person runs `work idea`, then `work` shall refuse the command and name the task.

### [g35] `work idea` keeps an upstream branch of another name
- [r35] While this repository checks out a git branch that has a branch name and the upstream branch of the git branch has a different branch name, when the person runs `work idea`, `work` shall write an item whose status is `idea`, commit the item and keep the upstream branch.

### [g36] `work backlog` prints every item with its title, status, provenance and ratings
- [r36] While an item exists, when the person runs `work backlog`, `work` shall print the item, the title of the item, the status of the item, the provenance of the item, the value of the item, the urgency of the item and the size of the item.

## Implementation, may change
- Each item is the file `.shop/backlog/b<n>.md`, and each change to it is one commit of that file, whose history is
  its log. `work backlog` only reads, and commits nothing.
- An item's score is (value + urgency) / size, with low and small 1, medium 2, and high and large 3. Within a state
  items go by score from high to low, and a tie goes to the item added first (the lower `b<n>`). An item missing a
  rating has no score and ranks after the rated items of its state.
- `work backlog` prints every item, one table a state, in the order `in-batch`, `needs-input`, `ready`, `shaped`,
  `idea`, `delivered`, `refused`, `withdrawn`; a state with no items is left out.
- A row's `waiting on` column names each item it is blocked by, with that item's status, and for an item that is
  `needs-input` the first line of its question.
- An item is blocked by each item it depends on that is not `delivered`, a missing one included (printed `missing`).
  `work batch start` makes the glossary's exception: an item whose dependency it picks earlier in the same pick is
  not blocked there.
- `work depend` refuses a dependency on an item that is `refused` or `withdrawn`, which is never delivered and so
  would block for good (plan 2 rulings, Q1). `work depend <item> --drop <item>` drops a dependency the item has, one
  on an item there is not included; one it does not have is refused.
- For an item that is `in-batch`, the `waiting on` column says how far its batch is along, `in batch-1 (building): 1
  of 2 tasks done`, and `--json` gives its row a `batch` object (`name`, `status`, `tasks_done`, `tasks`); no other
  row has one.
- A command that commits pushes the branch checked out to its upstream remote (else `origin`), never prompting, and
  waits `$SHOPSYSTEM_PUSH_TIMEOUT` seconds (default 60) for the remote's answer: a push the remote rejects, or one it
  does not answer in that time, is printed `not pushed: <remote>: <reason>` and the commit is kept.

## Not yet
- Bugs' risk and likelihood ratings (design goal 2): not built, because the design gives them no part in the rank.
