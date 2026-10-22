"""check and rules of scripts/model: solving the facts with model.lp, and running again under an interpreter that has
clingo when this one lacks it."""

import json
import os
import subprocess
import sys
from pathlib import Path

from model_facts import Model

LP = Path(__file__).resolve().with_name("model.lp")
SCRIPT = Path(__file__).resolve().with_name("model")     # the command check runs again (r55)
REEXEC = "SHOPSYSTEM_MODEL_REEXEC"      # set when check runs again under another interpreter (r56)


def solve(model=None):
    """The shown relations of model.lp over a model's facts (none when model is None), as (relations, labels):
    the relations sorted, the labels as {code: label} apart from them."""
    import clingo
    ctl = clingo.Control(["--warn=none"])
    ctl.add("base", [], LP.read_text() + "\n" + (model.asp() if model else ""))
    ctl.ground([("base", [])])
    atoms = []
    ctl.solve(on_model=lambda m: atoms.extend(m.symbols(shown=True)))
    out = []
    for a in atoms:
        args = [x.string if x.type == clingo.SymbolType.String else
                x.number if x.type == clingo.SymbolType.Number else str(x) for x in a.arguments]
        out.append((a.name, args))
    labels = {args[0]: args[1] for name, args in out if name == "label"}
    out = [t for t in out if t[0] != "label"]
    return sorted(out, key=lambda t: (t[0], [str(x) for x in t[1]])), labels


def rule_order(labels):
    """The codes in the order model.lp gives their labels, which puts the violations before the warnings."""
    text = LP.read_text()
    return sorted(labels, key=lambda code: text.index(f'label("{code}",'))


def interpreters():
    """The interpreters check tries for clingo, in order (r55)."""
    out = []
    if os.environ.get("SHOPSYSTEM_MODEL_PYTHON"):
        out.append(os.environ["SHOPSYSTEM_MODEL_PYTHON"])
    venvs = {(Path(v) / "bin").resolve() for v in (os.environ.get("VIRTUAL_ENV"),
                                                    sys.prefix if sys.prefix != sys.base_prefix else None) if v}
    for d in os.environ.get("PATH", "").split(os.pathsep):
        here = Path(d or ".").resolve()     # an empty entry is the current directory, named in full
        p = here / "python3"
        if p.is_file() and os.access(p, os.X_OK) and here not in venvs:
            out.append(str(p))
    out += ["/usr/local/bin/python3", "/usr/bin/python3"]
    return list(dict.fromkeys(out))


def has_clingo(python):
    try:
        return subprocess.run([python, "-c", "import clingo"], capture_output=True, timeout=60).returncode == 0
    except (OSError, subprocess.SubprocessError):
        return False


def run_again_with_clingo():
    """Run check again under the first interpreter that has clingo (r55); the interpreters tried when none has it."""
    tried = []
    for python in interpreters():
        tried.append(python)
        if has_clingo(python):
            sys.stdout.flush()
            try:
                os.execvpe(python, [python, str(SCRIPT), *sys.argv[1:]], {**os.environ, REEXEC: "1"})
            except OSError:
                continue
    return tried


def needing_clingo(command, run):
    """Run a command that solves with model.lp; without clingo it runs again under an interpreter that has it (r55)."""
    try:
        import clingo  # noqa: F401
    except ImportError:
        if os.environ.get(REEXEC):      # this is the run again (r56): it does not search a second time
            why = f"it ran again under {sys.executable}, which also failed to import clingo"
        else:
            why = "no interpreter it tried has it: " + ", ".join(run_again_with_clingo())
        print(f"{command} needs the clingo package, which this interpreter lacks; {why}.\n"
              f"  install: {sys.executable} -m pip install clingo\n"
              "  without it: `model facts` prints the facts for any Datalog or ASP engine.")
        return 2
    return run()


def rules(as_json=False):
    """Every rule's code and plain label, one a line, the violations first and then the warnings (r65);
    as one JSON object with each rule's kind when asked (r109)."""
    labels = solve()[1]
    if as_json:
        print(json.dumps({"rules": [{"code": c, "label": labels[c], "kind": "warning" if c.startswith("w_") else "violation"}
                                    for c in rule_order(labels)]}, indent=1))
        return 0
    for code in rule_order(labels):
        print(f"{code}  {labels[code]}")
    return 0


def check(args):
    model = Model(args.root).read()
    found, labels = solve(model)
    violations = [f for f in found if f[0].startswith("v")]
    warnings = [f for f in found if f[0].startswith("w_")]
    if args.json:
        printed = sorted({name for name, _ in violations + warnings}, key=rule_order(labels).index)
        print(json.dumps({"violations": violations, "warnings": warnings,
                          "unresolved": model.dangling, "problems": model.problems,
                          "labels": {code: labels[code] for code in printed}}, indent=1))
    else:
        by = {}
        for name, a in violations:
            by.setdefault(name, []).append(a)
        for name in sorted(by):
            print(f"{name}  {labels[name]}  ({len(by[name])})")
            for a in by[name][: args.limit]:
                print("    " + ", ".join(str(x) for x in a))
            if len(by[name]) > args.limit:
                print(f"    ... and {len(by[name]) - args.limit} more")
        counts = {}
        for name, _ in warnings:
            counts[name] = counts.get(name, 0) + 1
        for name in sorted(counts):
            print(f"warning {name}  {labels[name]}  ({counts[name]})")
        for d in model.dangling:
            print(f"unresolved: {d}")
        for p in model.problems:
            print(f"file: {p}")
        print(f"{len(violations)} violations, {len(warnings)} warnings, "
              f"{len(model.dangling)} unresolved references, {len(model.problems)} file problems")
    return 1 if violations or model.dangling or model.problems else 0
