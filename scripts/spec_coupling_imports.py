"""The code imports of `spec coupling` (b744, checking r147; decision 0151): each area's module group declared in
`.shop/modules.toml` (a table `[<area>]` with `modules`, path patterns relative to the repository's root, `**` across
folders; a file two tables match the first table's, a file none matches no area's: `area_of`), and each tracked Python
file (a `.py` file or one with a `python` shebang) of one area whose import or from-import statement, read by ast,
names a tracked Python file of another area (a bare name a file of the importer's folder, else a dotted name resolved
under the root, else under each folder that holds an area's file, a package's by the folder above its packages, as the
path a program or a test runs with: `folders`, `imported`, b772), the coupling of the imported file's area by the importer's holding `<importer> ->
<imported>` (`imports`)."""
import ast
import re
import subprocess
import tomllib
from pathlib import Path, PurePosixPath

MODULES = Path(".shop") / "modules.toml"


def _regex(pattern):
    """A path pattern as a regular expression: `**/` any folders, `**` anything, `*` and `?` within one name."""
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out, i = out + "(?:.*/)?", i + 3
        elif pattern.startswith("**", i):
            out, i = out + ".*", i + 2
        else:
            out += {"*": "[^/]*", "?": "[^/]"}.get(pattern[i], re.escape(pattern[i]))
            i += 1
    return re.compile(out + r"\Z")


def groups(root):
    """[(area, [regex, ...])] of `.shop/modules.toml` in its file order; none without the file."""
    path = Path(root) / MODULES
    if not path.is_file():
        return []
    tables = tomllib.loads(path.read_text())
    return [(area, [_regex(p) for p in table.get("modules", [])])
            for area, table in tables.items() if isinstance(table, dict)]


def area_of(declared, path):
    """The area of the first table whose patterns match `path`, else None."""
    return next((area for area, patterns in declared if any(p.match(path) for p in patterns)), None)


def tracked(root):
    """The tracked Python files of the repository at `root`, relative posix paths."""
    done = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, text=True)
    if done.returncode != 0:
        return []
    found = []
    for name in filter(None, done.stdout.split("\0")):
        path = Path(root) / name
        if path.is_file() and (name.endswith(".py") or _shebang(path)):
            found.append(name)
    return sorted(found)


def _shebang(path):
    try:
        with open(path, "rb") as f:
            first = f.readline(200)
    except OSError:
        return False
    return first.startswith(b"#!") and b"python" in first


def _names(tree):
    """(level, dotted module) of each module an import or from-import statement of `tree` names."""
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            yield from ((0, a.name) for a in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                yield node.level, node.module
            yield from ((node.level, ".".join(filter(None, (node.module, a.name)))) for a in node.names)


def folders(declared, files):
    """The sorted folders that hold an area's file among `files`, a file of a package by the folder above its
    packages (a folder holding an `__init__.py` of `files`): where an absolute import is looked up past the root."""
    found = set()
    for name in files:
        if area_of(declared, name) is None:
            continue
        folder = PurePosixPath(name).parent
        while str(folder) != "." and str(folder / "__init__.py") in files:
            folder = folder.parent
        found.add(str(folder))
    return sorted(found)


def imported(importer, level, module, files, extra=()):
    """The tracked Python file `module` names from `importer`, else None; an absolute name looked up in the
    importer's folder, the root, then each of `extra` (`folders`)."""
    folder = PurePosixPath(importer).parent
    for _ in range(max(level - 1, 0)):
        folder = folder.parent
    parts = module.split(".")
    bases = [folder] if level else [folder, PurePosixPath("."), *map(PurePosixPath, extra)]
    for base in bases:
        for candidate in (base.joinpath(*parts[:-1], parts[-1] + ".py"), base.joinpath(*parts, "__init__.py")):
            name = str(candidate)
            if name in files:
                return name
    return None


def imports(root):
    """(area imported, area importing, `<importer> -> <imported>`) of each import between two areas' files."""
    declared = groups(root)
    if not declared:
        return
    files = set(tracked(root))
    extra = folders(declared, files)
    for importer in sorted(files):
        by = area_of(declared, importer)
        if by is None:
            continue
        try:
            tree = ast.parse((Path(root) / importer).read_text())
        except (SyntaxError, UnicodeDecodeError, ValueError):
            continue
        for level, module in sorted(set(_names(tree))):
            target = imported(importer, level, module, files, extra)
            area = target and area_of(declared, target)
            if area and area != by:
                yield area, by, "%s -> %s" % (importer, target)
