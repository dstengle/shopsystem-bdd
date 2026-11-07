---
id: bounded-context/example.org/fixture/glossary
title: The typed glossary fixture
language: codified-1
---

# The typed glossary fixture

A glossary from the domain model's §1–§8 (`.shop/records/2026-11-02-domain-model/domain-model.md`), typed by
category, for the tests of the lexicon and the requirement grammar. It is not this repository's spec.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| work-item | under | capability-proposal |  |
| capability-proposal | part of | initiative |  |
| glossary-proposal | part of | initiative |  |
| work-item | of | initiative |  |
| stage | of | work-item |  |
| initiative directory | of | initiative |  |
| file | of | initiative |  |
| transcript | of | session |  |
| initiative | fulfils | request |  |
| capability-proposal | argues | capability |  |
| work-item | accepts | requirement |  |
| work-item | blocked by | work-item |  |
| round | for | capability-proposal |  |
| stage | for | initiative |  |
| question | on | work-item |  |
| question | on | request line |  |
| requirement | in | capability |  |
| request line | in | request |  |
| file | in | worktree |  |
| scenario | in | feature |  |
| stage | with | result |  |
| stage | needs | resource |  |
| file | outside | worktree |  |
| initiative | outside | delivery |  |
| capability-proposal | adds | requirement |  |
| measurement | under | initiative |  |

## Glossary

### Actors

- **the person** (actor): the human who asks, answers and approves. Not: user, human.
- **`work run`** (actor): the supervisor that runs nodes through transitions by starting sessions.
- **`work`** (actor): the command that writes statuses, transitions and requests.
- **a tool** (actor): one of `features`, `tools`, `measure`, `migrate` and `model`.
- **`features`** (actor): the tool that reads and generates feature files.
- **`tools`** (actor): the tool of the analysis tools.
- **`measure`** (actor): the tool that measures an initiative.
- **`migrate`** (actor): the tool that moves a repository between layouts and releases.
- **`model`** (actor): the tool that checks the spec's model.
- **the researcher** (actor): the role of a research stage.
- **the planner** (actor): the role of a plan stage.
- **the implementer** (actor): the role of an implement stage.
- **the reviewer** (actor): the role of a review stage.
- **the analyst** (actor): the role of an analysis stage.
- **the SessionStart hook** (actor): the plugin's hook run when a session starts.
- **`delivering-an-initiative`** (actor): the skill that starts `work run`.
- **`formulating-features`** (actor): the skill that formulates feature files.
- **`integrating-a-proposal`** (actor): the skill that integrates a note into the spec.
- **`checking-spec-consistency`** (actor): the skill that checks the spec's consistency.
- **`migrating-to-capabilities`** (actor): the skill that migrates a repository to capability files.
- **`initiative-round`** (actor): the agent of every round.
- **`trial-runner`** (actor): the agent that runs one trial.

### Kinds

- **bounded context** (kind): one repository's spec.
- **capability** (kind): one file under `spec/capabilities/`. Plural: capabilities.
- **group** (attribute of capability): Values: service, guarantees, operations.
- **requirement** (kind): one codified statement of a capability. Not: behaviour line.
- **requirement group** (kind): the requirements that together make one scenario.
- **term** (kind): one entry of the glossary.
- **design-decision** (kind): one file under `spec/decisions/`.
- **status** (attribute of design-decision): Values: `proposed`, `accepted`, `rejected`, `superseded`.
- **feature** (kind): the generated feature file of a capability.
- **scenario** (kind): one Gherkin scenario, generated from one requirement group.
- **step** (kind): one Given, When or Then line.
- **request** (kind): what brings work into a bounded context.
- **status** (attribute of request): Values: `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`,
  `refused`, `withdrawn`.
- **request line** (kind): one proposed statement of a request.
- **line outcome** (attribute of request line): Values: `accepted`, `rewritten`, `refused`, `question`, `withdrawn`.
- **initiative** (kind): the delivery of one request's accepted lines. Not: epic.
- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `abandoned`: `work abandon`; `started` → `done`: complete.
- **capability-proposal** (kind): the part of an initiative that proposes requirements of one capability.
- **status** (attribute of capability-proposal): Values: `drafted`, `awaiting-answer`, `approved`, `formulated`,
  `withdrawn`.
- **glossary-proposal** (kind): the part of an initiative that proposes terms.
- **status** (attribute of glossary-proposal): Values: `drafted`, `awaiting-answer`, `approved`, `withdrawn`.
- **work-item** (kind): the unit of delivery under a capability-proposal.
- **status** (attribute of work-item): Values: `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`,
  `green`, `awaiting-answer`, `failed`, `withdrawn`.
  Transitions: `drafted` → `researched`: research; `researched` → `planned`: plan; `planned` → `ready`: plan;
  `ready` → `claimed`: implement; `claimed` → `done`: implement; `done` → `green`: review.
- **question** (kind): an open point on a node.
- **answer** (kind): the answer to one question.
- **delegation** (kind): the person's words naming the questions a session may answer.
- **delivery** (kind): one invocation of `work run`. Plural: deliveries.
- **stage** (kind): one session `work run` starts for one node.
- **stage kind** (attribute of stage): Values: research, plan, implement, review, analysis.
- **round** (kind): a stage of the kinds integrate, gate, apply, formulate or intake.
- **round kind** (attribute of round): Values: integrate, gate, apply, formulate, intake.
- **worker** (kind): a stage that holds a worker slot.
- **session** (kind): one Claude Code conversation.
- **result** (kind): the result a stage writes.
- **outcome** (attribute of result): Values: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`,
  `QUESTION`, `NEEDS_CONTEXT`.
- **brief** (kind): the input data of one stage.
- **checkout** (kind): the repository's main working tree.
- **worktree** (kind): a working tree `work run` makes for one stage.
- **initiative branch** (kind): the branch of one initiative.
- **work-item branch** (kind): the branch of one work-item. Plural: work-item branches.
- **commit** (kind): one git commit.
- **remote** (kind): the git remote of a branch.
- **file set** (kind): the paths a work-item says its work changes.
- **claim** (kind): the files a claimed work-item holds.
- **stage directory** (kind): the directory of one stage, `runs/<node>/<k>-<stage>/`.
- **initiative directory** (kind): the directory of one initiative under `.shop/work/`.
- **record** (kind): a file under `.shop/records/`.
- **measurement** (kind): the record of one measured initiative.
- **finding** (kind): one finding of a review.
- **grade** (attribute of finding): Values: Critical, Important, Minor.
- **file** (kind): a file of the repository.
- **command** (kind): one run of `work`, `work run` or a tool, with its arguments.
- **reason** (kind): why a command was refused.
- **JSON object** (kind): one JSON value printed by a tool.
- **resource** (kind): what a session holds while it runs.
- **transition** (kind): a change of a node's status.
- **plan** (kind): the plan a planner writes.
- **suite** (kind): the project's tests.
- **change list** (kind): what an integrate round ends with.
- **transcript** (kind): the transcript of one session.
- **interpreter** (kind): a Python interpreter.
- **violation** (kind): a row `model check` finds.
- **hook** (kind): a hook of the plugin.
- **agent definition** (kind): a file under `agents/`.
- **upgrade step** (kind): the change between two plugin releases.
- **trial** (kind): one run of a plugin tool on a target.

### Events

- **start** (event): a stage or a delivery begins. Frame: `work run` starts stage.
- **end** (event): a stage stops. Frame: session ends stage.
- **write** (event): Forms: writes, written. Frame: `work` writes file.
- **commit** (event): Forms: commits, committed. Frame: `work` commits file.
- **refuse** (event): a command is not done. Frame: a tool refuses command.
- **merge** (event): a branch is merged into another. Frame: `work run` merges work-item branch.
- **rerun** (event): Forms: reruns, rerun. Frame: `work run` reruns stage.
- **discard** (event): a stage's work is dropped. Frame: `work run` discards stage.
- **give** (event): Forms: gives, given. Frame: `work run` gives brief to stage.
- **change** (event): a file or a status is changed. Frame: `work` changes file.
- **ask** (event): a question is asked. Frame: `work run` asks question.
- **raise** (event): a request is raised into an upstream. Frame: the person raises request.
- **read** (event): Forms: reads, read. Frame: the reviewer reads file.
- **show** (event): Forms: shows, shown. Frame: `delivering-an-initiative` shows reason.
- **keep** (event): Forms: keeps, kept. Frame: `work` keeps file.
- **push** (event): a commit is pushed. Frame: `work` pushes commit.
- **delete** (event): a file is removed. Frame: `work` deletes file.
- **approve** (event): the person approves a proposal. Frame: the person approves capability-proposal.
- **withdraw** (event): Forms: withdraws, withdrawn. Frame: the person withdraws capability-proposal.
- **list** (event): a tool lists things. Frame: `work` lists work-item.
- **name** (event): a message names a thing. Frame: `work` names file.
- **append** (event): a line is added at the end of a file. Frame: `work` appends file.
- **stop** (event): Forms: stops, stopped. Frame: `work run` stops stage.
- **relocate** (event): a path is moved with git. Frame: `migrate` relocates file.
- **generate** (event): a file is generated. Frame: `features` generates feature.
- **use** (event): a tool uses a thing. Frame: `work run` uses interpreter.
- **pull** (event): a work-item is pulled through its stages. Frame: `work run` pulls work-item.

### Resources

- **spec lock** (resource, exclusive): held by every integrate, apply and formulate round.
- **initiative lock** (resource, exclusive): held by every stage of an initiative that is not a worker.
- **worker slot** (resource, counted by `workers`): held by every worker.
- **merge lock** (resource, exclusive): held by a merge.
- **turn** (resource, exclusive): held by the side of a request whose turn it is.

### Conditions

- **open** (condition of initiative): its status is not `done` and not `abandoned`.
- **complete** (condition of initiative): every work-item of it is `green` or `withdrawn`.
- **settled** (condition of request line): its line outcome is `accepted`, `refused` or `withdrawn`.
- **closed** (condition of capability-proposal): its status is `formulated` or `withdrawn`.
- **free** (condition of resource): no session holds it.
- **passing** (condition of scenario): a scenario whose test passes.
