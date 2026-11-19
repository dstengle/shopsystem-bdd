# A bounded context's contract, revised: the business contract and its interface contracts

Design, 2026-11-19, for b348 (a bounded context asks another for its context) and b42 (terms negotiated between
contexts), after plugin 0.38.0 (the domain contract: `.shop/records/2026-11-19-domain-contract/design.md`). It revises
`.shop/records/2026-11-17-rest-contract/design.md` under the person's framing (quote-50 and their correction): a
business-logic contract, and separate interface contracts that each define one way of interacting with it (ports and
adapters). The person was offline; the calls made are marked **session's call** (directive-1).

## 1. What changed from the 2026-11-17 design

| 2026-11-17 | now |
|---|---|
| An HTTP pack (`client`, `endpoint`, `call`, `respond with the status`) so lines name endpoints and statuses | No HTTP word in any line. Lines say what an actor requests of a service and what the service does (the request pack of 0.38.0). A status is the HTTP adapter's rendering of an outcome. |
| The OpenAPI document holds the shapes; the model reads its schemas in as kinds and attributes | The domain model holds the shapes; the data schemas are **made from the model** (`generate_schemas.py`). OpenAPI only references them. |
| Prose of the OpenAPI document generated from the lines that name its endpoints | The OpenAPI document's `summary` says the operation in a sentence; nothing else of a line is copied into it. Whether summaries are generated from the vocabulary is open (§7). |
| A check both ways between the lines and the document | A check both ways between the **model** and each interface contract: `spec check`'s v_a1-v_a4 for cli.toml today, the same rules for OpenAPI here (`check_adapters.py`). Lines are checked against the model (v_m1-v_m8), never against an adapter. |
| "Requirements name the endpoint, as CLI lines name their command" (no manual binding) | The binding is the interface contract itself: cli.toml and the OpenAPI document each map operation ids to their surface, and both are checked against the model. There is no binding between a line and an adapter. |
| The seeding endpoint `POST /_test/seed` | The test driver's concern, not the contract's: a driver for HTTP (`driver_http`, as `driver_cli` reads cli.toml) builds the world through the store port, never through a served endpoint. Open (§7). |
| Terminology: the HTTP act is "call" so as not to clash with "request" | Resolved by the request pack: "request" is the domain's word in every area; an HTTP request is the adapter's and never appears in a line. |

What stays: a requirement states behaviour a client can observe; storage and retries are implementation; drift is
checked, not trusted; REST first, other ports later, each its own interface contract over the same model.

## 2. The contract (b348)

A **contract** is what a bounded context offers the contexts that build on it, at one version: its domain model, its
terms, its requirements, its design-decisions, its data schemas and its interface contracts. It is an object of the
specification area with a lifecycle (`published → superseded`) and three operations of a new `contracts` service:

- **publish** (by the person): keeps a contract of the specification at a version; refused at a version already
  published, or while a requirement is not in the requirement grammar. A later one supersedes the published one. It
  raises the event *contract published*.
- **fetch** (by a downstream context): returns the published contract, or the one at a version, and changes nothing;
  refused at a version never published. **This is b348's ask:** a downstream reads an upstream's context without
  raising a context request for new behaviour.
- **obtain** (by the person, on the downstream's side): keeps the contract of an upstream; keeps no context request;
  refused for a bounded context with no channel.

**Session's call:** `downstream context` is an object, a kind of agent, not an `actor` of the model: grammar 4 reads an
actor only as a proper noun ("the person"), and lines need "a downstream context fetches ...". The model's `by` list
names it as a kind of actor (`op_by`).

**Session's call:** a contract's version is a relation to the existing object `version` (`has → version (one)`),
not an attribute: an attribute typed `(version)` or `(text)` gives grammar 4 no "is `1.2.0`" without declared values
(spec_vocabulary_terms reads only number, time and text types, and text with no values takes no code). Lines say "a
contract that has the `1.2.0` version" and "publishes a contract with the `1.2.0` version". Recorded as open (§7, b365).

## 3. Term proposals (b42)

A **term proposal** is a kind of request line that proposes a term (a vocabulary entry, with the model lines that
declare its element when the upstream has none) and concerns a term. Being a request line, everything the context
requests service already says of request lines holds for it unchanged: settled with a line outcome, countered by a
rewritten one, refused with a line reason, every line settled before the request is accepted. New:

- **suggest** (by the person, the asker): keeps the term proposal in the context request and an entry on it; refused
  when it does not conform to the vocabulary-entry form, or out of the asker's turn (`awaiting-upstream`).
- On **accept**, every term an accepted term proposal concerns comes into the item the request becomes, in the
  upstream's own words (design-decision requests-only-propose: an accepted line is written in this context's terms;
  a term the upstream rewrites is a counter-proposal, `rewritten`).

The feed example of 2026-11-17 reads, in this framing (feed's words, illustrative: not parsed here, feed's vocabulary
is not this repository's): the web context's request to feed holds a term proposal
`- **short** (noun) → value video.format short.` and a request line "When a viewer lists the feed with the format
`short` excluded, the feed service shall return a feed that holds no video whose format is `short`." Feed accepts
both; "YouTube Short" is no new noun of feed.

## 4. From the model to the data schemas

`generate_schemas.py` lays b348 and b42 over a copy of `spec/`, reads the model with `domain_model.read` and writes
JSON Schema 2020-12 (`schemas/`); `--check` makes them again and compares, and validates `examples.json` (including
a negative example: a refusal reason the model does not declare). The rules:

| model | JSON Schema |
|---|---|
| object | an object with `reference` (a business reference `<kind>:<id>`), `text` when it is a kind of text or of file, its attributes and relations; `unevaluatedProperties: false` unless another object extends it |
| `kind of` another object | `allOf` of the other's schema |
| attribute of values | `enum` (a lifecycle's attribute too) |
| attribute text / number / time | string / number / date-time string |
| relation `holds` or `has` (composition) | the held things embedded, a property per target kind; a structureless kind of text as a string, `version` as `<major>.<minor>.<patch>` |
| any other relation (association) | a business reference |
| operation | a request `{operation, parameters}`; the object slot is not sent unless it is passed data (`PASSED`: suggest's term proposal); other objects by reference |
| outcome | the envelope (`envelope.schema.json`, from `domain_envelope`) with `content` the phrase's object (`every X`: an array), one case per outcome, `broken` always |
| refusal reasons | the error's `reason` an `enum` of the operation's declared reasons |
| event | a notification `{event, content}`, the content its raising operation's `done` object |

**Session's call:** the passed-or-referenced distinction is written in the generator (`PASSED`), not the model: the
model form has no way to say it. Proposed (§7, b366): a parameter written `<name> (passed)`.

What the generation shows about the model: the things a contract holds (terms, requirements, design-decisions) are
objects with no attributes in this repository's model, so the contract's content carries each as `{reference,
text}`. A downstream that needs a term's part of speech or a requirement's group as data needs the model to declare
them (§7).

## 5. The interface contracts

Each maps the same operation ids and the same business parameter names onto its port; neither says what an
operation does.

| | CLI (`cli-adapter.toml`, the form of `spec/adapters/cli.toml`) | HTTP (`http-adapter.openapi.yaml`, OpenAPI 3.1) |
|---|---|---|
| operation | `command = "spec contract publish"` | `operationId: contracts.publish` on `POST /contracts` |
| parameter | positional or option, by business name | path, query or body field, by the schema's name |
| requester | the person at the terminal | `x-actors`, each a security scheme (`x-actor`) |
| done / returned | exit 0, content on stdout (`--json`: the envelope) | 201 when something is kept, else 200; body: the envelope |
| refused | exit 1, the reason on stderr | a 4xx per reason: `x-outcome: refused`, `x-reasons` (409 a conflict with what is kept, 404 a thing not found, 422 anything else) |
| broken | exit 1 | 503, the envelope |
| event | (a hook, where there is one) | `webhooks`, `x-event` |
| checked by | `spec check` v_a1-v_a4 | `check_adapters.py`, the same rules both ways, plus every `$ref` resolving and every declared reason carried by exactly one status |

**Session's call:** the mapping lives in OpenAPI's own fields plus three `x-` extensions (`x-actors`, `x-outcome`,
`x-reasons`). The 2026-11-17 anti-goal "an `x-` field a person keeps by hand to say which requirement an operation
serves" still holds: these say which **model operation** a path is, the same thing cli.toml's tables say, and are
checked against the model.

**Session's call:** `contracts.fetch` is one operation on one path (`GET /contract`, `version` in the query) rather than
two paths, so an operation id stays one path and method.

## 6. Design-decisions this asks for (to write with `work decision` when the items are built)

- The HTTP adapter maps outcomes to statuses as §5's table says (tier: check, enforced by the adapter check).
- A downstream context's fetch reaches the upstream through a channel: the issue host today (a context request's
  issue), HTTP once a context serves its contract; both are adapters of one operation (tier: judgement).
- Data schemas are made from the domain model, never written by hand; an interface contract references them
  (tier: check).

## 7. Open

See README.md, "Still open".
