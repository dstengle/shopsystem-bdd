"""`work list` and `work show <request>` (capability requests, r25, r26; workflow simplification plan 9, D6, D9).

`list` gives each request with its status, and each observation of `.shop/records/observations.md` that no request's
nor any frozen initiative's `source` names (shop_frozen); `show` gives one request: its status, whose turn it is
and the URL of its issue, each line with its line outcome, each question with its answer, the resolution. Both only read. Plugin 0.30's
initiatives and work-items are frozen under `.shop/work/` and read as files, never listed."""
import json
import re
from pathlib import Path

import request_moves
import request_text
import shop_frozen
from shop_files import Refused, read


def uncited(root):
    """(id, date) of each observation that no request's or frozen initiative's `source` names."""
    path = Path(root) / ".shop" / "records" / "observations.md"
    if not path.is_file():
        return []
    cited = set(shop_frozen.sources(root))
    for _, _, _, source in request_text.requests(root):
        cited.update(re.findall(r"observation/[\w./-]+", str(source or "")))
    found = []
    for heading, body in re.findall(r"(?ms)^## (observation/\S+)\n(.*?)(?=^## |\Z)", read(path, root)):
        date = re.search(r"(?m)^date: (\S+)", body)
        if heading not in cited and "observation/" + heading.rsplit("/", 1)[-1] not in cited:
            found.append((heading, date.group(1) if date else None))
    return found


def listing(root, as_json):
    requests = list(request_text.requests(root))
    seen = uncited(root)
    if as_json:
        print(json.dumps({"requests": [{"request": n, "status": s, "turn": t} for n, s, t, _ in requests],
                          "observations": [{"observation": o, "date": d} for o, d in seen]}))
        return 0
    for name, status, _, _ in requests:
        print("request %s %s" % (name, status))
    for observation, date in seen:
        print("observation %s %s" % (observation, date))
    return 0


def parts(root, name, turn):
    """What `work show <request>` prints after its first line: whose turn it is, each line with its line outcome,
    each question with its answer, the resolution."""
    found = request_moves.sections(root, name)
    issue = request_text.field(read(request_moves.path_of(root, name), root), "issue")
    print("it is the %s's turn" % turn + (", on %s" % issue if issue else ""))
    for number, text in sorted(found["Lines"].items(), key=lambda e: int(e[0])):
        print("  line %s: %s - %s" % (number, found["Outcomes"].get(number, "unsettled"), text))
    for number, text in sorted(found["Questions"].items(), key=lambda e: int(e[0])):
        print("  question %s: %s" % (number, text))
        if number in found["Answers"]:
            print("  answer %s: %s" % (number, found["Answers"][number]))
    for number, text in sorted(found["Resolution"].items(), key=lambda e: int(e[0])):
        print("  resolution line %s: %s" % (number, text))


def show(root, name, as_json):
    """Print where the request `name` stands; return the exit status. Anything else is refused, naming it."""
    for request, status, turn, _ in request_text.requests(root):
        if request == name:
            print(json.dumps({"request": name, "status": status, "turn": turn}) if as_json
                  else "%s %s %s" % (name, status, turn))
            if not as_json:
                parts(root, name, turn)
            return 0
    raise Refused("%s is no request, item or quote that work show shows" % name)
