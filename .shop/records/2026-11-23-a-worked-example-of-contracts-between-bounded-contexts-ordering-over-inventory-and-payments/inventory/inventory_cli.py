"""The inventory service's command line, a stand-in for the example: its argparse only, which spec check reads."""
import argparse


def main(argv=None):
    top = argparse.ArgumentParser(prog="inventory")
    top.add_argument("--root")
    top.add_argument("--json", action="store_true")
    sub = top.add_subparsers(dest="command", required=True)
    for name, arg in (("hold", "product"), ("release", "allocation"), ("consume", "allocation"),
                      ("query", "product"), ("lapse", "allocation"), ("restock", "product"),
                      ("transfer", "product"), ("audit", "warehouse")):
        p = sub.add_parser(name)
        p.add_argument(arg)
        if name in ("hold", "restock", "transfer"):
            p.add_argument("--quantity")
        if name in ("hold", "restock", "transfer"):
            p.add_argument("--warehouse")
        if name == "hold":
            p.add_argument("--reference")
    return top.parse_args(argv)


if __name__ == "__main__":
    main()
