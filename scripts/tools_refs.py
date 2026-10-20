"""tools: references to a name, found by jedi (refs)."""
import os
import re
import sys

from tools_env import Refused


def is_test(path):
    parts = path.replace(os.sep, "/").split("/")
    return "tests" in parts[:-1] or "test" in parts[:-1] or parts[-1].startswith("test_") or bool(re.search(r"_test\.\w+$", parts[-1]))


def cmd_refs(args):
    try:
        import jedi
    except ImportError:
        raise Refused("jedi is missing from %s: tools install" % sys.executable)
    root = os.path.abspath(".")
    # a package under src/ installed for development is found by an import hook jedi cannot follow
    project = jedi.Project(root, added_sys_path=[path for path in (root, os.path.join(root, "src")) if os.path.isdir(path)])
    last = args.name.split(".")[-1]
    defined = [d for d in project.search(last, all_scopes=True)
               if d.name == last and d.module_path and (d.full_name or "").endswith(args.name)
               and d.type in ("function", "class", "statement", "module", "instance")]
    if not defined:
        raise Refused("nothing in the project is defined as %s" % args.name)
    places, definitions = set(), set()
    for one in defined:
        definitions.add((str(one.module_path), one.line))
        script = jedi.Script(path=str(one.module_path), project=project)
        for ref in script.get_references(one.line, one.column):
            if not ref.module_path or not str(ref.module_path).startswith(root + os.sep):
                continue
            places.add((os.path.relpath(str(ref.module_path), root), ref.line))
            # 'import add as put': the uses of put are uses of add, and are under another name
            alias = re.search(r"\b%s\s+as\s+(\w+)" % re.escape(last), ref.get_line_code() or "")
            if alias:
                there = jedi.Script(path=str(ref.module_path), project=project)
                for use in there.get_references(ref.line, alias.start(1), scope="file"):
                    places.add((os.path.relpath(str(ref.module_path), root), use.line))
    places -= {(os.path.relpath(path, root), line) for path, line in definitions}
    for path, line in sorted(places):
        print("%s:%d" % (path, line))
    files = {path for path, _ in places}
    tests = {path for path in files if is_test(path)}
    print("%d reference%s to %s, in %d production and %d test files; defined at %s" % (
        len(places), "" if len(places) == 1 else "s", args.name, len(files - tests), len(tests),
        ", ".join("%s:%d" % (os.path.relpath(path, root), line) for path, line in sorted(definitions))))
    return 0
