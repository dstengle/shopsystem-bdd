---
id: vocabulary/example.org/fixture/request-4-time/work
area: work
---

# The words of work

## Terms

- **session** (noun) → object session. An agent that works in a terminal.
- **file** (noun) → object file. A file of a repository.
- **stage** (noun) → object stage. A step of a piece of work.
- **line** (noun) → object line. A sentence a stage is to meet.
- **worktree** (noun) → object worktree. A checkout a session works in.
- **layout** (noun) → object layout. The files a worktree is to hold, and where each is.
- **commit** (noun) → object commit. A change a request records in a repository. This: the commit the request makes.
- **deadline** (noun) → object deadline. The moment a stage is due.
- **push** (noun) → object push. The commits a request sends to a remote.
- **status** (attribute) → attribute stage.status.
- **open** (adjective) → value stage.status open.
- **done** (adjective) → value stage.status done.
- **tier** (attribute) → attribute stage.tier. What checks a stage.
- **test** (noun) → value stage.tier test.
- **review** (noun) → value stage.tier review.
- **priority** (attribute) → attribute stage.priority. How soon a stage is to be ended.
- **low** (adjective) → value stage.priority low.
- **high** (adjective) → value stage.priority high.
- **urgent** (adjective) → value stage.priority urgent.
- **version** (attribute) → attribute file.version. The release a file was written for.
- **1.0.0** (noun) → value file.version 1.0.0.
- **2.0.0** (noun) → value file.version 2.0.0.
- **2.5.0** (noun) → value file.version 2.5.0.
- **verdict** (attribute) → attribute line.verdict. What became of a line.
- **proposed** (adjective) → value line.verdict proposed.
- **accepted** (adjective) → value line.verdict accepted.
- **refused** (adjective) → value line.verdict refused.
- **withdrawn** (adjective) → value line.verdict withdrawn.
- **follow** (verb, state) → relation session.follows. Forms: follows, followed. Frame: <agent> follows <stage>.
- **cover** (verb, state) → relation file.covers. Forms: covers, covered. Frame: <file> covers <line>.
  Frame: <stage> covers <line>.
- **open** (verb, action) → operation work.open. Forms: opens, opened. Frame: <actor> opens the board.
- **write** (verb, action) → operation work.write. Forms: writes, written. Frame: <actor> writes <file>.
- **end** (verb, action) → operation work.end. Forms: ends, ended. Frame: <actor> ends <stage>.
- **give** (verb, action) → operation work.give. Forms: gives, given. Frame: <actor> gives <file> to <agent>.
- **settle** (verb, action) → operation work.settle. Forms: settles, settled. Frame: <actor> settles <line>.
- **assign** (verb, action) → operation work.assign. Forms: assigns, assigned. Frame: <actor> assigns <session>.
- **inspect** (verb, action) → operation work.inspect. Forms: inspects, inspected. Frame: <actor> inspects <worktree>.
- **the work service** (proper noun) → service work.
