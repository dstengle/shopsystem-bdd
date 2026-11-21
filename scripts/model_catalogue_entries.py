"""What each entry of the rule and the construct catalogues says beside what the grammar and model.lp give it (b370):
its purpose and the items it came by and was changed by, kept in the plugin's `grammar/catalogue-entries.toml` (one
table `[rules.<code>]` or `[constructs.<code>]`: `purpose`, `since`, `changed`), which `spec rules --write` and `spec
constructs --write` write into each entry as `- Purpose:`, `- Since:` and `- Changed:`, and the header line naming
whose items they are (the plugin's context, from its `spec/index.md`). An entry the file has no table of is written
with none of these lines, which `spec check` fails (model_catalogue: v_c2, v_c3)."""
import re
import tomllib
from functools import cache
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
DATA = PLUGIN / "grammar" / "catalogue-entries.toml"


@cache
def _data(_stamp):
    return tomllib.loads(DATA.read_text()) if DATA.is_file() else {}


def data():
    """{"rules": {code: {...}}, "constructs": {code: {...}}} as the file gives them."""
    return _data(DATA.stat().st_mtime_ns if DATA.is_file() else 0)


def lines(catalogue, code):
    """The entry's `- Purpose:`, `- Since:` and `- Changed:` lines (catalogue "rules" or "constructs")."""
    return said(data().get(catalogue, {}).get(code, {}))


def said(found):
    """The `- Purpose:`, `- Since:` and `- Changed:` lines of one entry's table."""
    out = ["- Purpose: %s" % found["purpose"]] if found.get("purpose") else []
    out += ["- Since: %s" % found["since"]] if found.get("since") else []
    out += ["- Changed: %s" % ", ".join(found["changed"])] if found.get("changed") else []
    return out


def owner():
    """The context whose items Since: and Changed: name: the plugin's, `<owner>/<product>/<context name>`."""
    index = PLUGIN / "spec" / "index.md"
    found = re.search(r"^id: bounded-context/(\S+)$", index.read_text(), re.MULTILINE) if index.is_file() else None
    return found.group(1) if found else "?"


def header():
    return ("Each entry says its purpose, the item it came by (Since:) and the items that changed it (Changed:); "
            "Since: and Changed: name items of `%s`, kept in `grammar/catalogue-entries.toml`." % owner())
