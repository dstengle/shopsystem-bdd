"""`spec catalogue entry <catalogue>#<code> [--purpose P] [--item b<n>]` (b462, checking r59-r62): what one entry of
the rule or the construct catalogue says beside model.lp and the grammar, written into its table of
`grammar/catalogue-entries.toml` under the root (toml_edit: every other table and comment kept): its purpose, and the
item it came by (`since`), or, once it has one, an item that changed it (`changed`); and its `- Purpose:`, `- Since:`
and `- Changed:` lines written into the catalogue file in place when the file holds the entry, as `spec rules
--write` and `spec constructs --write` write them (model_catalogue_entries' `said`). An entry is named `rules#<code>`
or `constructs#<code>` (or by its catalogue's path, `grammar/rules.md#<code>`, as `spec check` names it); one of no
rule of model.lp or `spec lexicon --check` (model_rules' `rules`), or of no construct (model_constructs_table), is
refused naming it, nothing written."""
import re
import tomllib
from pathlib import Path

import toml_edit
from model_catalogue import entries
from model_catalogue_entries import said
from shop_files import LINE_BREAKS, Refused

DATA = "grammar/catalogue-entries.toml"
FILES = {"rules": "grammar/rules.md", "constructs": "grammar/constructs.md"}
OWN = re.compile(r"^- (?:Purpose|Since|Changed): ")


def codes(catalogue):
    """The codes an entry of the catalogue may have: model.lp's rules and the lexicon's, or the constructs."""
    if catalogue == "rules":
        from model_rules import rules
        return {code for code, *_ in rules()}
    from model_constructs_table import CONSTRUCTS
    return {c["code"] for c in CONSTRUCTS}


def entry(name):
    """(catalogue, code) of an entry's name; refused naming it when no rule or no construct has it."""
    catalogue, _, code = name.partition("#")
    catalogue = {path: cat for cat, path in FILES.items()}.get(catalogue, catalogue)
    if catalogue not in FILES or not code:
        raise Refused("{names} names no entry: write rules#<code> or constructs#<code>",
                      reason="catalogue entry of no rule or construct", names=["catalogue entry:%s" % name])
    if code not in codes(catalogue):
        raise Refused("{names}: no %s has the code %s" % ({"rules": "rule"}.get(catalogue, "construct"), code),
                      reason="catalogue entry of no rule or construct", names=["catalogue entry:%s" % name])
    return catalogue, code


def described(text, catalogue, code, purpose=None, item=None):
    """The TOML text with the entry's table given the purpose and the item; and the table as it then reads."""
    table = tomllib.loads(text).get(catalogue, {}).get(code)
    keys = (catalogue, code)
    if purpose is not None:
        text = toml_edit.with_key(text, keys, ("purpose",), purpose)
    if item is not None:
        found = table or {}
        if not found.get("since"):
            text = toml_edit.with_key(text, keys, ("since",), item)
        elif item != found["since"] and item not in found.get("changed", []):
            text = toml_edit.with_key(text, keys, ("changed",), list(found.get("changed", [])) + [item])
    if "changed" not in tomllib.loads(text)[catalogue][code]:
        text = toml_edit.with_key(text, keys, ("changed",), [])
    return text, tomllib.loads(text)[catalogue][code]


def relined(text, code, lines):
    """The catalogue's text with the entry `code`'s own lines in place of those it held, after its label; None when
    the catalogue holds no entry of the code."""
    for found, body in entries(text):
        if found != code:
            continue
        start = text.index("## %s\n" % code)
        rest = body.split("\n")
        kept = [x for x in rest if not OWN.match(x)]
        at = min(4, len(kept))      # the heading's end, "", the label, "": the entry's own lines come next
        new = "## %s" % code + "\n".join(kept[:at] + lines + kept[at:])
        return text[:start] + new + text[start + len("## %s" % code) + len(body):]
    return None


def describe(root, name, purpose=None, item=None):
    """Write the entry's table and its catalogue lines; the paths written, relative to the root."""
    catalogue, code = entry(name)
    if purpose is None and item is None:
        raise Refused("{names}: give --purpose or --item", reason="nothing to describe",
                      names=["catalogue entry:%s" % name])
    if purpose is not None and (not purpose.strip() or any(ch in purpose for ch in LINE_BREAKS)):
        raise Refused("the purpose is one line of text", reason="purpose not one line", names=["parameter:purpose"])
    if item is not None and not re.fullmatch(r"b[1-9]\d*", item):
        raise Refused("{names} is no item: write b<n>", reason="no such item", names=["item:%s" % item])
    root = Path(root)
    data = root / DATA
    try:
        text, table = described(data.read_text() if data.is_file() else "", catalogue, code,
                                purpose and purpose.strip(), item)
    except (tomllib.TOMLDecodeError, ValueError) as why:
        raise Refused("%s: %s" % (DATA, why)) from None
    data.parent.mkdir(parents=True, exist_ok=True)
    data.write_text(text)
    written = [DATA]
    path = root / FILES[catalogue]
    lined = relined(path.read_text(), code, said(table)) if path.is_file() else None
    if lined is not None:
        path.write_text(lined)
        written.append(FILES[catalogue])
    return written


def cmd(args):
    for rel in describe(args.root, args.entry, args.purpose, args.item):
        print("wrote %s" % rel)
    return 0


def add_parser(sub):
    p = sub.add_parser("catalogue", help="write what an entry of the rule or the construct catalogue says")
    cmds = p.add_subparsers(dest="catalogue_cmd", required=True)
    e = cmds.add_parser("entry", help="write an entry's purpose and item into grammar/catalogue-entries.toml and its catalogue")
    e.add_argument("entry", help="the entry: rules#<code> or constructs#<code>")
    e.add_argument("--purpose", help="what the rule or construct is for, one sentence")
    e.add_argument("--item", metavar="b<n>", help="the item it came by; once it has one, an item that changed it")
