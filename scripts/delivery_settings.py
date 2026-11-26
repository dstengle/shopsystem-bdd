"""`work settings set <setting> <value>` (b462, batches r84-r86): one setting of `.shop/delivery.toml` set in its own
table (toml_edit: every comment and other key kept) and committed. The delivery settings form is the settings the
plugin reads there, each under its table and of its type (`FORM`): `base`, `batch_size`, `batch.push`, `batch.tests`,
`batch.worktrees`, `batch.rules`, `review.size`, `review.checks` and `prices.<model>`; a setting named otherwise is
refused naming the setting, and a value not of its type naming the value (`setting`, `value`). `problems`, the keys of
a settings file's text outside the form."""
import tomllib
from pathlib import Path

from measure_cost import FIELDS
from plumbing import shop_files, toml_edit
from plumbing.shop_files import Refused

REL = ".shop/delivery.toml"


def _count(v):
    return isinstance(v, int) and not isinstance(v, bool) and v >= 1


def _text(v):
    return isinstance(v, str)


def _texts(v):
    return isinstance(v, list) and all(isinstance(x, str) for x in v)


def _price(v):
    return (isinstance(v, dict) and set(v) == set(FIELDS)
            and all(isinstance(x, (int, float)) and not isinstance(x, bool) and x >= 0 for x in v.values()))


# each setting: (its table, its key) -> (what its value is, the check of it)
FORM = {((), "base"): ("a text", _text), ((), "batch_size"): ("a whole number of 1 or more", _count),
        (("batch",), "push"): ("a text", _text), (("batch",), "tests"): ("a text", _text),
        (("batch",), "worktrees"): ("a text", _text), (("batch",), "rules"): ("a list of texts", _texts),
        (("review",), "size"): ("a whole number of 1 or more", _count),
        (("review",), "checks"): ("a list of texts", _texts)}
PRICE = ("a table of %s, numbers of 0 or more" % ", ".join(FIELDS), _price)
NAMES = ["base", "batch_size", "batch.push", "batch.tests", "batch.worktrees", "batch.rules", "review.size",
         "review.checks", "prices.<model>"]


def setting(name):
    """(table, key, (what, check)) of a setting's name, `batch_size`, `review.checks` or `prices.<model>`."""
    table, _, key = name.rpartition(".") if not name.startswith("prices.") else ("prices", ".", name[7:])
    table = tuple(table.split(".")) if table else ()
    if table == ("prices",) and key:
        return table, key, PRICE
    if (table, key) not in FORM:
        raise Refused("{names} is no setting the plugin reads in %s (%s)" % (REL, ", ".join(NAMES)),
                      reason="setting outside the delivery settings form", names=["setting:%s" % name])
    return table, key, FORM[(table, key)]


def value(name, text, form):
    """The value `text` gives a setting, a TOML literal (`7`, `["a", "b"]`, `{ input = 1.0, ... }`) or, of a text
    setting, the text as it is; refused naming the value when it is not of the setting's type."""
    what, check = form
    try:
        found = tomllib.loads("v = %s\n" % text)["v"]
    except tomllib.TOMLDecodeError:
        found = None
    if check is _text and not isinstance(found, str):
        found = text
    if found is None or not check(found):
        raise Refused("{names} is not %s, as %s is read" % (what, name),
                      reason="setting value outside the delivery settings form", names=["setting value:%s" % text])
    return found


def problems(text):
    """The settings of a settings file's text outside the form, each as `<table>.<key>` (empty when it conforms)."""
    data = tomllib.loads(text)
    out = []
    for key, v in data.items():
        if isinstance(v, dict) and key in ("batch", "review", "prices"):
            for sub, w in v.items():
                form = PRICE if key == "prices" else FORM.get(((key,), sub))
                if form is None or not form[1](w):
                    out.append("%s.%s" % (key, sub))
        elif ((), key) not in FORM or not FORM[((), key)][1](v):
            out.append(key)
    return out


def set_setting(root, name, text):
    table, key, form = setting(name)
    if text is None:
        raise Refused("{names} needs its value", reason="no setting value", names=["setting:%s" % name])
    found = value(name, text, form)
    path = Path(root) / REL
    before = path.read_text(encoding="utf-8") if path.is_file() else ""
    try:
        after = toml_edit.with_key(before, table, (key,), found)
    except (tomllib.TOMLDecodeError, ValueError) as why:
        raise Refused("%s: %s" % (REL, why)) from None
    shop_files.committed(root, [REL], "work settings set: %s = %s" % (name, toml_edit.literal(found)),
                         lambda: (path.parent.mkdir(parents=True, exist_ok=True), path.write_text(after)))
    print("%s: %s = %s" % (REL, name, toml_edit.literal(found)))
    return 0


def cmd_settings(args):
    return set_setting(args.root, args.setting, args.value)


def add_parser(sub):
    p = sub.add_parser("settings", help="set a setting of .shop/delivery.toml in its own table, and commit it")
    cmds = p.add_subparsers(dest="settings_cmd", required=True)
    s = cmds.add_parser("set", help="set one setting of .shop/delivery.toml (%s) and commit it" % ", ".join(NAMES))
    s.add_argument("setting", help="the setting: %s" % ", ".join(NAMES))
    s.add_argument("value", nargs="?", help="its value as TOML (7, [\"a\", \"b\"]); a text setting's may be the bare text")


COMMANDS = {"settings": cmd_settings}
