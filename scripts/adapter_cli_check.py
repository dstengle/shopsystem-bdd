"""The CLI contract checked both ways (the domain contract design, §6.1), run by `model check` when the context has
`spec/adapters/cli.toml` (model_domain) and by its test:

- v_a1: an operation of the domain model with no table of the contract and not listed under `[unexposed]`;
- v_a2: a table naming no operation of the model, or a parameter its operation does not declare;
- v_a3: a command or an option the contract names that the program's argparse lacks (a command whose program
  `[programs]` does not name, or whose file is missing, among them);
- v_a4: a subcommand or an option of a program's argparse that no table names and that is not listed as `cli-only`
  (the contract's `[cli-only]`, or the operation's own), `-h`/`--help` aside.

The argparse of a program is caught as its `main()` is about to parse (as tests/scripts/docs_testing.py catches the
plugin's tools); a hook's command is checked for its program alone. `problems(root)` gives (code, subject, why)."""
import argparse
import contextlib
import importlib.machinery
import importlib.util
import sys
from pathlib import Path

import adapter_cli
import domain_model


class _Caught(Exception):
    def __init__(self, parser):
        self.parser = parser


@contextlib.contextmanager
def _patched(owner, name, value):
    kept = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield
    finally:
        setattr(owner, name, kept)


def parser_of(path):
    """The top argparse parser of the program at `path`, caught as its main() is about to parse; None if it never
    parses."""
    path = Path(path)
    loader = importlib.machinery.SourceFileLoader("adapter_cli_program_%s" % abs(hash(str(path))), str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    folder = str(path.parent)
    sys.path.insert(0, folder)
    try:
        try:
            loader.exec_module(module)
        except Exception:  # noqa: BLE001 -- a program that does not load is one whose argparse cannot be read (v_a3)
            return None

        def caught(self, *_args, **_kwargs):
            raise _Caught(self)
        with _patched(argparse.ArgumentParser, "parse_args", caught), \
                _patched(argparse.ArgumentParser, "parse_known_args", caught), _patched(sys, "argv", [path.name]):
            for call in (lambda: module.main([]), lambda: module.main()):
                try:
                    call()
                except _Caught as got:
                    return got.parser
                except TypeError:
                    continue
    finally:
        sys.path.remove(folder)
    return None


def commands(parser, words=()):
    """{command words: leaf parser} of every runnable command under `parser`."""
    subs = [a for a in parser._actions if isinstance(a, argparse._SubParsersAction)]
    if not subs:
        return {" ".join(words): parser}
    out = {}
    for name, child in subs[0].choices.items():
        out.update(commands(child, tuple(words) + (name,)))
    return out


def options(parser):
    """The option strings of a parser, -h and --help aside."""
    return {o for a in parser._actions for o in a.option_strings if o not in ("-h", "--help")}


def _programs(root, contract):
    """{program word: {command words: leaf parser}, or None when it cannot be read}."""
    out = {}
    for word, rel in contract.programs.items():
        path = Path(root) / rel
        top = parser_of(path) if path.is_file() else None
        out[word] = None if top is None else {("%s %s" % (word, c)).strip(): p for c, p in commands(top).items()}
    return out


def problems(root, model=None):
    """(code, subject, why) of every v_a1-v_a4 of the context at `root`; none when it has no CLI contract."""
    contract = adapter_cli.read(root)
    if contract is None:
        return []
    model = model or domain_model.load(root)
    found, ops = [], {"%s.%s" % (o.service, o.name): o for o in model.operations()}
    for ident in sorted(set(ops) - set(contract.operations) - set(contract.unexposed)):
        found.append(("v_a1", ident, "the operation %s has no table in %s and is not unexposed" % (ident, contract.path)))
    for ident, op in contract.operations.items():
        if ident not in ops:
            found.append(("v_a2", ident, "%s names the operation %s, which the model does not declare"
                          % (contract.path, ident)))
            continue
        declared = {p.name for p in ops[ident].parameters}
        for name in sorted(set(op.parameters) - declared):
            found.append(("v_a2", "%s.%s" % (ident, name), "%s names the parameter %s, which %s does not declare"
                          % (contract.path, name, ident)))
    programs = _programs(root, contract)
    named = {}
    for ident, op in contract.operations.items():
        word = op.command.split()[0] if op.command else ""
        if word not in programs:
            found.append(("v_a3", ident, "the command %r names no program of [programs]" % op.command))
            continue
        if programs[word] is None:
            found.append(("v_a3", ident, "the program %s of %s does not parse its arguments with argparse"
                          % (contract.programs[word], word)))
            continue
        if op.hook is not None:
            continue
        leaf = programs[word].get(op.command)
        if leaf is None:
            found.append(("v_a3", ident, "%s has no command %r" % (contract.programs[word], op.command)))
            continue
        given = {p.option for p in op.parameters.values() if p.option} | set(op.cli_only)
        for option in sorted(given - options(leaf)):
            found.append(("v_a3", "%s %s" % (op.command, option), "%s has no option %s" % (op.command, option)))
        named.setdefault(op.command, set()).update(given)
    for word, leaves in sorted(programs.items()):
        for command, leaf in sorted((leaves or {}).items()):
            if command not in named:
                if command not in contract.cli_only_commands:
                    found.append(("v_a4", command, "no operation of %s names the command %r" % (contract.path, command)))
                continue
            for option in sorted(options(leaf) - named[command] - set(contract.cli_only_options)):
                found.append(("v_a4", "%s %s" % (command, option), "no parameter of %s names the option %s of %r"
                              % (contract.path, option, command)))
    return found
