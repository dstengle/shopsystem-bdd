#!/usr/bin/env python3
"""notes: the example's program, the CLI adapter of the notes service. Each command is a request of one operation
(spec/adapters/cli.toml): `notes add --title T --tag G`, `notes list`, `notes remove N`. The notes are kept in
notes.json beside it; a refusal exits 1 and names what is missing."""
import argparse
import json
import sys
from pathlib import Path


def load(root):
    path = Path(root) / "notes.json"
    return json.loads(path.read_text()) if path.is_file() else []


def save(root, notes):
    (Path(root) / "notes.json").write_text(json.dumps(notes, indent=1) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes")
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("--title")
    add.add_argument("--tag", action="append", default=[])
    sub.add_parser("list")
    sub.add_parser("remove").add_argument("note", type=int)
    args = parser.parse_args(argv)
    notes = load(args.root)
    if args.command == "add":
        if not args.title:
            print("notes add: a note needs --title", file=sys.stderr)
            return 1
        notes.append({"title": args.title, "tags": args.tag, "status": "kept"})
    elif args.command == "list":
        for n, note in enumerate(notes, 1):
            if note["status"] == "kept":
                print("%d %s %s" % (n, note["title"], " ".join("#" + t for t in note["tags"])))
        return 0
    else:
        notes[args.note - 1]["status"] = "removed"
    save(args.root, notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
