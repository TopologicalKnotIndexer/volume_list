"""Resolve prime knot names to the bundled canonical PD-code catalog."""

from ast import literal_eval
from collections import Counter
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
import re


SOURCE_DIR = Path(__file__).resolve().parent
PDCODE_FILE = SOURCE_DIR / "pd_code_list" / "data" / "pd_code_list.txt"
NMIRROR_FILE = SOURCE_DIR / "need_mirror.txt"
_PRIME_NAME = re.compile(r"^(m?)K(\d+)([an])(\d+)$", re.IGNORECASE)


def _parse_prime_name(name: str) -> tuple[bool, str]:
    if not isinstance(name, str):
        raise TypeError("a prime knot name must be a string")
    match = _PRIME_NAME.fullmatch(name.strip())
    if not match:
        raise ValueError(f"invalid prime knot name: {name!r}")
    mirror, crossings, family, index = match.groups()
    return bool(mirror), f"K{crossings}{family.lower()}{index}"


def _validate_pd_code(value: object, *, line_number: int) -> list[list[int]]:
    if not isinstance(value, list):
        raise ValueError(f"catalog line {line_number}: PD code must be a list")
    labels: list[int] = []
    for crossing in value:
        if not isinstance(crossing, list) or len(crossing) != 4:
            raise ValueError(f"catalog line {line_number}: malformed crossing")
        if any(isinstance(label, bool) or not isinstance(label, int) for label in crossing):
            raise ValueError(f"catalog line {line_number}: labels must be integers")
        labels.extend(crossing)
    counts = Counter(labels)
    expected = set(range(1, 2 * len(value) + 1))
    if set(counts) != expected or any(count != 2 for count in counts.values()):
        raise ValueError(f"catalog line {line_number}: labels must be 1..2n and occur twice")
    return value


@lru_cache(maxsize=1)
def load_prime_catalog() -> dict[str, list[list[int]]]:
    """Load, safely parse, and validate the committed prime-knot catalog."""

    if not PDCODE_FILE.is_file():
        raise FileNotFoundError(PDCODE_FILE)
    catalog: dict[str, list[list[int]]] = {}
    for line_number, raw_line in enumerate(
        PDCODE_FILE.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if not (line.startswith("[") and line.endswith("]") and "|" in line):
            raise ValueError(f"catalog line {line_number}: expected [KNOT_NAME|PD_CODE]")
        raw_name, raw_code = line[1:-1].split("|", 1)
        mirror, name = _parse_prime_name(raw_name)
        if mirror:
            raise ValueError(f"catalog line {line_number}: base names cannot be mirrored")
        if name in catalog:
            raise ValueError(f"catalog line {line_number}: duplicate name {name}")
        try:
            parsed = literal_eval(raw_code.strip())
        except (SyntaxError, ValueError) as exc:
            raise ValueError(f"catalog line {line_number}: invalid PD-code literal") from exc
        catalog[name] = _validate_pd_code(parsed, line_number=line_number)
    return catalog


@lru_cache(maxsize=1)
def _need_mirror_names() -> frozenset[str]:
    if not NMIRROR_FILE.is_file():
        raise FileNotFoundError(NMIRROR_FILE)
    names: set[str] = set()
    for line_number, raw_line in enumerate(
        NMIRROR_FILE.read_text(encoding="utf-8-sig").splitlines(), start=1
    ):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        mirror, name = _parse_prime_name(line)
        if mirror:
            raise ValueError(f"need_mirror line {line_number}: unexpected mirror prefix")
        names.add(name)
    missing = names - set(load_prime_catalog())
    if missing:
        raise ValueError(f"need_mirror contains names missing from the catalog: {sorted(missing)}")
    return frozenset(names)


def mirror_pd_code(pd_code: list[list[int]]) -> list[list[int]]:
    """Return the planar mirror of a PD code."""

    return [[first, fourth, third, second] for first, second, third, fourth in pd_code]


def is_neg_writhe_knot(basename: str) -> bool:
    """Return whether the organization convention toggles this base diagram."""

    mirror, canonical = _parse_prime_name(basename)
    if mirror:
        raise ValueError("basename must not contain a mirror prefix")
    return canonical in _need_mirror_names()


def get_prime_knot_pd_code_by_name(knotname: str) -> list[list[int]]:
    """Return an independent PD-code copy for a prime knot or its mirror."""

    requested_mirror, basename = _parse_prime_name(knotname)
    catalog = load_prime_catalog()
    if basename not in catalog:
        raise KeyError(f"knot is not present in the bundled catalog: {basename}")
    pd_code = deepcopy(catalog[basename])
    if requested_mirror ^ (basename in _need_mirror_names()):
        pd_code = mirror_pd_code(pd_code)
    return pd_code


if __name__ == "__main__":
    print(get_prime_knot_pd_code_by_name("K7a7"))
