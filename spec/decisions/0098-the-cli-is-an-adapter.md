---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-cli-is-an-adapter
summary: "The CLI's programs, commands, options, exit codes and streams belong to the CLI adapter, specified by spec/adapters/cli.toml and checked against argparse; no requirement names one."
date: 2026-11-19
status: accepted
tier: check
enforced_by: [tests/scripts/test_adapter_cli_check.py]
---

# 0098. The CLI is an adapter

## Context

The requirements named commands, options and exits, so a change of interface changed business lines (the domain contract, quote-50).

## Decision

The CLI programs (work, spec, features, tools, measure, migrate), their commands, options, exit codes and streams are the CLI adapter's. spec/adapters/cli.toml maps each operation of the domain model to the command that requests it and each parameter to its option or positional; the specification check holds it to argparse both ways (v_a1-v_a4). No requirement line names a program, a command, an option or an exit.

## Alternatives

Keeping the CLI pack's words in the lines (run, option, print, exit): rejected, an interface change would retire business lines.
