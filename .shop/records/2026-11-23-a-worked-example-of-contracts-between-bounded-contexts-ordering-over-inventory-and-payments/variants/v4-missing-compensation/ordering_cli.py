"""The ordering service's command line, a stand-in for the example: its argparse only, which spec check reads."""
import argparse


def main(argv=None):
    top = argparse.ArgumentParser(prog="ordering")
    top.add_argument("--root")
    top.add_argument("--json", action="store_true")
    sub = top.add_subparsers(dest="command", required=True)
    place = sub.add_parser("place")
    place.add_argument("product")
    place.add_argument("--quantity")
    place.add_argument("--card")
    sub.add_parser("withdraw").add_argument("order")
    sub.add_parser("view").add_argument("product")
    return top.parse_args(argv)


if __name__ == "__main__":
    main()
