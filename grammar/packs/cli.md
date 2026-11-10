# cli

The command-line pack: the words of a tool that a person or a session runs. A bounded context imports it with
`imports: [cli]` in the frontmatter of `spec/index.md`; a word of its own spelled the same is marked `Redefines: cli.`

## Glossary

- **tool** (noun): a program a person or a session runs. Kind of: agent.
- **command** (noun): what a person or a session runs. This: the command the run runs.
- **option** (noun): a named argument of a command, written as a code (`--json`).
- **reason** (noun): why a tool refuses a command.
- **output** (noun): what a tool prints.
- **artifact** (noun): what a thing is written to follow: a form, a schema, a layout or a reference.
- **run** (verb, action): an agent starts a command. Frame: agent runs command. Frame: agent runs command with option. Frame: agent runs command on thing.
- **print** (verb, action): a tool writes a thing to its output. Frame: tool prints thing.
- **exit** (verb, action): a tool ends, successfully or with an error naming a thing. Frame: tool exits successfully.
  Frame: tool exits with an error naming thing.
- **change** (verb, action): an agent makes a thing other than it was, or with "nothing" leaves every thing as it was. Frame: agent changes thing.
- **refuse** (verb, action): a tool declines a command. Frame: tool refuses command.
- **conform** (verb, state): a thing meets what an artifact sets out. Frame: thing conforms to artifact.
- **name** (verb, action): an agent says which thing it means, as in "refuse the command and name the reason". Frame: agent names thing.

## Definitions

- A tool refuses a command when it exits with an error on it.
