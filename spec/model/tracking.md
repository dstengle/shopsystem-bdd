---
id: model/missingmass.io/shopsystem/shopsystem-bdd/tracking
area: tracking
kind: supporting
imports: [specification]
---

# Work tracking

## Purpose

Work to do: the backlog's items and their lines, the context requests between bounded contexts, and the person's quotes and directives.

```model
object context request kind of text
  attributes: status: open | awaiting-asker | awaiting-upstream | accepted | delivered | refused | withdrawn; side: asker | upstream
  relations: has → request line | thread | turn (many); holds → entry | request line (many); addresses → bounded context (many); originates from → bounded context (many); for → context request (many)

object request line kind of text
  attributes: line outcome: accepted | rewritten | refused | withdrawn | question
  relations: has → line reason (many); counters → request line (many)

object question kind of text
  relations: on → item | context request (many)

object answer kind of text

object session kind of agent
  relations: has → workspace | transcript (many)

object item kind of file
  attributes: status: shaped | ready | in-batch | delivered | refused | withdrawn | idea | needs-input; provenance: own | peer | product; value: low-value | medium-value | high-value; urgency: low-urgency | medium-urgency | high-urgency; size: small | medium | large
  lifecycle status: idea → shaped; shaped → ready; ready → shaped; ready → in-batch; in-batch → delivered; in-batch → needs-input; in-batch → ready; needs-input → shaped; idea → refused; shaped → refused; idea → withdrawn; shaped → withdrawn; ready → withdrawn; needs-input → withdrawn
  relations: has → dependency | request line | title | shaping note | scenario | requirement | task | defect (many); holds → relation row | universal condition | upstream entry | given block | requirement | capability | term | requirement id | requirement group | chore (many); proposes → requirement (many); meets → readiness bar | bar check (many)
  relations: holds → model line (many)
  relations: holds → operation table | operation (many)
  relations: exceeds → review limit (many)
  relations: derives from → item (one)
  relations: moves → term (many)

object backlog

object quote kind of file
  relations: from → session (many)

object message

object dependency kind of text
  relations: on → item (many)

object title kind of text

object workspace name kind of text

object shaping note kind of text

object transcript kind of file

object queued message kind of message

object directive kind of file
  attributes: status: live | promoted | dropped
  lifecycle status: live → promoted; live → dropped
  relations: has → quote (many)

object relation row kind of text

object upstream entry kind of text

object given block kind of text

object readiness bar
  relations: has → bar check (many)

object bar check

object requirement id kind of text

object universal condition id kind of text

object chore kind of text
  relations: holds → file (many)

object resolution kind of text

object observation

object thread
  attributes: status: open | closed; status: open | closed
  relations: on → channel (many)

object entry kind of text
  attributes: side: asker | upstream
  relations: on → context request (many); holds → field | requirement | term | given block (many)

object requirement grammar kind of artifact

object channel
  relations: holds → thread (many)
  attributes: availability: available | rejecting
  relations: provides → thread (many)

object field kind of text
  attributes: side: asker | upstream

object line reason kind of text

object relation-row form kind of artifact

object upstream-entry form kind of artifact

object example-data form kind of artifact

object universal kind of capability

object idea
object turn
object shared store
  attributes: availability: available | rejecting | unreachable
object brainstorming session kind of session

service backlog
  operation note idea(title, note)  outcomes: done → the item
  operation shape(item, note)  outcomes: done | refused: item not an idea, no note
  operation rate(item, value, urgency, size)  outcomes: done
  operation link(item, prerequisite)  outcomes: done
  operation ready(item)
    outcomes: done → the item | refused: item not shaped, bar check unmet, term violating a rule, requirement with no translation, universal condition with no translation, requirement group violating a rule, request line not settled
  operation decline(item)  outcomes: done
  operation withdraw(item, reason)  outcomes: done
  operation answer(item, answer)  outcomes: done
  operation show(item)  outcomes: returned → the item
  operation list()  outcomes: returned → every item
  operation reopen(item)  outcomes: done | refused: item not ready
  operation annotate(item, note)  outcomes: done | refused: item closed
  operation merge(item, successor, reason)  outcomes: done | refused: item closed, successor closed, successor that is the item
  operation retitle(item, title)  outcomes: done | refused: item not open
  operation split(item, requirement)  outcomes: done → the item | refused: item not an idea or shaped, requirement not in the item
  operation allocate(item)  outcomes: done | refused: item not ready
  operation deliver(item)  outcomes: done | refused: item not in-batch
  operation restore(item)  outcomes: done | refused: item not in-batch
  operation suspend(item, question)  outcomes: done | refused: item not in-batch

service drafting
  operation draft(item, relation row, universal condition, universal condition id, upstream entry, given block, requirement id, requirement, capability)
    outcomes: done → the item | refused: relation row not in form, upstream entry not in form, given block not example data, requirement id of no requirement, universal condition id of no condition, chore in the item, capability that exists
  operation recodify(capability, item)  outcomes: done
  operation reword(requirement)  outcomes: done | refused: requirement of a capability
  operation remove(requirement)  outcomes: done | refused: requirement of a capability
  operation assign(chore, item)  outcomes: done | refused: requirement in the item
  operation write(term, item)  outcomes: done
  operation declare(model line, item)  outcomes: done
  operation apply(retirement list, item)  outcomes: done | refused: requirement id of no requirement
  operation expose(operation table, item)  outcomes: done | refused: operation table of no operation
  operation withhold(operation, item)  outcomes: done
  operation retract(capability, item)  outcomes: done
  operation remove model line(model line, item)  outcomes: done | refused: model line not in the item
  operation reword model line(model line, item)  outcomes: done | refused: model line not in the item
  operation remove term(term, item)  outcomes: done | refused: term not in the item
  operation reword term(term, item)  outcomes: done | refused: term not in the item
  operation write into pack(term, pack, item)  outcomes: done | refused: term in the pack
  operation take out(item, universal condition, upstream entry, given block)  outcomes: done | refused: universal condition not in the item, upstream entry not in the item, given block not in the item
  operation replace(item, universal condition, upstream entry, given block)  outcomes: done | refused: universal condition not in the item, upstream entry not in the item, given block not in the item
  operation move(model line, item)  outcomes: done | refused: model line not in the domain model
  operation move term(term, item)  outcomes: done | refused: term not in the vocabulary

service context requests
  operation raise(context request, origin, thread, text, bounded context)
    outcomes: done → the context request | refused: thread missing, origin beside a thread, text that does not identify this bounded context, bounded context with no channel, repository rejecting
  operation ask(question)  outcomes: done
  operation reply(context request, answer)  outcomes: done | refused: context request asked of this bounded context
  operation offer(context request, capability)  outcomes: done
  operation serve(context request)  outcomes: done | refused: repository rejecting
  operation propose(context request)  outcomes: done
  operation settle(request line, line outcome: accepted | rewritten | refused | withdrawn | question, line reason)
    outcomes: done | refused: context request not this side's turn, request line that does not parse, line reason missing
  operation pass turn(turn)  outcomes: done | refused: context request not this side's turn, repository rejecting
  operation accept(context request)  outcomes: done → the item | refused: request line not settled
  operation resolve(context request)  outcomes: done | refused: context request not accepted
  operation catch up()  outcomes: done
  operation watch(bounded context)  outcomes: notifies → each entry not held
  operation survey(bounded context)  outcomes: returned → every context request
  operation inspect(context request)  outcomes: returned → the context request
  operation suggest(context request, term proposal) by the person
    outcomes: done → the term proposal | refused: term proposal not in the vocabulary-entry form, context request not this side's turn

service conversation
  operation quote(message)  outcomes: done → the quote
  operation prompt(session)  outcomes: done
  operation give(directive)  outcomes: done → the directive
  operation promote(directive, item)  outcomes: done | refused: directive not live, item that does not exist
  operation drop(directive, reason)  outcomes: done | refused: directive not live
  operation read(quote)  outcomes: returned → the quote

actor the person kind of agent

object model line kind of text
  relations: restates → element (one)
  relations: specifies → operation (one)
  relations: holds → member line (many)
  relations: moves to → area (one); leaves → area (one)

object retirement list kind of file
  relations: holds → requirement id | requirement (many)

object domain model kind of file
  relations: holds → model line | operation (many)
  relations: holds → element (many)
  relations: holds → member line (many)

object operation-table form kind of artifact

object successor kind of item

object review limit

object term proposal kind of request line
  relations: concerns → term (many)

object vocabulary-entry form kind of artifact
```
