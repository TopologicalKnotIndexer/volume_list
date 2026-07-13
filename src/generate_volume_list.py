"""Regenerate the volume catalog from prime-knot computations."""

from decimal import Decimal
from pathlib import Path
import argparse
import os
import tempfile

from get_volume import get_volume
from name_to_pd_code import name_to_pd_code
from volume_catalog import CATALOG_PATH, load_names, render_catalog


def compute_records(
    names: list[str],
    *,
    resolve=name_to_pd_code,
    compute_volume=get_volume,
    timeout: float = 15.0,
    python_path: str | os.PathLike[str] | None = None,
    verified: bool = False,
    bits_prec: int = 80,
) -> dict[str, Decimal]:
    """Compute prime values once, mirror them, and add composite factors."""

    records: dict[str, Decimal] = {}
    base_names = [name for name in names if "," not in name and not name.startswith("m")]
    for name in base_names:
        pd_code = resolve(name)
        value = compute_volume(
            pd_code,
            timeout=timeout,
            python_path=python_path,
            verified=verified,
            bits_prec=bits_prec,
        )
        records[name] = Decimal(str(value))
    for name in names:
        if "," not in name and name.startswith("m"):
            records[name] = records[name[1:]]
    for name in names:
        if "," in name:
            records[name] = sum((records[factor] for factor in name.split(",")), Decimal(0))
    return records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Regenerate volume_info_list.txt atomically.")
    parser.add_argument("--output", type=Path, default=CATALOG_PATH)
    parser.add_argument("--timeout", type=float, default=15.0)
    parser.add_argument("--python", dest="python_path")
    parser.add_argument("--verified", action="store_true")
    parser.add_argument("--bits-prec", type=int, default=80)
    args = parser.parse_args(argv)
    names = load_names()
    records = compute_records(
        names,
        timeout=args.timeout,
        python_path=args.python_path,
        verified=args.verified,
        bits_prec=args.bits_prec,
    )
    rendered = render_catalog(names, records)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(
        prefix=args.output.name + ".", suffix=".tmp", dir=args.output.parent
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(rendered)
        os.replace(temporary, args.output)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise
    print(f"wrote {len(names)} records to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
