"""batch-measurement's steps for how measure reads files: a line break inside a JSON string, times ending in Z."""
import json

from pytest_bdd import given, parsers, then


@given(parsers.parse("the text of one of those messages holds U+{code} inside its JSON string"))
def text_holds(world, code):
    session = list(world.store)[-1]
    rows = [json.loads(line) for line in world.store[session].splitlines()]
    rows[0]["message"]["content"] = [{"type": "text", "text": "before%safter" % chr(int(code, 16))}]
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    assert chr(int(code, 16)) in text
    world.store[session] = text


@then("measure exits successfully")
def exits_successfully(world):
    assert world.code == 0, world.err
