"""adapter_annotate: each operation's requirements written into the contract's text, every other line kept, and
written again in place of what an operation held before (checking r48-r51, b368)."""
import adapter_annotate
import adapter_cli

TEXT = '''# a comment
adapter = "cli"

[operations."notes.add"]
command = "notes add"
requirements = ["notes#r9: gone."]
[operations."notes.add".parameters]
title = { option = "--title" }

[operations."notes.list"]
command = "notes list"
requirements = [
  "notes#r8: gone too.",
]

[environment]
'''


def test_each_operation_given_what_governs_it_and_nothing_else():
    governs = {"notes.add": [("notes#r1", 'When the person adds a "note", it is kept.')]}
    out = adapter_annotate.annotated(TEXT, governs)
    contract = adapter_cli.parse(out)
    assert contract.operations["notes.add"].requirements == ["notes#r1"]
    assert contract.operations["notes.list"].requirements == []
    assert contract.operations["notes.add"].parameters["title"].option == "--title"
    assert out.startswith("# a comment\n") and "gone" not in out


def test_annotated_twice_is_annotated_once():
    governs = {"notes.list": [("notes#r2", "When the person lists the notes, they are returned.")]}
    once = adapter_annotate.annotated(TEXT, governs)
    assert adapter_annotate.annotated(once, governs) == once
    assert once.count("requirements = [") == 1
