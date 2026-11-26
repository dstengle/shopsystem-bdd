"""`work context keep <id>` and `work context list` (b576, shop r1-r5): the bounded contexts a shop keeps, each by its
context id, kept in `.shop/contexts.toml` (`contexts = [...]`, one id a line, in the order kept), which only `work
context keep` writes and commits. The shop's product id is the product path of this bounded context's id
(spec/index.md's id less `bounded-context/` and its last part, `missingmass.io/shopsystem`: `product_id`), and it
covers an id `bounded-context/<product id>/<name>` (`covers`). An id not in the context id form, one the product id
does not cover and one kept already are refused naming the id (`keep`). The listing prints each id kept, or, while the
shop keeps none, this bounded context's id alone (`listed`)."""
import tomllib
from pathlib import Path

import shop_files
from migrate_init import FORM
from shop_files import Refused

REL = ".shop/contexts.toml"
HEADER = "# The bounded contexts this shop keeps, each by its context id; written by `work context keep`.\n"


def this_id(root):
    """This bounded context's id, as spec/index.md gives it."""
    return "bounded-context/" + shop_files.context_path(root)


def product_id(root):
    """The product id of the shop: this bounded context's id less `bounded-context/` and its last part."""
    return shop_files.context_path(root).rpartition("/")[0]


def covers(product, ident):
    return ident.startswith("bounded-context/%s/" % product) and len(ident) > len("bounded-context/%s/" % product)


def kept(root):
    """The ids of the bounded contexts the shop keeps, in the order kept (none with no file)."""
    path = Path(root) / REL
    if not path.is_file():
        return []
    try:
        found = tomllib.loads(path.read_text(encoding="utf-8")).get("contexts", [])
    except tomllib.TOMLDecodeError as why:
        raise Refused("%s: %s" % (REL, why)) from None
    if not isinstance(found, list) or not all(isinstance(i, str) for i in found):
        raise Refused("%s: contexts is a list of bounded context ids" % REL)
    return found


def render(ids):
    return HEADER + "contexts = [\n" + "".join('  "%s",\n' % i for i in ids) + "]\n"


def keep(root, ident):
    """The bounded context of `ident` kept in the shop and committed; refused, naming the id, when it is not in the
    context id form, its product is not the shop's, or the shop keeps one under it already."""
    names = ["id:%s" % ident]
    if not FORM.fullmatch(ident):
        raise Refused("{names} is not in the context id form bounded-context/<domain>/<path>",
                      reason="id not in the context id form", names=names)
    product = product_id(root)
    if not covers(product, ident):
        raise Refused("{names} is outside the product id %s of this shop" % product,
                      reason="id outside the product id", names=names)
    ids = kept(root)
    if ident in ids:
        raise Refused("{names} is kept already in this shop", reason="id kept already", names=names)
    path = Path(root) / REL
    shop_files.committed(root, [REL], "work context keep: %s" % ident,
                         lambda: (path.parent.mkdir(parents=True, exist_ok=True),
                                  path.write_text(render(ids + [ident]), encoding="utf-8")))
    print("kept %s" % ident)
    return 0


def listed(root):
    """The ids the shop keeps, else this bounded context's alone."""
    return kept(root) or [this_id(root)]


def cmd_context(args):
    if args.context_cmd == "keep":
        return keep(args.root, args.id)
    for ident in listed(args.root):
        print(ident)
    return 0


def add_parser(sub):
    p = sub.add_parser("context", help="the bounded contexts this shop keeps, each by its context id")
    cmds = p.add_subparsers(dest="context_cmd", required=True)
    k = cmds.add_parser("keep", help="keep a bounded context in this shop under its context id, and commit it")
    k.add_argument("id", help="the context id, bounded-context/<product id>/<name>")
    cmds.add_parser("list", help="print the id of each bounded context this shop keeps (this one's, while it keeps none)")


COMMANDS = {"context": cmd_context}
