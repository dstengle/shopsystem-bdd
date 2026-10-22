"""scripts/features' reading of the tests that bind scenarios: bindings (with --unbound) and rebind."""
import ast
import json
import os

from features_gherkin import Refused, locate


def test_modules(tests):
    """Every *.py under tests, parsed: (path, source bytes, tree, the module's top-level string assignments)."""
    found = []
    for root, _, names in sorted(os.walk(tests)):
        for name in sorted(names):
            if not name.endswith(".py"):
                continue
            path = os.path.join(root, name)
            with open(path, "rb") as handle:
                source = handle.read()
            try:
                tree = ast.parse(source, path)
            except SyntaxError as why:
                raise Refused("%s does not parse: %s" % (path, why))
            strings = {t.id: n.value.value for n in tree.body if isinstance(n, ast.Assign)
                       and isinstance(n.value, ast.Constant) and isinstance(n.value.value, str)
                       for t in n.targets if isinstance(t, ast.Name)}
            found.append((path, source, tree, strings))
    return found


_ALIASES = {}  # id(tree) -> (tree, {alias: pytest_bdd name}): each module's imports read once, not once a call


def aliases(tree):
    """`from pytest_bdd import <name> as <alias>` of `tree`: {alias: name}, the first import of an alias winning."""
    if id(tree) not in _ALIASES:
        found = {}
        for n in ast.walk(tree):
            if isinstance(n, ast.ImportFrom) and n.module == "pytest_bdd":
                for a in n.names:
                    found.setdefault(a.asname, a.name)
        _ALIASES[id(tree)] = (tree, found)
    return _ALIASES[id(tree)][1]


def called_name(node, tree=None):
    """The name a call goes by; `from pytest_bdd import scenario as s` makes s(...) a call of scenario."""
    name = node.func.id if isinstance(node.func, ast.Name) else getattr(node.func, "attr", None)
    if tree is not None and isinstance(node.func, ast.Name) and name in aliases(tree):
        return aliases(tree)[name]
    return name


def binding_calls(tests):
    """Every scenario(<feature>, "<title>") call under tests: (path, source bytes, feature or None, title node)."""
    found = []
    for path, source, tree, names_ in test_modules(tests):
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or len(node.args) < 2:
                continue
            title = node.args[1]
            if called_name(node, tree) != "scenario" or not isinstance(title, ast.Constant) or not isinstance(title.value, str):
                continue
            first = node.args[0]
            feature = first.value if isinstance(first, ast.Constant) else names_.get(getattr(first, "id", None))
            found.append((path, source, feature if isinstance(feature, str) else None, title))
    return found


def scenarios_calls(tests):
    """Every scenarios(<path>, ...) call under tests: (path, line, the feature files or directories it names)."""
    found = []
    for path, _, tree, names_ in test_modules(tests):
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and called_name(node, tree) == "scenarios":
                named = [a.value if isinstance(a, ast.Constant) else names_.get(getattr(a, "id", None)) for a in node.args]
                found.append((path, node.lineno, [n for n in named if isinstance(n, str)]))
    return found


def unbound_report(args, files):
    """(feature path, title, the calls binding it) for each scenario of the files named after --unbound that no call binds, or several calls bind."""
    if args.unbound:
        wanted = {os.path.realpath(p) for p in args.unbound}
        for p in args.unbound:
            if not any(os.path.realpath(path) == os.path.realpath(p) for path, _ in files):
                raise Refused("%s is not a feature file under %s" % (p, args.dir))
    else:
        wanted = {os.path.realpath(path) for path, _ in files}
    calls = {}  # (feature file, title) -> ["<module>:<line>", ...]
    every = scenarios_calls(args.tests)
    for path, f in files:
        real = os.path.realpath(path)
        for module, line, named in every:
            for name in named:
                folder = os.path.realpath(os.path.join(args.dir, name))
                if os.path.isdir(folder):
                    hit = real.startswith(folder + os.sep)
                else:
                    hit = os.path.basename(name) == os.path.basename(path)
                if hit:
                    for title in {sc.title for sc in f.scenarios}:
                        calls.setdefault((real, title), []).append("%s:%d" % (module, line))
    for module, _, feature, title in binding_calls(args.tests):
        for path, f in files:
            if (feature is None or os.path.basename(feature) == os.path.basename(path)) \
                    and any(sc.title == title.value for sc in f.scenarios):
                calls.setdefault((os.path.realpath(path), title.value), []).append("%s:%d" % (module, title.lineno))
    out = []
    for path, f in files:
        real = os.path.realpath(path)
        if real not in wanted:
            continue
        for title in dict.fromkeys(sc.title for sc in f.scenarios):
            where = calls.get((real, title), [])
            if len(where) != 1:
                out.append((path, title, sorted(where)))
    return out


def unbound_line(path, title, where):
    return "%s: %s | bound by %s" % (path, title, ", ".join(where) if where else "no test")


def cmd_bindings(args, files):
    titles = {}
    for path, f in files:
        for sc in f.scenarios:
            titles.setdefault(sc.title, set()).add(os.path.basename(path))
    lost = []
    for path, _, feature, title in binding_calls(args.tests):
        have = titles.get(title.value, set())
        if not have or (feature and os.path.basename(feature) not in have):
            lost.append({"file": path, "line": title.lineno, "title": title.value, "feature": feature})
    unbound = unbound_report(args, files) if args.unbound is not None else []
    if args.json:
        print(json.dumps({"wrong": lost, "unbound": [{"file": p, "title": t, "bound_by": w} for p, t, w in unbound]}))
        return 1 if lost or unbound else 0
    for one in lost:
        print('%s:%d: no scenario titled "%s" in %s' % (one["file"], one["line"], one["title"], one["feature"] or "any feature file"))
    if not lost:
        print("every binding names a scenario")
    for one in unbound:
        print(unbound_line(*one))
    return 1 if lost or unbound else 0


def cmd_rebind(args, files):
    locate(files, args.new, args)
    edits = {}
    only = os.path.realpath(args.file) if args.file else None
    for path, source, feature, title in binding_calls(args.tests):
        if title.value != args.old:
            continue
        if only and (feature is None or os.path.realpath(os.path.join(args.dir, feature)) != only):
            continue
        if title.lineno != title.end_lineno:
            raise Refused("%s:%d: the title is written over several lines" % (path, title.lineno))
        edits.setdefault(path, (source, []))[1].append(title)
    literal = ('"%s"' % args.new.replace("\\", "\\\\").replace('"', '\\"')).encode()
    count = 0
    for path, (source, nodes) in edits.items():
        lines = source.split(b"\n")
        for node in sorted(nodes, key=lambda n: (n.lineno, n.col_offset), reverse=True):
            line = lines[node.lineno - 1]
            lines[node.lineno - 1] = line[:node.col_offset] + literal + line[node.end_col_offset:]
            count += 1
        with open(path, "wb") as handle:
            handle.write(b"\n".join(lines))
    print("%d binding%s rebound" % (count, "" if count == 1 else "s"))
    return 0
