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
  operation withdraw(item)  outcomes: done
  operation answer(item, answer)  outcomes: done
  operation show(item)  outcomes: returned → the item
  operation list()  outcomes: returned → every item
  operation reopen(item)  outcomes: done | refused: item not ready

service drafting
  operation draft(item, relation row, universal condition, universal condition id, upstream entry, given block, requirement id, requirement, capability)
    outcomes: done → the item | refused: relation row not in form, upstream entry not in form, given block not example data, requirement id of no requirement, universal condition id of no condition, chore in the item, capability that exists
  operation recodify(capability, item)  outcomes: done
  operation reword(requirement)  outcomes: done | refused: requirement of a capability
  operation remove(requirement)  outcomes: done | refused: requirement of a capability
  operation assign(chore, item)  outcomes: done | refused: requirement in the item
  operation write(term, item)  outcomes: done
  operation declare(model line, item)  outcomes: done

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

service conversation
  operation quote(message)  outcomes: done → the quote
  operation prompt(session)  outcomes: done
  operation give(directive)  outcomes: done → the directive
  operation promote(directive, item)  outcomes: done | refused: directive not live, item that does not exist
  operation drop(directive, reason)  outcomes: done | refused: directive not live
  operation read(quote)  outcomes: returned → the quote

actor the person kind of agent

object model line kind of text
```
