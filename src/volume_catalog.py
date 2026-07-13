"""Parse, validate, and canonicalize the committed volume catalog."""

from decimal import Decimal, InvalidOperation
from pathlib import Path
import re


SOURCE_DIR = Path(__file__).resolve().parent
NAME_PATH = SOURCE_DIR / "combined_knot_name.txt"
CATALOG_PATH = SOURCE_DIR / "volume_info_list.txt"
_PRIME = re.compile(r"^m?K\d+[an]\d+$")
_QUANTUM = Decimal("0.00000000000000000001")


def load_names(path: Path = NAME_PATH) -> list[str]:
    """Load and validate the ordered catalog name list."""

    names: list[str] = []
    seen: set[str] = set()
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        factors = line.split(",")
        if any(not _PRIME.fullmatch(factor) for factor in factors):
            raise ValueError(f"name line {line_number}: invalid knot name {line!r}")
        if line in seen:
            raise ValueError(f"name line {line_number}: duplicate knot name {line}")
        seen.add(line)
        names.append(line)
    return names


def load_catalog(path: Path = CATALOG_PATH) -> tuple[list[str], dict[str, Decimal]]:
    """Load ordered ``[KNOT_NAME|VOLUME]`` records as exact decimals."""

    order: list[str] = []
    records: dict[str, Decimal] = {}
    for line_number, raw_line in enumerate(
        path.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not (line.startswith("[") and line.endswith("]") and "|" in line):
            raise ValueError(f"catalog line {line_number}: expected [KNOT_NAME|VOLUME]")
        name, raw_value = line[1:-1].split("|", 1)
        if name in records:
            raise ValueError(f"catalog line {line_number}: duplicate knot name {name}")
        try:
            value = Decimal(raw_value)
        except InvalidOperation as exc:
            raise ValueError(f"catalog line {line_number}: invalid decimal {raw_value!r}") from exc
        if not value.is_finite() or value < 0:
            raise ValueError(f"catalog line {line_number}: volume must be finite and nonnegative")
        order.append(name)
        records[name] = value
    return order, records


def canonicalize_catalog(
    names: list[str], records: dict[str, Decimal]
) -> dict[str, Decimal]:
    """Enforce mirror equality and connected-sum additivity."""

    if set(names) != set(records) or len(names) != len(records):
        missing = sorted(set(names) - set(records))
        extra = sorted(set(records) - set(names))
        raise ValueError(f"catalog/name mismatch: missing={missing}, extra={extra}")

    canonical: dict[str, Decimal] = {}
    for name in names:
        if "," not in name and not name.startswith("m"):
            canonical[name] = records[name].quantize(_QUANTUM)
    for name in names:
        if "," not in name and name.startswith("m"):
            base = name[1:]
            if base not in canonical:
                raise ValueError(f"mirror entry has no base entry: {name}")
            canonical[name] = canonical[base]
    for name in names:
        if "," not in name:
            continue
        factors = name.split(",")
        missing = [factor for factor in factors if factor not in canonical]
        if missing:
            raise ValueError(f"composite {name} has missing prime factors: {missing}")
        canonical[name] = sum((canonical[factor] for factor in factors), Decimal(0)).quantize(
            _QUANTUM
        )
    return canonical


def render_catalog(names: list[str], records: dict[str, Decimal]) -> str:
    """Render records with exactly twenty decimal places."""

    return "".join(f"[{name}|{records[name]:.20f}]\n" for name in names)
