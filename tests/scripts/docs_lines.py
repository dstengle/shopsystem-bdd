"""The requirement lines of the docs (b263): every line of any code block of a page that reads as a requirement, with
the context it is read in and whether the page shows it refused. A ```reading block is test_docs.py's; a ```mermaid
block holds no line.

A line is a sentence that says `shall` and ends with one `.`: a ```requirement or ```refused line, a capability
file's `- [r<n>] ` bullet in a ```markdown or ```diff block, a `model explain` row `<cap>#r<n>  <line>`, a
`before`/`after` row, and the argument of a `$ ` command in a ```console block. A line is shown refused when its
block is ```refused, or when it is the argument of `$ model parse` whose output prints `may follow:` or `refused`.

The context a block is read in: the one an HTML comment `<!-- docs: context <dir> -->` names on the line before its
fence (a fixture context of tests/scripts/fixtures/, for a page's sketch of a context no repository holds); else a
console command's `--root <dir>`; else docs/examples/notes-cli/ for its own pages and docs/getting-started.md; else
this repository."""
import pathlib
import re
import shlex

from docs_testing import EXAMPLE, FENCE, REPO

MARK = re.compile(r"^<!--\s*docs:\s*context\s+(\S+)\s*-->$")
SHALL = re.compile(r"\bshall\b")
PREFIX = re.compile(r"^(?:[+-]?\s*-\s*\[\w+\]\s*|\S+#[rU]\d+\s+|(?:before|after)\s+\[\w+\]\s+|line \d+: \w+ - )")
OPENING = re.compile(r"(?:^|(?<=: ))(?:While|When|If|Where|A|An|The|Every|No|`)")
EXAMPLE_PAGES = ("docs/getting-started.md",)
SKIPPED = ("reading", "mermaid")


def blocks(text):
    """[(language, body lines, fence line number, the context its marker names or None)] of a page."""
    out, open_, mark = [], None, None
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        m = FENCE.match(s)
        if open_ is None and m:
            open_ = (m.group(1), m.group(2), [], n, mark)
        elif open_ is not None and s.startswith(open_[0]) and not s.strip(open_[0][0]):
            out.append(open_[1:])
            open_ = None
        elif open_ is not None:
            open_[2].append(line)
        if open_ is None and s:
            mark = None
            if (got := MARK.match(s)) and FENCE.match(s) is None:
                mark = REPO / got.group(1)
    return out


def page_root(page):
    return EXAMPLE if page.startswith("docs/examples/notes-cli/") or page in EXAMPLE_PAGES else REPO


def sentence(text):
    """The requirement line in a row of a block: its prefix taken off, or None when the row holds none."""
    s = PREFIX.sub("", text.strip())
    if not SHALL.search(s) or not s.endswith(".") or s.endswith(".."):
        return None
    m = OPENING.search(s)
    return s[m.start():] if m else None


def command_lines(body, i):
    """[(line, refused, root or None)] of the arguments of the `$ ` row i of a console block."""
    row = body[i].strip()[2:]
    try:
        words = [w.replace("\\`", "`") for w in shlex.split(row)]
    except ValueError:
        words = row.split()
    output = []
    for later in body[i + 1:]:
        if later.strip().startswith("$ "):
            break
        output.append(later.strip())
    refused = "model" in words[:2] and "parse" in words and \
        any("may follow:" in o or o.startswith("refused") for o in output)
    root = REPO / words[words.index("--root") + 1] if "--root" in words[:-1] else None
    return [(w, refused, root) for w in words if SHALL.search(w) and w.endswith(".")]


def lines(page, text):
    """[(page:line, line, refused, root)] of every requirement line of a page's code blocks."""
    out = []
    for lang, body, n, mark in blocks(text):
        if lang in SKIPPED:
            continue
        for i, row in enumerate(body):
            where = "%s:%d" % (page, n + 1 + i)
            if lang == "console" and row.strip().startswith("$ "):
                out += [(where, line, refused, mark or root or page_root(page))
                        for line, refused, root in command_lines(body, i)]
            elif lang != "console" or not row.strip().startswith(("$", ">")):
                line = sentence(row)
                if line:
                    out.append((where, line, lang == "refused", mark or page_root(page)))
    return out


def context(root):
    """A context's path relative to this repository, as a message names it."""
    return str(pathlib.Path(root).relative_to(REPO)) if root != REPO else "this repository"
