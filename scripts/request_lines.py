"""The check the upstream makes of a request's lines (the GF conversion's design §13, §13.4; requests r38): `work
outcome accepted` and a counter-proposal parse in the upstream's own requirement grammar, and a refusal names the
line, the refusal and `model parse`'s hint. A line is parsed in the grammar of the capability it goes into when one is
named, else in the one `spec/index.md`'s marker names (spec_language, CNL 4's I19). An upstream whose `spec/index.md`
or a capability file is not codified is refused, naming `migrate upgrade`. `root` is the upstream's repository, where
the check runs."""
from pathlib import Path

import spec_read
from shop_files import Refused


def uncodified(root):
    """The upstream's first spec file without `language: codified-1` or `codified-2`, as a path from its root, or
    None."""
    spec = Path(root) / "spec"
    for path in [spec / "index.md", *sorted((spec / "capabilities").glob("*.md"))]:
        if not spec_read.codified(path):
            return path.relative_to(root).as_posix()
    return None


def check(root, lines, capability=None):
    """Refuse the first line the upstream would not read, each in the grammar of `capability`'s file (or of the
    index); return None when every line passes."""
    old = uncodified(root)
    if old:
        raise Refused("the upstream's %s is not codified: run `migrate upgrade`" % old)
    import spec_grammar
    import spec_language
    for number, line in enumerate(lines, 1):
        try:
            parsed = spec_language.parse(root, line, capability)
        except (ImportError, spec_grammar.GrammarError) as err:
            raise Refused("the upstream's requirement grammar could not be built (%s); run "
                          "`python3 scripts/tools install`" % err) from err
        if parsed.tree is not None:
            continue
        why = "line %d does not parse in the upstream's requirement grammar: %s\n  %s" % (number, line, parsed.refusal)
        if not parsed.trees:
            hint = spec_language.hint(root, line, capability)
            why += "\n  parsed up to: %s\n  nearest words: %s" % (hint["prefix"], ", ".join(hint["near"]) or "(none)")
        raise Refused(why)
