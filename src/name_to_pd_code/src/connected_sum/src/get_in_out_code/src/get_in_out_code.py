"""Derive incoming and outgoing incidences for canonically labelled PD codes."""

from collections import Counter


def _successor(label: int, maximum: int) -> int:
    return 1 if label == maximum else label + 1


def _validate_canonical_pd_code(pd_code: list[list[int]]) -> int:
    if not isinstance(pd_code, list):
        raise TypeError("pd_code must be a list")

    labels: list[int] = []
    for crossing in pd_code:
        if not isinstance(crossing, list) or len(crossing) != 4:
            raise ValueError("every crossing must be a four-item list")
        for label in crossing:
            if isinstance(label, bool) or not isinstance(label, int):
                raise TypeError("arc labels must be integers")
            labels.append(label)

    maximum = 2 * len(pd_code)
    counts = Counter(labels)
    if set(counts) != set(range(1, maximum + 1)) or any(count != 2 for count in counts.values()):
        raise ValueError("labels must be exactly 1..2n and each label must occur twice")
    return maximum


def get_in_out_code(pd_code: list[list[int]]) -> list[list[str]]:
    """Return `IN`/`OUT` states for each incidence in a canonical PD code.

    The first and third entries of each crossing follow the PD convention
    directly. The orientation of the second/fourth pair is determined by
    which label is the cyclic successor of the other.
    """

    maximum = _validate_canonical_pd_code(pd_code)
    states: list[list[str]] = []
    for _, second, _, fourth in pd_code:
        if second == _successor(fourth, maximum):
            states.append(["IN", "OUT", "OUT", "IN"])
        elif fourth == _successor(second, maximum):
            states.append(["IN", "IN", "OUT", "OUT"])
        else:
            raise ValueError("the second and fourth labels must be consecutive along the oriented component")
    return states


if __name__ == "__main__":
    print(get_in_out_code([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]))
