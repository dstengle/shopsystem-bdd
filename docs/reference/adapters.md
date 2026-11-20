# Adapter contracts

A requirement line says what happens between the parties: the person asks a service for an operation, the service
answers. It never names a command, an option, an exit code, a file or a pull request. Those are a **port's**
business, and each port's **adapter** has its own contract beside the specification, in `spec/adapters/`. Change the
interface and the contract changes; no line does. This page is the reference of the CLI adapter's contract,
`spec/adapters/cli.toml`, and of the response every adapter renders.

## The response

Every operation answers with one shape, whatever the port:

| field | what it holds |
|---|---|
| `outcome` | `done`, `returned`, `refused`, `passed` or `failed`: the domain's outcomes, which lines state; or `broken`, a failure of the infrastructure, outside the domain and never stated by a line |
| `content` | what the operation returns: the domain object or list its model names, by its attributes |
| `errors` | each a `{reason, names}`: a refusal's reason (one the operation declares under `refused:`) and the things it names by business reference (`parameter:tier`, `item:b12`, `rule:v_d6`) |
| `notices` | what completed but should be said, such as a change kept but not shared |

`errors` holds something exactly when the outcome is `refused` or `failed`. The CLI renders the response as text for
people, and as one JSON object under `--json`:

```console
$ work show b12 --json
{
  "outcome": "returned",
  "content": {
    "item": {
      "id": "b12",
      ...
  "errors": [],
  "notices": []
}
```

Every command takes `--json`. A command that printed a JSON object of its own before 0.38.0 now prints it under
`content` (see the [0.38.0 changes](../../CHANGELOG.md)); [Commands](commands.md) has each.

## `spec/adapters/cli.toml`

TOML, one table per operation of the [domain model](domain-model.md). The example context's whole contract:

```toml
adapter = "cli"
json = "--json"

[programs]
notes = "notes.py"

[outcomes]
done = { exit = 0 }
returned = { exit = 0, content = "stdout" }
refused = { exit = 1, errors = "stderr" }
broken = { exit = 1, errors = "stderr" }

[cli-only]
options = ["--root", "--json"]

[operations."notes.add"]
command = "notes add"
requirements = [
  "notes#r1: When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.",
  "notes#r2: If the person adds a note without a title, then the notes service shall refuse the request and name the title.",
]
[operations."notes.add".parameters]
title = { option = "--title", example = "Buy milk" }
tag = { option = "--tag", repeat = true }

[operations."notes.list"]
command = "notes list"
requirements = [
  "notes#r3: When the person lists the notes, the notes service shall return every note.",
]

[operations."notes.remove"]
command = "notes remove"
requirements = [
  "notes#r4: When the person removes a note, the notes service shall set the status of the note to `removed`.",
]
[operations."notes.remove".parameters]
note = { positional = 1, example = "1" }
```

- **`[programs]`** maps a command's first word to its program, a path from the context's root.
- **`[outcomes]`** says how each outcome shows: its exit code (0 or 1, never another), and the stream its content
  and its errors go to. `json` names the option that prints the envelope.
- **`[operations."<service>.<operation>"]`** gives the `command` that requests the operation, or a `hook` (a Claude
  Code hook that drives it, such as `SessionStart`) with its `command`.
- **`requirements`** under an operation's table lists, generated, the requirements that govern it: each line whose
  trigger requests the operation, its refusals among them, as `"<capability>#r<n>: <line>"`. `spec annotate` writes
  them; never edit them by hand.
- **`[operations."...".parameters]`** maps each parameter, by its business name, to an `option` or a `positional`
  place; `repeat = true` for an option given more than once, `flag = true` for a boolean one, and `example`, the value
  a scenario's driver gives a required parameter the step leaves out.
- **`[cli-only]`** lists the options and commands that are the adapter's own (`--root`, `--json`, `--hook`; a command
  that prints a report no operation names); an operation's own table may list its CLI-only options too.
- **`[unexposed]`** lists the operations no command requests (an agent performs them when dispatched).
- **`[environment]`** names each environment variable the adapter reads, and the parameter or port it feeds.

A refusal names business references; the adapter spells them its way. `parameter:title` prints as `--title` in the
message on stderr, `item:b12` as `b12`; the JSON envelope keeps the references.

### Checked both ways

`spec check` reads the contract and each program's argparse (caught as its `main()` is about to parse) and holds the
two to each other:

| code | what it catches |
|---|---|
| `v_a1` | an operation of the model with no table and not under `[unexposed]` |
| `v_a2` | a table naming no operation of the model, or a parameter its operation does not declare |
| `v_a3` | a command or an option the contract names that the program's argparse lacks |
| `v_a4` | a subcommand or an option of the argparse that no table names and that is not CLI-only |
| `v_a5` | an operation that does not hold a requirement that governs it (`spec annotate` writes it) |
| `v_a6` | an operation that holds a requirement that no longer governs it (`spec annotate` takes it out) |

## The scenarios' driver

A generated scenario says the request in domain words: "When the person adds a note n1 without a title". A
driver makes such a request through the adapter: this repository's `tests/scenarios/driver_cli.py` reads `cli.toml`,
builds the command line from the operation and the step's parameters, runs it with `--json`, and reads back the
response, so that "Then the notes service refuses this request" can check `outcome == "refused"` and "names the
title" the error's names. This repository's generated scenarios do not go through it yet: their request steps are
re-keyed to the earlier CLI handlers, which read the printed text and the exit code (b358 moves them onto the
driver). The [getting started](../getting-started.md#6-the-session-builds-it) binding makes the
request and checks the envelope by hand.

## Other ports

A port is anything the domain talks through: the CLI and hooks (driving: they make requests), and git as the store,
GitHub as the issue host, GF and clingo as the parser and solver (driven: the services use them). Each mechanism is
recorded as a design-decision, not as a line: "The CLI is an adapter", "GitHub issues carry context requests", "Pull
requests carry a batch's change to review", "Git is the store and the isolation", "Files under spec/ and .shop/ are
the storage", "Hooks are a driving adapter", "The response envelope" ([`spec/decisions/`](../../spec/decisions/)).
An HTTP service in front of the same model would need a second contract (OpenAPI) and a second driver; no line
changes.
