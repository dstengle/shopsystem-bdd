"""What is still read of plugin 0.30's frozen queue, `.shop/work/` (workflow simplification plan 9, D5, D6): only the
`source:` ids of its initiatives and requests, as citations of observations. Frozen history is never checked, so a
file whose frontmatter does not read is passed over, never refused. Standard library only."""
import re
from pathlib import Path

from model_parse import (
    frontmatter,  # the reader scripts/model uses; model_work imports this module
)

WORK = Path(".shop") / "work"
IDENT = re.compile(r"[a-z-]+/[\w./-]+")


def sources(root):
    """Every id named in the `source:` of `.shop/work/*/initiative.md` and `.shop/work/requests/*.md`."""
    work = Path(root) / WORK
    found = set()
    for path in sorted(work.glob("*/initiative.md")) + sorted(work.glob("requests/*.md")):
        try:
            data = frontmatter(path.read_text(encoding="utf-8"))[0]
        except (OSError, UnicodeDecodeError, ValueError):
            continue
        source = data.get("source") if isinstance(data, dict) else None
        found.update(IDENT.findall(str(source or "")))
    return found
