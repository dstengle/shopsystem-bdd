"""The response envelope (the domain contract design, §5.4): one shape every operation answers with, on every port.

`Response(outcome, content, errors, notices)`: the outcome one of the domain's (`DOMAIN`: done, returned, refused,
passed, failed) or `broken`, a failure of the infrastructure, outside the domain and never stated by a line; the
content the domain object or list the operation gives; each error `{reason, names}`, a refusal's or a failure's
business reason and the things it names by business reference (`parameter:tier`, `item:b12`); each notice what
completed but should be said (`{reason: "not shared", names: ["shared store"]}`). Errors are given exactly when the
outcome is refused, failed or broken. Its JSON (`json`, `read`) is the adapters' serialisation of it."""
import json
from dataclasses import dataclass, field

DOMAIN = ("done", "returned", "refused", "passed", "failed")
OUTCOMES = DOMAIN + ("broken",)
ERRING = ("refused", "failed", "broken")


@dataclass
class Response:
    outcome: str
    content: object = None
    errors: list = field(default_factory=list)
    notices: list = field(default_factory=list)

    def __post_init__(self):
        if self.outcome not in OUTCOMES:
            raise ValueError("no outcome %r: one of %s" % (self.outcome, ", ".join(OUTCOMES)))
        if bool(self.errors) != (self.outcome in ERRING):
            raise ValueError("a response %s has %s" % (self.outcome, "errors" if self.errors else "no errors"))
        for entry in self.errors + self.notices:
            if set(entry) != {"reason", "names"}:
                raise ValueError("an error or a notice is {reason, names}, not %r" % (entry,))

    def as_dict(self):
        return {"outcome": self.outcome, "content": self.content, "errors": [dict(e) for e in self.errors],
                "notices": [dict(n) for n in self.notices]}

    def json(self):
        return json.dumps(self.as_dict(), indent=2, sort_keys=False)


def error(reason, names=()):
    return {"reason": str(reason), "names": list(names)}


def refused(why):
    """The response of a `shop_refused.Refused`: its reason and names."""
    return Response("refused", errors=[error(why.reason or str(why), getattr(why, "names", []))])


def broken(exc):
    """The response of a failure outside the domain: what broke, naming nothing."""
    return Response("broken", errors=[error(str(exc) or type(exc).__name__)])


def read(text):
    """A response read back from its JSON."""
    data = json.loads(text)
    return Response(data["outcome"], data.get("content"), data.get("errors") or [], data.get("notices") or [])
