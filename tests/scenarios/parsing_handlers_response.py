"""parsing's Then of a response's request (r24, b543): read off the logical form `spec parse --form` printed of the
`response-request` line (design_model_check_worlds_response's REQUESTING), the response's request of an operation with
its parameters as the trigger's request is read (`request-params`): a `request(e, O, ...)` atom in the response part
with a `param` or `noparam` atom of its event."""
import re
import sys

W = sys.modules["shop_work_queue_world"]
REQUEST = re.compile(r"request\((e\d+), [a-z0-9_-]+\.[a-z0-9_-]+, ")


def response(form):
    """The lines of the response part of a printed logical form."""
    lines = form.splitlines()
    at = next((k for k, line in enumerate(lines) if line.strip() == "response"), len(lines))
    return "\n".join(lines[at + 1:])


@W.local("ThenDoes")
def uses(step):
    """The logical form l1 uses `request-params`: its response requests an operation with a parameter."""
    if sys.modules["vocab"].origin(step.request.node) != "parsing" or step.event != "use" \
            or not step.subject.startswith("the logical form") or step.nps[0] != "`request-params`":
        return False
    said = response(step.context["result"].stdout)
    events = REQUEST.findall(said)
    assert any(re.search(r"(no)?param\(%s, " % e, said) for e in events), ("no request with its parameters", said)
    return None
