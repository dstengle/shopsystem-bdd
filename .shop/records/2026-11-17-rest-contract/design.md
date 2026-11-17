# A bounded context's REST contract: the HTTP pack, the OpenAPI document and its check, schemas in the model

Design, 2026-11-17. The person's words: quote-49 and the brainstorming of 2026-11-17 in session 0164vZm2TjT9HL3zaqsfvuQk.
Items: b348 (a context asks another for its context), b42 (terms negotiated between contexts), b241 (the artifact
registry, parked 2026-11-16 by quote-41, taken up again here), b13.

## Intent

A bounded context that needs something outside its own scope must find out what its upstream already does before it
proposes anything, and must be able to build its code against the upstream's running server. In the person's first
product, the web context needed "the feed without YouTube Shorts"; the feed context had no term for a YouTube Short, and
the two contexts only got along because they were built together and shared knowledge no file held. No server of a
product has been built successfully yet: nothing tells a context how its code calls another's.

The contract of a context is what a downstream needs for both: its behaviour in requirement lines, the words of those
lines with their meanings, and the concrete interface its code is called through. This design settles what a contract
says, for REST first. How a contract travels between contexts (published and pulled, asked over issues, collected by the
product), terms and schema changes proposed in a request, and the domain map with the product are later designs, in
that order; this one leaves room for them.

## Principles the person set

- **A requirement states behaviour a client can observe.** What a client cannot observe (error handling inside the
  context, storage, retries) is an implementation detail, tested by unit tests (which may be structured into nested
  groups to navigate), never by requirement lines or scenarios. Moving the feed from files to a database changes no line
  and no scenario. So the whole spec of a context is its public contract; no line or capability is marked public or
  internal.
- **No manual binding.** A requirement is never tied to an endpoint by a table kept beside it: the line names the
  endpoint, as CLI lines name their command today.
- **Drift is checked, not trusted.** Whatever is written in two places is checked against each other by a tool, or
  generated from one of them.
- **Schemas and fields belong to the model, not the glossary.** (b241's direction, agreed 2026-11-10.) A schema's
  properties are read in as the words of the lines, not copied by hand into term entries.
- **Statements without scenarios are allowed** where a test of another kind checks them (an endpoint exists); grammar 4's
  "may", "always" and "never" already produce no scenario.
- **REST first.** gRPC, a message bus and others come later, each its own pack over the same shape.

## Goals

1. A context's lines can say what its HTTP API does: "When a client requests `GET /feed` with the `exclude` parameter set
   to `shorts`, `feed` shall return a feed that holds no YouTube Short." (the HTTP pack).
2. A context keeps one OpenAPI document of its API, whose shapes (schemas, parameters, responses) are written by hand and
   whose prose (each operation's `summary` and `description`) is generated from the lines that name it.
3. The data words of the lines (kinds, attributes, values, relations) are read from the OpenAPI document's schemas.
4. A check finds every difference between the lines and the document, in both directions.
5. A generated scenario of a line runs against the context's server over HTTP.

## Non-goals

- How a contract is published, fetched, pinned or compared with a later version (the next design: b348).
- Proposing a term, a schema change or a capability to another context (b42, after that). This design only keeps it
  possible: a proposal will carry an OpenAPI fragment beside its lines and terms.
- The domain map and asking the product which context owns something.
- gRPC, message buses, a CLI contract of a server context.
- Headers other than the caller's identity, cookies, content negotiation, pagination conventions.
- Generating schemas, parameters or responses from lines, or lines from the document.
- A check that flags lines about internals (a rough warning on storage words was mentioned and left out).
- How a context's unit tests are structured.

## Anti-goals

- A binding table, annotation or `x-` field that a person keeps by hand to say which requirement an operation serves.
- An attribute or a value written both as a term entry and in a schema.
- Prose in the OpenAPI document that can say something its lines do not.
- A requirement whose only purpose is to describe an implementation detail so that it gets a scenario.

## Approaches considered

- **A. The document by hand, operations citing requirement ids.** Checked traceability; but the citation is a binding
  kept by hand, which the person called prone to issues.
- **B. The document generated from the lines.** One source, no drift; but the lines would have to carry every signature
  (paths, fields, types), which grammar 4 cannot and which makes lines about shapes, not behaviour.
- **C. (Chosen.) Lines name the interface; the document holds the shapes; a check ties them.** Each line names the
  endpoint, parameters, values and status codes it concerns, as codes, through the HTTP pack; the document's schemas
  give the lines their data words; the document's prose is generated from the lines; a check compares the two both ways.
  No binding is kept by hand (the line is the binding), shapes stay in the format built for them, and drift is found by
  the check. The person chose it over A for the binding and kept B's generation for the prose.

## The design

### 1. The HTTP pack (`grammar/packs/http.md`)

A pack like `cli`, imported with `imports: [http]` (a server context may import both). Its words, to be settled when the
pack is written (see "Terminology" below for the clash):

- **client** (noun): a program that calls the context over HTTP. Kind of: agent.
- **endpoint** (noun): a method and a path, written as a code (`GET /feed`). An endpoint is a constant, never example data.
- **parameter** (noun): a named input of an endpoint, a code (`exclude`); "with the `exclude` parameter set to `shorts`"
  as the CLI pack's "the `--every` option set to `5`" (spec_lf_option is the model).
- **status** (noun): a response's HTTP status, a code of three digits (`401`).
- **call** (verb, action): a client calls an endpoint (the trigger), with and without parameters, on a thing (a path
  parameter), with a body (a thing of the operation's request-body schema), as a caller or with no caller;
- **caller** (noun): the identity a call carries, as the operation's OpenAPI `security` declares it ("with no viewer"
  reads as a call with no caller of kind viewer; the builder settles the phrase);
- **return** (verb, action): the context answers a call with a thing in the response body.
- **respond** (verb, action): the context answers a call with a status ("respond with the status `401`").
- **conform** as in the CLI pack: a response body conforms to a schema (an artifact).
- a definition like the CLI pack's refuse: a response with a 4xx status is a refusal, so model logic and model explain
  can relate "refuse" lines to status lines.

The context's own name (`feed`) is the agent that returns and responds, as `work` is in this plugin's lines.

### 2. The OpenAPI document

- One document per context, its path declared in `spec/index.md` (frontmatter `interface: spec/openapi.yaml`, the
  builder's call of the key); OpenAPI 3.1, YAML.
- **Written by hand:** `paths` with their operations, `parameters`, `responses` with status codes, `components.schemas`,
  and each schema's and property's `description`.
- **Generated:** each operation's `summary` (from its first line, by id order) and `description` (every line that names
  the operation's endpoint, verbatim, each with its id). A command writes them in place (`model interface --write`, the
  builder's name; `model forms` lists the document with it as its writer), and `--check` refuses a stale document, as
  `model rules` and `model constructs` do. Nothing else in the document is rewritten: keys, order and comments of the
  hand-written parts are kept byte for byte.

### 3. Schemas read into the model

`spec_lexicon`'s layers gain the document as a layer under the glossary (spec_packs' order: packs, document, glossary,
capabilities' terms): for each schema under `components.schemas`:

- the schema is a **kind**, its noun the schema's name in words (`Video` -> video, `VideoList` -> video list), its
  definition the schema's `description`;
- each scalar property is an **attribute** of that kind, its `Type:` from the schema (integer/number -> number,
  `date-time` -> time, string -> text), its values the property's `enum` (as nouns, `Values (noun):`), its order by
  number when numeric;
- each property that is a `$ref` is a **relation row** `K | of | S` (one), and an array of `$ref`s a row `K | in | S`
  (the collection holds its members);
- a schema with `allOf` of another is a `Kind of:` it.

A property's word is its name in words (`duration`, `published_at` -> published at, `channelId` -> channel id); an
`x-term` extension on the property overrides it where the name does not read. The person did not settle this mapping;
it is the builder's to propose in the plan.

A term entry of the glossary or a capability spelled like a word the document gives is v_t16's problem (a word defined
twice) unless marked `Redefines: openapi.`; b240's `Field of:` entries are superseded by the document. b241's `Schema:`
on an artifact entry stays for schemas that are not the context's interface (a file format, a config).

### 4. The check (`model check`, new codes)

Over the lines read in grammar 4 and the document:

- an endpoint, a parameter, a parameter's value or a status a line names that the document lacks (for the operation of
  that endpoint): an error naming the line and the code;
- an operation of the document that no line names: an error naming the operation;
- a response status of an operation that no line names: a warning (2xx defaults are often unstated);
- a parameter of an operation no line names: a warning;
- a line that returns a thing of a kind the operation's 2xx response schema does not hold or is not: an error;
- a line that calls with a body of a kind the operation's request-body schema is not, or with a caller (or with no
  caller) the operation's `security` does not allow: an error;
- a stale generated `summary` or `description`: the `--check` of section 2.

Every error names both sides, so the fix is clear: add the operation to the document or reword the line.

### 5. Statements without scenarios

A line that only states the interface ("`feed` always exposes `GET /feed`.") needs no scenario: the check of section 4
already holds the endpoint to the document. The builder decides whether such a line needs its own construct or whether
"always" with a state verb of the HTTP pack suffices. A test that the running server serves every operation of the
document (status other than 404/405 on each path) is the builder's call; the person said it is conceivable, not required.

### 6. Scenarios against the server

`features generate` writes the scenario of an HTTP line as it does a CLI line: Givens of example data, a When of the call
(the endpoint, its parameters with their values, its body, its caller), Thens of the status and of what the body holds.

**Example data through a seeding interface (settled by the person, 2026-11-17).** Every server context serves, in its
test build only, one seeding endpoint (`POST /_test/seed`, the builder's path) that takes example data shaped by the
document's schemas (things of its kinds with their attribute values and rows) and makes them exist as the context would
hold them. Storage stays the context's own: the seed body speaks only the contract's words. The plugin ships generic step
handlers for HTTP lines, driven by the pack and the document: each Given becomes part of a seed call, the When the call
itself, each Then a check of the status or the body. A context writes its own handlers only for what these do not cover.
The seeding endpoint is never part of the contract: the check of section 4 ignores it, and it must not be served by a
deployed build (the builder decides how that is enforced and tested).

How the server is started for a test run is the builder's; each response is validated against its schema.

## Terminology

This plugin's glossary already has **request** (a request between contexts) and **response** is free. The HTTP pack's
call act must not read as that request: "a client requests `GET /feed`" in a context that imports both would be two
senses of one word (v_t15 refuses overlapping frames, and kinds differ, so it may pass v_t2, but readers will trip).
Settled by the person (2026-11-17): the pack's act is **call**, "a client calls `GET /feed`".

## Calls made by the session (the person may revisit)

- **`Field of:` stays allowed.** Where a context declares an interface document, a `Field of:` entry of a word the
  document gives is a warning naming both; elsewhere nothing changes. No problem code, no `migrate upgrade` step: a
  minor release, as b241's note asked ("warnings first").
- **Dependencies.** The document's prose is rewritten through a round-trip YAML library (ruamel.yaml), pinned and
  installed by `tools install` and probed by `tools probe` like clingo and pgf. Response validation and the HTTP client
  are test-time dependencies of a server context's own test environment, not of `model`.

## Left to the builder

- The pack's exact words and frames (within the terminology above).
- The key naming the document in `spec/index.md`, the command's name, the new check codes.
- The mapping of property names to words and the `x-term` override.
- Which OpenAPI features are read in the first cut (`oneOf`, `discriminator`, nullable): the first cut reads objects,
  scalars, enums, `$ref`, arrays of `$ref`, `allOf` of one; anything else a warning naming the schema.
- How the server is run under test; response validation against schemas.
- Whether a pack can ship an OpenAPI fragment of its own (b241's note mentions it); not needed for REST first.

## Order of work (for the plan)

1. The HTTP pack: words and frames, parsed in grammar 4, a construct catalogue entry, the logical form and model logic's
   facts of a call, a return and a status.
2. The document read as a layer: kinds, attributes, values, rows from schemas.
3. The check, both directions.
4. Generated prose (`--write`, `--check`) and `model forms`' row.
5. Scenarios of HTTP lines, run against a small example server in `docs/examples/` (the feed sketch), which is also the
   docs' worked example.

## The feed example

```
## Behaviour (feed)
- [r1] When a client calls `GET /feed`, `feed` shall return the feed of the viewer.
- [r2] When a client calls `GET /feed` with the `exclude` parameter set to `short`,
       `feed` shall return a feed that holds no video whose format is `short`.
- [r3] If a client calls `GET /feed` with no viewer, then `feed` shall respond with the status `401`.
```

```yaml
paths:
  /feed:
    get:
      summary: Returns the feed of the viewer.                    # generated: feed#r1
      description: |                                              # generated
        [r1] When a client calls `GET /feed`, ...
      parameters:
        - {name: exclude, in: query, schema: {enum: [short]}}
      responses:
        "200": {content: {application/json: {schema: {$ref: "#/components/schemas/Feed"}}}}
        "401": {description: No viewer.}
components:
  schemas:
    Feed:  {description: The videos a viewer is shown., properties: {videos: {type: array, items: {$ref: "#/components/schemas/Video"}}}}
    Video: {description: A video a channel published., properties: {format: {enum: [standard, short]}, duration: {type: integer}}}
```

"YouTube Short" is then no new noun: it is a video whose format is `short`. Had feed lacked the value and the parameter,
the web context's proposal (b42's design) would carry r2 with the fragment adding them.
