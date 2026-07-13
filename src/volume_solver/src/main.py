"""Command-line interface for volume_solver."""

from ast import literal_eval
import argparse
import sys

from volume_solver import get_volume


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compute a knot complement's hyperbolic volume from a PD code."
    )
    parser.add_argument(
        "--verified",
        action="store_true",
        help="certify hyperbolicity and volume (requires SnapPy inside SageMath)",
    )
    parser.add_argument("--bits-prec", type=int, default=80, help="certified precision")
    args = parser.parse_args(argv)
    raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not raw:
        parser.exit(2, "error: expected a PD-code literal on standard input\n")
    try:
        pd_code = literal_eval(raw)
        if not isinstance(pd_code, list):
            raise TypeError("a PD code must be a list")
        print(get_volume(pd_code, verified=args.verified, bits_prec=args.bits_prec))
    except (ImportError, OSError, TypeError, ValueError, RuntimeError) as exc:
        parser.exit(2, f"error: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
