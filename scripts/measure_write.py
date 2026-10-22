"""measure's record: one measurement as a record of kind `measurement`, its figures one JSON block in its body.
Standard library only."""
import datetime
import json
from pathlib import Path

import workqueue
from measure_read import Refused

DIRECTORY = Path(".shop") / "records" / "measurements"


def today():
    return datetime.date.today().isoformat()


def path_of(root, initiative, date):
    return Path(root) / DIRECTORY / ("%s-%s.md" % (date, initiative))


def check_unwritten(root, initiative, date, replace):
    """The path of the measurement; refused when it exists and `replace` is not given."""
    path = path_of(root, initiative, date)
    if path.exists() and not replace:
        raise Refused("the measurement %s exists; --replace writes over it" % path.relative_to(root))
    return path


def text_of(root, initiative, date, figures):
    try:
        context = workqueue.context_path(root)
    except workqueue.Refused as why:
        raise Refused(str(why)) from None
    head = ("---\nid: measurement/%s/%s-%s\nkind: measurement\nabout: bounded-context/%s\ndate: %s\n---\n\n"
            % (context, date, initiative, context, date))
    return "%s# Measurement of %s\n\n```json\n%s\n```\n" % (head, initiative, json.dumps(figures, indent=2))


def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
