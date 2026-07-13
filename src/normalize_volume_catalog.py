"""Check or rewrite deterministic mirror/composite volume records."""

import argparse
import sys

from volume_catalog import (
    CATALOG_PATH,
    canonicalize_catalog,
    load_catalog,
    load_names,
    render_catalog,
)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Enforce mirror equality and connected-sum additivity in the volume catalog."
    )
    parser.add_argument("--write", action="store_true", help="rewrite the committed catalog")
    args = parser.parse_args(argv)
    names = load_names()
    order, current = load_catalog()
    if order != names:
        print("error: catalog order differs from combined_knot_name.txt", file=sys.stderr)
        return 2
    canonical = canonicalize_catalog(names, current)
    rendered = render_catalog(names, canonical)
    existing = CATALOG_PATH.read_text(encoding="utf-8-sig")
    if rendered == existing:
        print(f"catalog is canonical: {len(names)} records")
        return 0
    changed = sum(current[name] != canonical[name] for name in names)
    if not args.write:
        print(f"error: {changed} records require normalization", file=sys.stderr)
        return 1
    CATALOG_PATH.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"normalized {changed} of {len(names)} records")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
