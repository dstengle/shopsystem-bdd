"""The CLI contract checked both ways (the domain contract design, §6.1), run by `model check` when the context has
`spec/adapters/cli.toml` (model_domain) and by its test:

- v_a1: an operation of the domain model with no table of the contract and not listed under `[unexposed]`;
- v_a2: a table naming no operation of the model, or a parameter its operation does not declare;
- v_a3: a command or an option the contract names that the program's argparse lacks (a command whose program
  `[programs]` does not name, or whose file is missing, among them);
- v_a4: a subcommand or an option of a program's argparse that no table names and that is not listed as `cli-only`
  (the contract's `[cli-only]`, or the operation's own), `-h`/`--help` aside.

The argparse of a program is caught as its `main()` is about to parse, in a process of its own (adapter_cli_probe),
so that nothing of the program runs in the check's; a hook's command is checked for its program alone. `problems(root)` gives (code, subject, why)."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import adapter_cli
import domain_model

PROBE = Path(__file__).with_name("adapter_cli_probe.py")
TIMEOUT = 60


def read_program(path):
    """{command words: set of option strings} of the program at `path`, read by adapter_cli_probe in a process of its
    own, in a scratch folder, with no input, no bytecode written into the context and a time limit; None when it never parses (or does not end)."""
    with tempfile.TemporaryDirectory() as scratch:
        try:
            done = subprocess.run([sys.executable, "-B", str(PROBE), str(Path(path).resolve())], cwd=scratch,
                                  stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=TIMEOUT)
        except subprocess.TimeoutExpired:
            return None
    last = done.stdout.rstrip("\n").rpartition("\n")[2]
    try:
        found = json.loads(last)
    except ValueError:
        return None
    return None if found is None else {c: set(o) for c, o in found.items()}


def _programs(root, contract):
    """{program word: {command words: its option strings}, or None when it cannot be read}."""
    out = {}
    for word, rel in contract.programs.items():
        path = Path(root) / rel
        top = read_program(path) if path.is_file() else None
        out[word] = None if top is None else {("%s %s" % (word, c)).strip(): o for c, o in top.items()}
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
        for option in sorted(given - leaf):
            found.append(("v_a3", "%s %s" % (op.command, option), "%s has no option %s" % (op.command, option)))
        named.setdefault(op.command, set()).update(given)
    for word, leaves in sorted(programs.items()):
        for command, leaf in sorted((leaves or {}).items()):
            if command not in named:
                if command not in contract.cli_only_commands:
                    found.append(("v_a4", command, "no operation of %s names the command %r" % (contract.path, command)))
                continue
            for option in sorted(leaf - named[command] - set(contract.cli_only_options)):
                found.append(("v_a4", "%s %s" % (command, option), "no parameter of %s names the option %s of %r"
                              % (contract.path, option, command)))
    return found
