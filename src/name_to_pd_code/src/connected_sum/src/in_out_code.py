"""Derive incidence directions for canonically labelled PD codes."""

from collections import Counter


def _successor(label: int, maximum: int) -> int:
    return 1 if label == maximum else label + 1


def in_out_code(pd_code: list[list[int]]) -> list[list[str]]:
    """Return the ``IN``/``OUT`` state of every crossing incidence.

    Labels must be the canonical contiguous range ``1..2n`` and each label
    must occur twice. The second/fourth pair is oriented by cyclic adjacency.
    """

    if not isinstance(pd_code, list):
        raise TypeError("pd_code must be a list")
    labels: list[int] = []
    for crossing in pd_code:
        if not isinstance(crossing, list) or len(crossing) != 4:
            raise ValueError("every crossing must be a four-item list")
        if any(isinstance(label, bool) or not isinstance(label, int) for label in crossing):
            raise TypeError("arc labels must be integers")
        labels.extend(crossing)

    maximum = 2 * len(pd_code)
    counts = Counter(labels)
    if set(counts) != set(range(1, maximum + 1)) or any(count != 2 for count in counts.values()):
        raise ValueError("labels must be exactly 1..2n and each label must occur twice")

    result: list[list[str]] = []
    for _, second, _, fourth in pd_code:
        if second == _successor(fourth, maximum):
            result.append(["IN", "OUT", "OUT", "IN"])
        elif fourth == _successor(second, maximum):
            result.append(["IN", "IN", "OUT", "OUT"])
        else:
            raise ValueError("the second and fourth labels must be consecutive along the component")
    return result
