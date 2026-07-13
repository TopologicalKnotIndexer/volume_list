"""Command-line interface for connected_sum."""

import sys

from connected_sum import connected_sum


def main() -> int:
    """Read two PD codes from standard input and print their connected sum."""

    first = sys.stdin.readline()
    second = sys.stdin.readline()
    if not first or not second:
        print("expected two input lines containing PD codes", file=sys.stderr)
        return 2
    try:
        print(connected_sum(first, second))
    except (TypeError, ValueError) as exc:
        print(f"invalid input: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
