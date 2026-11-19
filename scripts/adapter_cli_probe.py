"""The argparse of a consumer's program read in a process of its own (adapter_cli_check runs it): `python
adapter_cli_probe.py <program>` loads the program with its own folder first on sys.path and none of the plugin's, and
catches its top parser as main() is about to parse; it prints {command words: [option strings]} of every runnable
command as JSON, or `null` when the program never parses. Standard library only, so that nothing of the plugin is
loaded beside the program."""
import argparse
import importlib.machinery
import importlib.util
import json
import sys
from pathlib import Path


class _Caught(Exception):
    def __init__(self, parser):
        self.parser = parser


def _caught(self, *_args, **_kwargs):
    raise _Caught(self)


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
    return sorted({o for a in parser._actions for o in a.option_strings if o not in ("-h", "--help")})


def parser_of(path):
    path = Path(path).resolve()
    sys.path[0] = str(path.parent)
    loader = importlib.machinery.SourceFileLoader("adapter_cli_program", str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    try:
        loader.exec_module(module)
    except Exception:  # noqa: BLE001 -- a program that does not load is one whose argparse cannot be read (v_a3)
        return None
    argparse.ArgumentParser.parse_args = _caught
    argparse.ArgumentParser.parse_known_args = _caught
    sys.argv = [path.name]
    for call in (lambda: module.main([]), lambda: module.main()):
        try:
            call()
        except _Caught as got:
            return got.parser
        except TypeError:
            continue
        except BaseException:  # noqa: BLE001 -- a main that fails or exits before it parses never parses
            return None
    return None


def main():
    top = parser_of(sys.argv[1])
    found = None if top is None else {c: options(p) for c, p in commands(top).items()}
    sys.stdout = sys.__stdout__
    print("\n" + json.dumps(found))


if __name__ == "__main__":
    main()
