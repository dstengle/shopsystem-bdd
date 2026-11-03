"""The check `work request` makes of a request's lines before it writes anything (the GF conversion's design §13,
§13.4): where the upstream's `spec/index.md` is codified, each line parses in the upstream's requirement grammar, and a
refusal names the line, the refusal and `model parse`'s hint; otherwise each line keeps the 0.29 shape `model check`
held. `root` is the upstream's repository, where the request is written."""
from pathlib import Path

import model_legacy
import spec_read
from workqueue import Refused


def check(root, lines):
    """Refuse the first line the upstream would not read; return None when every line passes."""
    if not spec_read.codified(Path(root) / "spec" / "index.md"):
        for number, line in enumerate(lines, 1):
            if not all(model_legacy.ears(line)):
                raise Refused("line %d is not in the strict form model check holds: %s" % (number, line))
        return
    import spec_grammar
    for number, line in enumerate(lines, 1):
        try:
            parsed = spec_grammar.parse(root, line)
        except (ImportError, spec_grammar.GrammarError) as err:
            raise Refused("the upstream's requirement grammar could not be built (%s); run "
                          "`python3 scripts/tools install`" % err) from err
        if parsed.tree is not None:
            continue
        why = "line %d does not parse in the upstream's requirement grammar: %s\n  %s" % (number, line, parsed.refusal)
        if not parsed.trees:
            hint = spec_grammar.hint(root, line)
            why += "\n  parsed up to: %s\n  nearest words: %s" % (hint["prefix"], ", ".join(hint["near"]) or "(none)")
        raise Refused(why)
