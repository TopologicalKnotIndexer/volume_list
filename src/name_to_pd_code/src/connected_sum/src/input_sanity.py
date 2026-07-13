"""Safe parsing and weak structural validation for PD codes."""

from ast import literal_eval
from collections import Counter
from copy import deepcopy


def input_sanity(value: str | list[list[int]]) -> list[list[int]]:
    """Return a validated copy of *value* without executing input text.

    This validator checks the representation invariants used by the connected-
    sum algorithm. It does not claim that every accepted code has a planar
    realization.
    """

    if isinstance(value, str):
        try:
            parsed = literal_eval(value)
        except (SyntaxError, ValueError) as exc:
            raise ValueError("input is not a Python literal representing a PD code") from exc
    elif isinstance(value, list):
        parsed = deepcopy(value)
    else:
        raise TypeError("PD code input must be a string or a list")

    if not isinstance(parsed, list):
        raise TypeError("a PD code must be a list of crossings")

    labels: list[int] = []
    for crossing in parsed:
        if not isinstance(crossing, list):
            raise TypeError("every crossing must be a list")
        if len(crossing) != 4:
            raise ValueError("every crossing must contain exactly four labels")
        for label in crossing:
            if isinstance(label, bool) or not isinstance(label, int):
                raise TypeError("arc labels must be integers")
            labels.append(label)

    invalid = {label: count for label, count in Counter(labels).items() if count != 2}
    if invalid:
        details = ", ".join(f"{label}: {count}" for label, count in sorted(invalid.items()))
        raise ValueError(f"every arc label must occur exactly twice; observed {details}")
    return parsed


if __name__ == "__main__":
    print(input_sanity("[[1, 2, 2, 1]]"))
