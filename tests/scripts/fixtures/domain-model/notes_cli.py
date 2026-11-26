#!/usr/bin/env python3
"""notes: a stand-in program of the domain-model fixture's notes service, the CLI adapter of its operations (the
domain contract design, §6.1): each command a request of one operation, its notes kept in `<root>/notes.json`, its
response printed as the plugin's commands print it (the envelope under `--json`, adapter_cli_respond)."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
from adapter_cli_respond import prepare, respond
from plumbing.domain_envelope import Response
from plumbing.shop_refused import Refused


def _notes(root):
    path = Path(root) / "notes.json"
    return json.loads(path.read_text()) if path.is_file() else []


def _keep(root, notes):
    (Path(root) / "notes.json").write_text(json.dumps(notes, indent=1) + "\n")


def _note(notes, name):
    found = [n for n in notes if n["id"] == name]
    if not found:
        raise Refused("no note {names}", reason="no such note", names=["note:%s" % name])
    return found[0]


def add(args):
    if not args.text:
        raise Refused("a note gives {names}", reason="no text", names=["parameter:text"])
    notes = _notes(args.root)
    note = {"id": "n%d" % (len(notes) + 1), "text": args.text, "priority": args.priority,
            "reminder": args.reminder, "status": "draft", "tags": []}
    _keep(args.root, notes + [note])
    print(note["id"])
    return Response("done", note)


def file(args):
    notes = _notes(args.root)
    note = _note(notes, args.note)
    if note["status"] != "draft":
        raise Refused("{names} is %s, not a draft note" % note["status"], reason="not a draft note",
                      names=["note:%s" % note["id"]])
    note["status"] = "active"
    _keep(args.root, notes)
    return Response("done", note)


def archive(args):
    notes = _notes(args.root)
    _note(notes, args.note)["status"] = "retired"
    _keep(args.root, notes)
    return Response("done")


def label(args):
    notes = _notes(args.root)
    _note(notes, args.note)["tags"] += args.tag
    _keep(args.root, notes)
    return Response("done")


def listing(args):
    notes = _notes(args.root)
    for note in notes:
        print("%s %s %s" % (note["id"], note["status"], note["text"]))
    return Response("returned", notes)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="notes", description=__doc__)
    ap.add_argument("--root", default=".")
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("add")
    a.add_argument("--text")
    a.add_argument("--priority", choices=("low", "high"), default="low")
    a.add_argument("--reminder", action="store_true")
    for name in ("file", "archive"):
        sub.add_parser(name).add_argument("note")
    lab = sub.add_parser("label")
    lab.add_argument("note")
    lab.add_argument("--tag", action="append", default=[])
    sub.add_parser("list")
    args = prepare(ap).parse_args(argv)
    handler = {"add": add, "file": file, "archive": archive, "label": label, "list": listing}[args.cmd]
    return respond("notes", handler, args)


if __name__ == "__main__":
    sys.exit(main())
