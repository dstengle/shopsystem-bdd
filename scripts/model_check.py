"""check and rules of scripts/spec: solving the facts with model.lp, and running again under an interpreter that has
clingo when this one lacks it."""

import json
import os
import subprocess
import sys
from pathlib import Path

import adapter_cli_respond
from model_facts import Model

LP = Path(__file__).resolve().with_name("model.lp")
SCRIPT = Path(__file__).resolve().with_name("spec")     # the command check runs again (r55)
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
    """The codes in the order model.lp gives their labels, which puts the violations before the warnings; a code it
    has no label of (a rule of the lexicon alone, b848) after them, by its code."""
    text = LP.read_text()

    def at(code):
        found = text.find(f'label("{code}",')
        return (found if found >= 0 else len(text), code)
    return sorted(labels, key=at)


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
                os.execvpe(python, [python, str(SCRIPT), *sys.argv[1:]], {**adapter_cli_respond.marked(), REEXEC: "1"})
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
              "  without it: `shop spec facts` prints the facts for any Datalog or ASP engine.")
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


def rows(found, labels, head, limit):
    """Each relation with its label and count, then its rows up to the limit (a warning's too: decision-tiers r11)."""
    by = {}
    for name, a in found:
        by.setdefault(name, []).append(a)
    for name in sorted(by):
        print(f"{head}{name}  {labels[name]}  ({len(by[name])})")
        for a in by[name][:limit]:
            print("    " + ", ".join(str(x) for x in a))
        if len(by[name]) > limit:
            print(f"    ... and {len(by[name]) - limit} more")


def lexical(problems, labels):
    """The lexicon problems `(code, term, message)` an item's lay brings as violations `(code, [term, message])`,
    each code given its label in `labels`: model.lp's, else the rule catalogue's, else its own."""
    from model_rules import LEXICON
    for code, _, _ in problems:
        labels.setdefault(code, LEXICON[code][0] if code in LEXICON else "a rule of the lexicon")
    return [(code, [term, message]) for code, term, message in problems]


def check(args):
    model = Model(args.root).read()
    found, labels = solve(model)
    lay_only = getattr(args, "lay_only", None)       # `spec check --item`: what the item's lay alone brings (b808)
    found = [f for f in found if not (lay_only and lay_only(*f))]
    brought, reasons = getattr(args, "brought", None), []      # `spec check --item`: what the item brings (b871)
    if brought:
        found, reasons = brought(model, found, labels)
    found += lexical(getattr(args, "lexicon", ()), labels)       # `spec check --item`: the lay's lexicon (b848)
    violations = [f for f in found if f[0].startswith("v")]
    warnings = [f for f in found if f[0].startswith("w_")]
    if args.json:
        printed = sorted({name for name, _ in violations + warnings}, key=rule_order(labels).index)
        print(json.dumps({"violations": violations, "warnings": warnings,
                          "unresolved": model.dangling, "problems": model.problems, "item": reasons,
                          "labels": {code: labels[code] for code in printed}}, indent=1))
    else:
        rows(violations, labels, "", args.limit)
        rows(warnings, labels, "warning ", args.limit)
        for reason in reasons:
            print(f"item: {reason}")
        for d in model.dangling:
            print(f"unresolved: {d}")
        for p in model.problems:
            print(f"file: {p}")
        print(f"{len(violations)} violations, {len(warnings)} warnings, "
              f"{len(model.dangling)} unresolved references, {len(model.problems)} file problems")
    return 1 if violations or model.dangling or model.problems else 0
