"""The CLI adapter's contract (the domain contract design, §6.1): `spec/adapters/cli.toml`, read with `tomllib`.

Its tables: `[outcomes]` (each outcome's exit, and where its content and errors go; `json`, the option that prints
the envelope, there or at the top), `[programs]` (a command's first word and the program's path from the context's
root, which the check reads the argparse of), `[operations."<service>.<operation>"]` with `command` (the words that
request it) or `hook` (the event a hook answers, with the command it runs), its `parameters` (each `positional = <n>`
or `option = "--x"`, `repeat`, `flag`, `example`: the value given when a request says nothing of the parameter) and
its `cli-only` options, `[unexposed]` (the operations no command requests), `[cli-only]` (the options and commands
that are the adapter's own, `--root`, `--json`) and `[environment]` (each variable and the parameter or port it
feeds). A contract that does not read refused naming the file.

`spell` translates a business reference to its CLI spelling for a person (`parameter:tier` as `--tier`, `item:b12`
as `b12`); `argv` the words that request an operation with its parameters by business name."""
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

from shop_refused import Refused

PATH = Path("spec") / "adapters" / "cli.toml"


@dataclass(frozen=True)
class Parameter:
    name: str
    positional: int | None = None
    option: str | None = None
    repeat: bool = False
    flag: bool = False
    example: object = None


@dataclass
class Operation:
    id: str
    command: str = ""
    hook: str | None = None
    parameters: dict = field(default_factory=dict)
    cli_only: list = field(default_factory=list)


@dataclass
class Contract:
    path: str
    outcomes: dict
    json: str
    programs: dict
    operations: dict
    unexposed: list
    cli_only_options: list
    cli_only_commands: list
    environment: dict

    def by_command(self, words):
        """The operation a command's words request, or None."""
        words = " ".join(words.split()) if isinstance(words, str) else " ".join(words)
        return next((op for op in self.operations.values() if op.command == words and op.hook is None), None)

    def spell(self, ref, operation=None):
        """A business reference as the CLI spells it: a parameter of `operation` as its option or its positional's
        name, any other reference by its name after the kind."""
        kind, _, name = ref.partition(":")
        op = self.operations.get(operation) if operation else None
        if kind == "parameter" and op is not None and name in op.parameters:
            param = op.parameters[name]
            return param.option or name
        return name or ref


def exists(root):
    return (Path(root) / PATH).is_file()


def _strings(value, where):
    if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
        raise Refused("%s: %s is a list of strings" % (PATH, where))
    return list(value)


def _parameter(op, name, spec):
    if not isinstance(spec, dict):
        raise Refused("%s: operation %s: parameter %s is a table" % (PATH, op, name))
    unknown = set(spec) - {"positional", "option", "repeat", "flag", "example"}
    if unknown or ("positional" in spec) == ("option" in spec):
        raise Refused("%s: operation %s: parameter %s takes positional or option, and repeat, flag, example%s"
                      % (PATH, op, name, " (not %s)" % ", ".join(sorted(unknown)) if unknown else ""))
    return Parameter(name, spec.get("positional"), spec.get("option"), bool(spec.get("repeat")),
                     bool(spec.get("flag")), spec.get("example"))


def _operation(ident, table):
    if not isinstance(table, dict) or not (table.get("command") or table.get("hook")):
        raise Refused("%s: operation %s has no command" % (PATH, ident))
    params = {name: _parameter(ident, name, spec) for name, spec in (table.get("parameters") or {}).items()}
    cli_only = table.get("cli-only") or {}
    return Operation(ident, " ".join(str(table.get("command", "")).split()), table.get("hook"), params,
                     _strings(cli_only.get("options", []), "operations.%s.cli-only.options" % ident))


def parse(text, path=str(PATH)):
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as why:
        raise Refused("%s does not read: %s" % (path, why)) from None
    outcomes = dict(data.get("outcomes") or {})
    json_option = outcomes.pop("json", None) or data.get("json") or "--json"
    cli_only, unexposed = data.get("cli-only") or {}, data.get("unexposed") or {}
    return Contract(path, outcomes, json_option, dict(data.get("programs") or {}),
                    {ident: _operation(ident, table) for ident, table in (data.get("operations") or {}).items()},
                    _strings(unexposed.get("operations", []), "unexposed.operations"),
                    _strings(cli_only.get("options", []), "cli-only.options"),
                    _strings(cli_only.get("commands", []), "cli-only.commands"),
                    dict(data.get("environment") or {}))


def read(root):
    """The contract of the context at `root`, or None when it has no `spec/adapters/cli.toml`."""
    path = Path(root) / PATH
    if not path.is_file():
        return None
    return parse(path.read_text(encoding="utf-8"), str(PATH))


def argv(contract, operation, params=None, without=()):
    """The words that request `operation` with `params` ({business name: value}): each positional in its place, each
    option with its value (a flag alone, a repeated one once a value), a parameter neither given nor in `without`
    given its example; a value None or False leaves its parameter out."""
    op = contract.operations.get(operation)
    if op is None or op.hook is not None:
        raise Refused("%s names no command of the operation %s" % (contract.path, operation))
    params = dict(params or {})
    unknown = sorted(set(params) - set(op.parameters))
    if unknown:
        raise Refused("the operation %s has no parameter %s in %s" % (operation, ", ".join(unknown), contract.path))
    for name, param in op.parameters.items():
        if name not in params and name not in without and param.example is not None:
            params[name] = param.example
    options, positionals = [], []
    for name, param in op.parameters.items():
        value = params.get(name)
        if value is None or value is False:
            continue
        values = value if isinstance(value, (list, tuple)) else [value]
        if param.positional is not None:
            positionals.append((param.positional, [str(v) for v in values]))
        elif param.flag:
            options.append(param.option)
        else:
            for v in values if param.repeat else values[:1]:
                options += [param.option, str(v)]
    return op.command.split() + [v for _, values in sorted(positionals) for v in values] + options
