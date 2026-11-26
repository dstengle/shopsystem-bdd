# request

The domain-request pack (the domain contract design, §4.3): the words of a request an actor makes of a service by one
of its operations, and of the response the service gives. A bounded context with a domain model (`spec/model/`)
imports it with `imports: [request]` in the frontmatter of `spec/index.md`, in place of the retired CLI pack; a word of
its own spelled the same is marked `Redefines: request.` An operation and its parameters are the context's own (its
model's services, named by its vocabulary): "When the person enters a design-decision with the tier `check`, ...",
"If the person enters a design-decision without a tier, then the decisions service shall refuse the request and name
the tier." Each word of this pack is the request machinery's, not a model element's.

## Glossary

- **request** (noun): what an actor asks of a service by an operation. This: the request the trigger makes.
- **parameter** (noun): a named input of a request.
- **service** (noun): what answers a request. Kind of: agent.
- **reason** (noun): why a service refuses a request.
- **response** (noun): what a service gives back to a request.
- **check** (noun): the request of an operation whose outcomes are passed or failed. This: the check the trigger makes.
- **artifact** (noun): what a thing is written to follow: a form, a schema, a layout or a reference.
- **outcome** (attribute of response): how a service ended a request. Values (adjective): `done`, `returned`, `refused`, `passed`, `failed`.
- **refuse** (verb, action): a service declines a request. Frame: service refuses request.
- **name** (verb, action): an agent says which thing it means, as in "refuse the request and name the tier". Frame: agent names thing.
- **return** (verb, action): a service gives a thing as the content of its response. Frame: service returns thing.
- **notify** (verb, action): a service tells an actor of a thing, unasked. Forms: notifies, notified. Frame: service notifies agent of thing.
- **complete** (verb, action): a service ends a request with the outcome `done` or `returned`. Frame: service completes request.
- **fail** (verb, action): a service ends a check, or a request it could not carry out, with the outcome `failed`. Frame: service fails check. Frame: service fails request.
- **keep** (verb, action): a service records a thing durably in the store. Forms: keeps, kept. Frame: service keeps thing.
- **change** (verb, action): an agent makes a thing other than it was, or with "nothing" leaves every thing as it was. Frame: agent changes thing.
- **conform** (verb, state): a thing meets what an artifact sets out. Frame: thing conforms to artifact.
- **start** (verb, action): an actor's session begins. Frame: agent starts.
