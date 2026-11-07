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

- **the person** (actor): the human who asks, answers and approves. Not: user, human. Kind of: agent.
- **`work run`** (actor): the supervisor that runs nodes through transitions by starting sessions. Kind of: agent.
- **`work`** (actor): the command that writes statuses, transitions and requests. Kind of: agent.
- **a tool** (actor): one of `features`, `tools`, `measure`, `migrate` and `model`. Kind of: agent.
- **`features`** (actor): the tool that reads and generates feature files. Kind of: agent.
- **`tools`** (actor): the tool of the analysis tools. Kind of: agent.
- **`measure`** (actor): the tool that measures an initiative. Kind of: agent.
- **`migrate`** (actor): the tool that moves a repository between layouts and releases. Kind of: agent.
- **`model`** (actor): the tool that checks the spec's model. Kind of: agent.
- **the researcher** (actor): the role of a research stage. Kind of: agent.
- **the planner** (actor): the role of a plan stage. Kind of: agent.
- **the implementer** (actor): the role of an implement stage. Kind of: agent.
- **the reviewer** (actor): the role of a review stage. Kind of: agent.
- **the analyst** (actor): the role of an analysis stage. Kind of: agent.
- **the SessionStart hook** (actor): the plugin's hook run when a session starts. Kind of: agent.
- **`delivering-an-initiative`** (actor): the skill that starts `work run`. Kind of: agent.
- **`formulating-features`** (actor): the skill that formulates feature files. Kind of: agent.
- **`integrating-a-proposal`** (actor): the skill that integrates a note into the spec. Kind of: agent.
- **`checking-spec-consistency`** (actor): the skill that checks the spec's consistency. Kind of: agent.
- **`migrating-to-capabilities`** (actor): the skill that migrates a repository to capability files. Kind of: agent.
- **`initiative-round`** (actor): the agent of every round. Kind of: agent.
- **`trial-runner`** (actor): the agent that runs one trial. Kind of: agent.

### Kinds

- **agent** (kind): a session, a tool or the person, as the one that does what a verb says. Kind of: thing.
- **text** (kind): a file, or a part of one a tool writes whole. Kind of: thing.
- **thing** (kind): anything a requirement names.
- **bounded context** (kind): one repository's spec. Kind of: thing.
- **capability** (kind): one file under `spec/capabilities/`. Plural: capabilities. Kind of: text.
- **group** (attribute of capability): Values: service, guarantees, operations.
- **requirement** (kind): one codified statement of a capability. Not: behaviour line. Kind of: text.
- **requirement group** (kind): the requirements that together make one scenario. Kind of: thing.
- **term** (kind): one entry of the glossary. Kind of: text.
- **design-decision** (kind): one file under `spec/decisions/`. Kind of: text.
- **status** (attribute of design-decision): Values: `proposed`, `accepted`, `rejected`, `superseded`.
- **feature** (kind): the generated feature file of a capability. Kind of: text.
- **scenario** (kind): one Gherkin scenario, generated from one requirement group. Kind of: text.
- **step** (kind): one Given, When or Then line. Kind of: text.
- **request** (kind): what brings work into a bounded context. Kind of: text.
- **status** (attribute of request): Values: `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`,
  `refused`, `withdrawn`.
- **request line** (kind): one proposed statement of a request. Kind of: text.
- **line outcome** (attribute of request line): Values: `accepted`, `rewritten`, `refused`, `question`, `withdrawn`.
- **initiative** (kind): the delivery of one request's accepted lines. Not: epic. Kind of: text.
- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `abandoned`: `work abandon`; `started` → `done`: complete.
- **capability-proposal** (kind): the part of an initiative that proposes requirements of one capability. Kind of: text.
- **status** (attribute of capability-proposal): Values: `drafted`, `awaiting-answer`, `approved`, `formulated`,
  `withdrawn`.
- **glossary-proposal** (kind): the part of an initiative that proposes terms. Kind of: text.
- **status** (attribute of glossary-proposal): Values: `drafted`, `awaiting-answer`, `approved`, `withdrawn`.
- **work-item** (kind): the unit of delivery under a capability-proposal. Kind of: text.
- **status** (attribute of work-item): Values: `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`,
  `green`, `awaiting-answer`, `failed`, `withdrawn`.
  Transitions: `drafted` → `researched`: research; `researched` → `planned`: plan; `planned` → `ready`: plan;
  `ready` → `claimed`: implement; `claimed` → `done`: implement; `done` → `green`: review.
- **question** (kind): an open point on a node. Kind of: text.
- **answer** (kind): the answer to one question. Kind of: text.
- **delegation** (kind): the person's words naming the questions a session may answer. Kind of: text.
- **delivery** (kind): one invocation of `work run`. Plural: deliveries. Kind of: agent.
- **stage** (kind): one session `work run` starts for one node. Kind of: session.
- **stage kind** (attribute of stage): Values: research, plan, implement, review, analysis.
- **round** (kind): a stage of the kinds integrate, gate, apply, formulate or intake. Kind of: stage.
- **round kind** (attribute of round): Values: integrate, gate, apply, formulate, intake.
- **worker** (kind): a stage that holds a worker slot. Kind of: stage.
- **session** (kind): one Claude Code conversation. Kind of: agent.
- **result** (kind): the result a stage writes. Kind of: text.
- **outcome** (attribute of result): Values: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`,
  `QUESTION`, `NEEDS_CONTEXT`.
- **brief** (kind): the input data of one stage. Kind of: text.
- **checkout** (kind): the repository's main working tree. Kind of: thing.
- **worktree** (kind): a working tree `work run` makes for one stage. Kind of: thing.
- **initiative branch** (kind): the branch of one initiative. Kind of: thing.
- **work-item branch** (kind): the branch of one work-item. Plural: work-item branches. Kind of: thing.
- **commit** (kind): one git commit. Kind of: thing.
- **remote** (kind): the git remote of a branch. Kind of: thing.
- **file set** (kind): the paths a work-item says its work changes. Kind of: text.
- **claim** (kind): the files a claimed work-item holds. Kind of: thing.
- **stage directory** (kind): the directory of one stage, `runs/<node>/<k>-<stage>/`. Kind of: thing.
- **initiative directory** (kind): the directory of one initiative under `.shop/work/`. Kind of: thing.
- **record** (kind): a file under `.shop/records/`. Kind of: text.
- **measurement** (kind): the record of one measured initiative. Kind of: text.
- **finding** (kind): one finding of a review. Kind of: text.
- **grade** (attribute of finding): Values: Critical, Important, Minor.
- **file** (kind): a file of the repository. Kind of: text.
- **command** (kind): one run of `work`, `work run` or a tool, with its arguments. Kind of: thing.
- **reason** (kind): why a command was refused. Kind of: text.
- **JSON object** (kind): one JSON value printed by a tool. Kind of: text.
- **resource** (kind): what a session holds while it runs. Kind of: thing.
- **transition** (kind): a change of a node's status. Kind of: text.
- **plan** (kind): the plan a planner writes. Kind of: text.
- **suite** (kind): the project's tests. Kind of: thing.
- **change list** (kind): what an integrate round ends with. Kind of: text.
- **transcript** (kind): the transcript of one session. Kind of: text.
- **interpreter** (kind): a Python interpreter. Kind of: thing.
- **violation** (kind): a row `model check` finds. Kind of: text.
- **hook** (kind): a hook of the plugin. Kind of: thing.
- **agent definition** (kind): a file under `agents/`. Kind of: agent.
- **upgrade step** (kind): the change between two plugin releases. Kind of: text.
- **trial** (kind): one run of a plugin tool on a target. Kind of: thing.

### Events

- **start** (event): a stage or a delivery begins. Frame: agent starts thing.
- **end** (event): a stage stops. Frame: agent ends thing.
- **write** (event): Forms: writes, written. Frame: agent writes text.
- **commit** (event): Forms: commits, committed. Frame: agent commits text.
- **refuse** (event): a command is not done. Frame: agent refuses thing.
- **merge** (event): a branch is merged into another. Frame: agent merges work-item branch.
- **rerun** (event): Forms: reruns, rerun. Frame: agent reruns stage.
- **discard** (event): a stage's work is dropped. Frame: agent discards stage.
- **give** (event): Forms: gives, given. Frame: agent gives thing to thing.
- **change** (event): a file or a status is changed. Frame: agent changes text.
- **ask** (event): a question is asked. Frame: agent asks question.
- **raise** (event): a request is raised into an upstream. Frame: agent raises request.
- **read** (event): Forms: reads, read. Frame: agent reads thing.
- **show** (event): Forms: shows, shown. Frame: agent shows text.
- **keep** (event): Forms: keeps, kept. Frame: agent keeps text.
- **push** (event): a commit is pushed. Frame: agent pushes commit.
- **delete** (event): a file is removed. Frame: agent deletes text.
- **approve** (event): the person approves a proposal. Frame: agent approves thing.
- **withdraw** (event): Forms: withdraws, withdrawn. Frame: agent withdraws thing.
- **list** (event): a tool lists things. Frame: agent lists thing.
- **name** (event): a message names a thing. Frame: agent names thing.
- **append** (event): a line is added at the end of a file. Frame: agent appends text.
- **stop** (event): Forms: stops, stopped. Frame: agent stops thing.
- **relocate** (event): a path is moved with git. Frame: agent relocates file.
- **generate** (event): a file is generated. Frame: agent generates feature.
- **use** (event): a tool uses a thing. Frame: agent uses thing.
- **pull** (event): a work-item is pulled through its stages. Frame: agent pulls work-item.

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
