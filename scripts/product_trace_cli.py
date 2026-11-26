"""`spec trace <job>` (b644, product r26-r30): the product service's trace requested on the command line, over
product_trace: each requirement of the job's trace by its id with why it is in the trace and its text, then each
adapter spec by its id with why, printed as text, the whole trace the content of a `returned` response (the envelope
under `--json`). A job no requirement group serves is refused naming it."""
import product_trace
from domain_envelope import Response


def text(found):
    lines = ["the trace of the job %s:" % found["job"]]
    lines += ["  %s (%s): %s" % (r["id"], r["why"], r["text"]) for r in found["requirements"]]
    lines += ["  adapter spec %s (%s)" % (a["id"], a["why"]) for a in found["adapter specs"]]
    return "\n".join(lines) + "\n"


def cmd_trace(args):
    found = product_trace.trace(args.root, args.job)
    if not args.json:
        print(text(found), end="")
    return Response("returned", found)


def add_parser(sub):
    t = sub.add_parser("trace", help="print the requirements and adapter specs a job of the product rests on")
    t.add_argument("job", help="the job's id")


COMMANDS = {"trace": cmd_trace}
