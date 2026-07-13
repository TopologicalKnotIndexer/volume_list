"""Convert a canonically labelled oriented knot PD code to signed DT code."""

from ast import literal_eval
import sys

try:
    from .in_out_code import in_out_code
except ImportError:  # Direct execution from the src directory.
    from in_out_code import in_out_code


def _component_count(pd_code: list[list[int]]) -> int:
    adjacency: dict[int, set[int]] = {}
    for first, second, third, fourth in pd_code:
        for left, right in ((first, third), (second, fourth)):
            adjacency.setdefault(left, set()).add(right)
            adjacency.setdefault(right, set()).add(left)
    components = 0
    visited: set[int] = set()
    for start in adjacency:
        if start in visited:
            continue
        components += 1
        stack = [start]
        visited.add(start)
        while stack:
            for neighbor in adjacency[stack.pop()]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
    return components


def pd_code_to_dt_code(pd_code: list[list[int]]) -> tuple[int, ...]:
    """Return SnapPy-style signed Dowker-Thistlethwaite entries.

    Arc labels must be the canonical traversal numbers ``1..2n``. This API
    represents one knot component; use a link-aware DT codec for links.
    """

    states = in_out_code(pd_code)
    if not pd_code:
        return ()
    if _component_count(pd_code) != 1:
        raise ValueError("this DT tuple format requires a one-component knot")

    odd_to_signed_even: dict[int, int] = {}
    for crossing, incidence in zip(pd_code, states):
        under_in = crossing[0]
        over_in = crossing[1] if incidence[1] == "IN" else crossing[3]
        if (under_in - over_in) % 2 == 0:
            raise ValueError(
                f"crossing encounters must have opposite parity: {under_in}, {over_in}"
            )
        if under_in % 2 == 0:
            odd, signed_even = over_in, under_in
        else:
            odd, signed_even = under_in, -over_in
        if odd in odd_to_signed_even:
            raise ValueError(f"odd encounter {odd} appears at multiple crossings")
        odd_to_signed_even[odd] = signed_even

    expected_odds = set(range(1, 2 * len(pd_code), 2))
    expected_evens = set(range(2, 2 * len(pd_code) + 1, 2))
    if set(odd_to_signed_even) != expected_odds:
        raise ValueError("crossings do not pair every odd traversal encounter exactly once")
    if {abs(value) for value in odd_to_signed_even.values()} != expected_evens:
        raise ValueError("crossings do not pair every even traversal encounter exactly once")
    return tuple(odd_to_signed_even[odd] for odd in sorted(expected_odds))


def parse_pd_code(text: str) -> list[list[int]]:
    """Safely parse a PD-code literal; structural checks occur in conversion."""

    try:
        value = literal_eval(text)
    except (SyntaxError, ValueError) as exc:
        raise ValueError("input is not a Python literal representing a PD code") from exc
    if not isinstance(value, list):
        raise TypeError("a PD code must be a list")
    return value


def main() -> int:
    raw = sys.stdin.buffer.read().decode("utf-8-sig").strip()
    if not raw:
        print("error: expected a PD-code literal on standard input", file=sys.stderr)
        return 2
    try:
        print(pd_code_to_dt_code(parse_pd_code(raw)))
    except (TypeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
