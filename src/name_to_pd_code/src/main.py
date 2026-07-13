"""Command-line interface for name_to_pd_code."""

import sys

try:
    from .get_knot_pd_code_by_name import get_knot_pd_code_by_name
except ImportError:  # Direct execution from the src directory.
    from get_knot_pd_code_by_name import get_knot_pd_code_by_name


def main() -> int:
    name = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not name:
        print("error: expected a knot name on standard input", file=sys.stderr)
        return 2
    try:
        print(get_knot_pd_code_by_name(name))
    except (FileNotFoundError, KeyError, TypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
