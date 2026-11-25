---
id: product/missingmass.io/shopsystem/jobs
form: jobs to be done
---

# Jobs to be done

Each job is a structured entry, not a requirement line: an id, its actor (one of `index.md`'s actors) and its
statement in the form "When <situation>, <actor> wants <motivation>, so they can <outcome>." Which context a job is
assigned to is the domain map's (`domain.md`), not the job's.

## [j1] Shape work into checkable lines
- actor: the person
- statement: When an intention for a bounded context is settled in conversation, the person wants it written as
  requirement lines that read to one meaning and pass the readiness bar, so they can hand it to a build without
  explaining it again.

## [j2] Build and review ready work as one change
- actor: the person
- statement: When items are ready, the person wants them built together, each in its own workspace, and reviewed once
  as one change, so they can merge behaviour whose scenarios pass and whose review findings are settled.

## [j3] Exchange requests between contexts
- actor: the person
- statement: When a bounded context needs behaviour another context owns, the person wants to ask that context in its
  own terms and settle the lines turn by turn, so they can rely on the behaviour once it is delivered.

## [j4] Publish and obtain contracts
- actor: the person
- statement: When a bounded context's behaviour is relied on by others, the person wants its contract kept at a
  version and obtained by each downstream context, so they can change the context without breaking what others rely
  on unknowingly.

## [j5] Upgrade a repository to a new release
- actor: the person
- statement: When a new release of the product is out, the person wants each hosted context's files moved to it step
  by step, so they can use the release without rewriting their specification by hand.

## [j6] Measure a batch
- actor: the person
- statement: When a batch is merged, the person wants what it cost and what escaped it measured and compared with
  earlier batches, so they can change the workflow on evidence.
