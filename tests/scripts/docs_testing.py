"""What the docs test reads (the user docs' design, §9): the pages, their fenced blocks and links, the commands of the
plugin's tools read off their argparse, a ```console line checked against them, and GitHub's anchors of a page."""
import argparse
import contextlib
import functools
import importlib.machinery
import importlib.util
import pathlib
import re
import shlex
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
DOCS = REPO / "docs"
COMMANDS = DOCS / "reference" / "commands.md"
EXAMPLE = DOCS / "examples" / "notes-cli"
TOOLS = ("work", "model", "features", "tools", "measure", "migrate")
FENCE = re.compile(r"^(`{3,}|~{3,})\s*([\w-]*)")
LINK = re.compile(r"!?\[(?:[^\]\[]|\[[^\]]*\])*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
SHELL_STOPS = {"|", "||", "&&", ";", ">", ">>", "2>", "2>&1", "<"}


def newest_section(text):
    """CHANGELOG.md's newest release: from its first `## ` heading to the next one."""
    parts = re.split(r"^(?=## )", text, flags=re.MULTILINE)
    return parts[1] if len(parts) > 1 else ""


def pages():
    """{repo-relative path: text} of every page the test reads: README.md, CHANGELOG.md's newest section, and each
    docs/**/*.md but docs/history/."""
    out = {"README.md": (REPO / "README.md").read_text(encoding="utf-8")}
    log = REPO / "CHANGELOG.md"
    if log.exists():
        out["CHANGELOG.md"] = newest_section(log.read_text(encoding="utf-8"))
    for p in sorted(DOCS.rglob("*.md")):
        rel = p.relative_to(REPO)
        if rel.parts[:2] != ("docs", "history"):
            out[str(rel)] = p.read_text(encoding="utf-8")
    return out


def fenced(text):
    """[(language, body lines, the line number of the fence)] of a page's fenced blocks, and the page's lines outside
    any block as [(line number, line)]."""
    blocks, outside, open_ = [], [], None
    for n, line in enumerate(text.splitlines(), 1):
        m = FENCE.match(line.strip())
        if open_ is None and m:
            open_ = (m.group(1), m.group(2), [], n)
        elif open_ is not None and line.strip().startswith(open_[0]) and not line.strip().strip(open_[0][0]):
            blocks.append((open_[1], open_[2], open_[3]))
            open_ = None
        elif open_ is not None:
            open_[2].append(line)
        else:
            outside.append((n, line))
    return blocks, outside


def blocks_of(kind):
    """[(page:line, body lines)] of every ```<kind> block of the pages."""
    return [("%s:%d" % (page, n), body) for page, text in pages().items()
            for lang, body, n in fenced(text)[0] if lang == kind]


class _Caught(Exception):
    def __init__(self, parser):
        self.parser = parser


@functools.cache
def parser(tool):
    """The top argparse parser of one of the plugin's tools, caught as its main() is about to parse."""
    path = REPO / "scripts" / tool
    loader = importlib.machinery.SourceFileLoader("docs_cli_" + tool, str(path))
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(loader.name, loader))
    loader.exec_module(module)
    if hasattr(module, "parser") and tool == "measure":
        return module.parser()

    def caught(self, *args, **kwargs):
        raise _Caught(self)
    with _patched(argparse.ArgumentParser, "parse_args", caught), \
            _patched(argparse.ArgumentParser, "parse_known_args", caught), _patched(sys, "argv", [tool]):
        try:
            module.main() if tool in ("features", "tools") else module.main([])
        except _Caught as got:
            return got.parser
    raise AssertionError("%s's main() never parsed its arguments" % tool)


@contextlib.contextmanager
def _patched(owner, name, value):
    kept = getattr(owner, name)
    setattr(owner, name, value)
    try:
        yield
    finally:
        setattr(owner, name, kept)


def subcommands(p):
    """{name: parser} of a parser's subcommands, {} when it has none."""
    for action in p._actions:
        if isinstance(action, argparse._SubParsersAction):
            return dict(action.choices)
    return {}


def leaves(tool):
    """Every runnable command path of a tool, as words: `work backlog`, `work batch start` ..."""
    out = []

    def walk(p, words):
        subs = subcommands(p)
        if not subs:
            out.append(" ".join(words))
        for name, child in subs.items():
            walk(child, words + [name])
    walk(parser(tool), [tool])
    return out


def _options(p):
    return {o: a for a in p._actions for o in a.option_strings}


def console_commands():
    """[(page:line, command text)] of each `$ ` line of every ```console block."""
    return [(where, line.strip()[2:].strip()) for where, body in blocks_of("console") for line in body
            if line.strip().startswith("$ ")]


def tool_words(command):
    """(tool, words after it) when a console command runs one of the plugin's tools (bare, or `python3
    .../scripts/<tool>`, after any VAR=value), else None. Words stop at a pipe, a redirect or a `;`."""
    try:
        words = shlex.split(command, comments=True)
    except ValueError:
        words = command.split()
    while words and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", words[0]):
        words = words[1:]
    if words and re.fullmatch(r"python3?", words[0]):
        words = words[1:]
        if not words or not words[0].replace("\\", "/").rsplit("/", 1)[-1] in TOOLS \
                or "scripts/" not in words[0].replace("\\", "/") and "/" in words[0]:
            return None
        words[0] = words[0].replace("\\", "/").rsplit("/", 1)[-1]
    if not words or words[0] not in TOOLS:
        return None
    for i, w in enumerate(words):
        if w in SHELL_STOPS:
            words = words[:i]
            break
    return words[0], words[1:]


def command_problem(tool, words):
    """What is wrong with a command line of a tool: a subcommand its argparse does not know, or an option its
    subcommand's --help does not list; None when nothing is."""
    chain, p, path, rest = [], parser(tool), [tool], list(words)
    chain.append(p)
    while rest:
        w = rest.pop(0)
        if w.startswith("--"):
            name = w.split("=", 1)[0]
            action = next((a for q in reversed(chain) for o, a in _options(q).items() if o == name), None)
            if action is None:
                return "`%s` has no option %s" % (" ".join(path), name)
            if "=" not in w and action.nargs != 0 and rest and not rest[0].startswith("-"):
                rest.pop(0)
            continue
        if w.startswith("-") and len(w) > 1:
            if w.split("=", 1)[0] not in _options(p):
                return "`%s` has no option %s" % (" ".join(path), w)
            continue
        subs = subcommands(p)
        if subs:
            if w not in subs:
                return "`%s` has no subcommand %s (it has %s)" % (" ".join(path), w, ", ".join(subs))
            p = subs[w]
            path.append(w)
            chain.append(p)
    if subcommands(p):
        return "`%s` needs a subcommand (%s)" % (" ".join(path), ", ".join(subcommands(p)))
    return None


def slug(heading):
    """GitHub's anchor of a heading's text."""
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", heading.strip()).lower()
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


def anchors(text):
    """Every anchor of a page: each heading's slug (a repeat numbered -1, -2 as GitHub does) and each explicit
    `<a id=...>` or `<a name=...>`."""
    out, seen = set(), {}
    for _, line in fenced(text)[1]:
        m = re.match(r"^#{1,6}\s+(.*?)\s*#*\s*$", line)
        if m:
            s = slug(m.group(1))
            out.add(s if s not in seen else "%s-%d" % (s, seen[s]))
            seen[s] = seen.get(s, 0) + 1
    out.update(re.findall(r"<a\s+(?:id|name)=\"([^\"]+)\"", text))
    return out


def links(text):
    """[(line number, target)] of each relative link of a page outside its code (not http(s), mailto or the like)."""
    out = []
    for n, line in fenced(text)[1]:
        line = re.sub(r"`[^`]*`", "", line)
        for target in LINK.findall(line):
            if not re.match(r"^[a-z][a-z0-9+.-]*:", target):
                out.append((n, target))
    return out


def link_problem(page, target):
    """What is wrong with a relative link of a page (repo-relative): a file that is not there, or an anchor that a
    docs page does not have; None when it resolves."""
    path, _, anchor = target.partition("#")
    file = (REPO / page).parent / path if path else REPO / page
    file = file.resolve()
    if not file.exists():
        return "%s links %s, which is not there" % (page, target)
    in_docs = file.suffix == ".md" and (file == REPO / "README.md" or DOCS in file.parents)
    if anchor and in_docs and anchor not in anchors(file.read_text(encoding="utf-8")):
        return "%s links %s, and %s has no heading #%s" % (page, target, file.relative_to(REPO), anchor)
    return None
