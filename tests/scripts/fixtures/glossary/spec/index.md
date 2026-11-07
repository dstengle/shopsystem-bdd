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

- **the person** (proper noun): the human who asks, answers and approves. Not: user, human. Kind of: agent.
- **`work run`** (proper noun): the supervisor that runs nodes through transitions by starting sessions. Kind of: agent.
- **`work`** (proper noun): the command that writes statuses, transitions and requests. Kind of: agent.
- **a tool** (proper noun): one of `features`, `tools`, `measure`, `migrate` and `model`. Kind of: agent.
- **`features`** (proper noun): the tool that reads and generates feature files. Kind of: agent.
- **`tools`** (proper noun): the tool of the analysis tools. Kind of: agent.
- **`measure`** (proper noun): the tool that measures an initiative. Kind of: agent.
- **`migrate`** (proper noun): the tool that moves a repository between layouts and releases. Kind of: agent.
- **`model`** (proper noun): the tool that checks the spec's model. Kind of: agent.
- **the researcher** (proper noun): the role of a research stage. Kind of: agent.
- **the planner** (proper noun): the role of a plan stage. Kind of: agent.
- **the implementer** (proper noun): the role of an implement stage. Kind of: agent.
- **the reviewer** (proper noun): the role of a review stage. Kind of: agent.
- **the analyst** (proper noun): the role of an analysis stage. Kind of: agent.
- **the SessionStart hook** (proper noun): the plugin's hook run when a session starts. Kind of: agent.
- **`delivering-an-initiative`** (proper noun): the skill that starts `work run`. Kind of: agent.
- **`formulating-features`** (proper noun): the skill that formulates feature files. Kind of: agent.
- **`integrating-a-proposal`** (proper noun): the skill that integrates a note into the spec. Kind of: agent.
- **`checking-spec-consistency`** (proper noun): the skill that checks the spec's consistency. Kind of: agent.
- **`migrating-to-capabilities`** (proper noun): the skill that migrates a repository to capability files. Kind of: agent.
- **`initiative-round`** (proper noun): the agent of every round. Kind of: agent.
- **`trial-runner`** (proper noun): the agent that runs one trial. Kind of: agent.

### Kinds

- **agent** (noun): a session, a tool or the person, as the one that does what a verb says. Kind of: thing.
- **text** (noun): a file, or a part of one a tool writes whole. Kind of: thing.
- **thing** (noun): anything a requirement names.
- **bounded context** (noun): one repository's spec. Kind of: thing.
- **capability** (noun): one file under `spec/capabilities/`. Plural: capabilities. Kind of: text.
- **group** (attribute of capability): Values: service, guarantees, operations.
- **requirement** (noun): one codified statement of a capability. Not: behaviour line. Kind of: text.
- **requirement group** (noun): the requirements that together make one scenario. Kind of: thing.
- **term** (noun): one entry of the glossary. Kind of: text.
- **design-decision** (noun): one file under `spec/decisions/`. Kind of: text.
- **status** (attribute of design-decision): Values: `proposed`, `accepted`, `rejected`, `superseded`.
- **feature** (noun): the generated feature file of a capability. Kind of: text.
- **scenario** (noun): one Gherkin scenario, generated from one requirement group. Kind of: text.
- **step** (noun): one Given, When or Then line. Kind of: text.
- **request** (noun): what brings work into a bounded context. Kind of: text.
- **status** (attribute of request): Values: `open`, `awaiting-asker`, `awaiting-upstream`, `accepted`, `delivered`,
  `refused`, `withdrawn`.
- **request line** (noun): one proposed statement of a request. Kind of: text.
- **line outcome** (attribute of request line): Values: `accepted`, `rewritten`, `refused`, `question`, `withdrawn`.
- **initiative** (noun): the delivery of one request's accepted lines. Not: epic. Kind of: text.
- **status** (attribute of initiative): Values: `proposed`, `started`, `done`, `abandoned`.
  Transitions: `proposed` → `started`: `work start`; `started` → `abandoned`: `work abandon`; `started` → `done`: complete.
- **capability-proposal** (noun): the part of an initiative that proposes requirements of one capability. Kind of: text.
- **status** (attribute of capability-proposal): Values: `drafted`, `awaiting-answer`, `approved`, `formulated`,
  `withdrawn`.
- **glossary-proposal** (noun): the part of an initiative that proposes terms. Kind of: text.
- **status** (attribute of glossary-proposal): Values: `drafted`, `awaiting-answer`, `approved`, `withdrawn`.
- **work-item** (noun): the unit of delivery under a capability-proposal. Kind of: text.
- **status** (attribute of work-item): Values: `drafted`, `researched`, `planned`, `ready`, `claimed`, `done`,
  `green`, `awaiting-answer`, `failed`, `withdrawn`.
  Transitions: `drafted` → `researched`: research; `researched` → `planned`: plan; `planned` → `ready`: plan;
  `ready` → `claimed`: implement; `claimed` → `done`: implement; `done` → `green`: review.
- **question** (noun): an open point on a node. Kind of: text.
- **answer** (noun): the answer to one question. Kind of: text.
- **delegation** (noun): the person's words naming the questions a session may answer. Kind of: text.
- **delivery** (noun): one invocation of `work run`. Plural: deliveries. Kind of: agent.
- **stage** (noun): one session `work run` starts for one node. Kind of: session.
- **stage kind** (attribute of stage): Values: research, plan, implement, review, analysis.
- **round** (noun): a stage of the kinds integrate, gate, apply, formulate or intake. Kind of: stage.
- **round kind** (attribute of round): Values: integrate, gate, apply, formulate, intake.
- **worker** (noun): a stage that holds a worker slot. Kind of: stage.
- **session** (noun): one Claude Code conversation. Kind of: agent.
- **result** (noun): the result a stage writes. Kind of: text.
- **outcome** (attribute of result): Values: `DONE`, `DONE_WITH_CONCERNS`, `PARTIAL`, `BLOCKED`, `HAND-BACK`,
  `QUESTION`, `NEEDS_CONTEXT`.
- **brief** (noun): the input data of one stage. Kind of: text.
- **checkout** (noun): the repository's main working tree. Kind of: thing.
- **worktree** (noun): a working tree `work run` makes for one stage. Kind of: thing.
- **initiative branch** (noun): the branch of one initiative. Kind of: thing.
- **work-item branch** (noun): the branch of one work-item. Plural: work-item branches. Kind of: thing.
- **commit** (noun): one git commit. Kind of: thing.
- **remote** (noun): the git remote of a branch. Kind of: thing.
- **file set** (noun): the paths a work-item says its work changes. Kind of: text.
- **claim** (noun): the files a claimed work-item holds. Kind of: thing.
- **stage directory** (noun): the directory of one stage, `runs/<node>/<k>-<stage>/`. Kind of: thing.
- **initiative directory** (noun): the directory of one initiative under `.shop/work/`. Kind of: thing.
- **record** (noun): a file under `.shop/records/`. Kind of: text.
- **measurement** (noun): the record of one measured initiative. Kind of: text.
- **finding** (noun): one finding of a review. Kind of: text.
- **grade** (attribute of finding): Values: Critical, Important, Minor.
- **file** (noun): a file of the repository. Kind of: text.
- **command** (noun): one run of `work`, `work run` or a tool, with its arguments. Kind of: thing.
- **reason** (noun): why a command was refused. Kind of: text.
- **JSON object** (noun): one JSON value printed by a tool. Kind of: text.
- **resource** (noun): what a session holds while it runs. Kind of: thing.
- **transition** (noun): a change of a node's status. Kind of: text.
- **plan** (noun): the plan a planner writes. Kind of: text.
- **suite** (noun): the project's tests. Kind of: thing.
- **change list** (noun): what an integrate round ends with. Kind of: text.
- **transcript** (noun): the transcript of one session. Kind of: text.
- **interpreter** (noun): a Python interpreter. Kind of: thing.
- **violation** (noun): a row `model check` finds. Kind of: text.
- **hook** (noun): a hook of the plugin. Kind of: thing.
- **agent definition** (noun): a file under `agents/`. Kind of: agent.
- **upgrade step** (noun): the change between two plugin releases. Kind of: text.
- **trial** (noun): one run of a plugin tool on a target. Kind of: thing.

### Events

- **start** (verb): a stage or a delivery begins. Frame: agent starts thing.
- **end** (verb): a stage stops. Frame: agent ends thing.
- **write** (verb): Forms: writes, written. Frame: agent writes text.
- **commit** (verb): Forms: commits, committed. Frame: agent commits text.
- **refuse** (verb): a command is not done. Frame: agent refuses thing.
- **merge** (verb): a branch is merged into another. Frame: agent merges work-item branch.
- **rerun** (verb): Forms: reruns, rerun. Frame: agent reruns stage.
- **discard** (verb): a stage's work is dropped. Frame: agent discards stage.
- **give** (verb): Forms: gives, given. Frame: agent gives thing to thing.
- **change** (verb): a file or a status is changed. Frame: agent changes text.
- **ask** (verb): a question is asked. Frame: agent asks question.
- **raise** (verb): a request is raised into an upstream. Frame: agent raises request.
- **read** (verb): Forms: reads, read. Frame: agent reads thing.
- **show** (verb): Forms: shows, shown. Frame: agent shows text.
- **keep** (verb): Forms: keeps, kept. Frame: agent keeps text.
- **push** (verb): a commit is pushed. Frame: agent pushes commit.
- **delete** (verb): a file is removed. Frame: agent deletes text.
- **approve** (verb): the person approves a proposal. Frame: agent approves thing.
- **withdraw** (verb): Forms: withdraws, withdrawn. Frame: agent withdraws thing.
- **list** (verb): a tool lists things. Frame: agent lists thing.
- **name** (verb): a message names a thing. Frame: agent names thing.
- **append** (verb): a line is added at the end of a file. Frame: agent appends text.
- **stop** (verb): Forms: stops, stopped. Frame: agent stops thing.
- **relocate** (verb): a path is moved with git. Frame: agent relocates file.
- **generate** (verb): a file is generated. Frame: agent generates feature.
- **use** (verb): a tool uses a thing. Frame: agent uses thing.
- **pull** (verb): a work-item is pulled through its stages. Frame: agent pulls work-item.

### Resources

- **spec lock** (noun, exclusive): held by every integrate, apply and formulate round.
- **initiative lock** (noun, exclusive): held by every stage of an initiative that is not a worker.
- **worker slot** (noun, counted by `workers`): held by every worker.
- **merge lock** (noun, exclusive): held by a merge.
- **turn** (noun, exclusive): held by the side of a request whose turn it is.

### Conditions

- **open** (adjective of initiative): its status is not `done` and not `abandoned`.
- **complete** (adjective of initiative): every work-item of it is `green` or `withdrawn`.
- **settled** (adjective of request line): its line outcome is `accepted`, `refused` or `withdrawn`.
- **closed** (adjective of capability-proposal): its status is `formulated` or `withdrawn`.
- **free** (adjective of resource): no session holds it.
- **passing** (adjective of scenario): a scenario whose test passes.
