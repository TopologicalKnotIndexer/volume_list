"""Resolve prime or composite knot names to PD codes."""

try:
    from .get_prime_knot_pd_code_by_name import (
        _parse_prime_name,
        get_prime_knot_pd_code_by_name,
    )
    from .solve_connected_sum import solve_connected_sum
except ImportError:  # Direct execution from the src directory.
    from get_prime_knot_pd_code_by_name import (
        _parse_prime_name,
        get_prime_knot_pd_code_by_name,
    )
    from solve_connected_sum import solve_connected_sum


def get_knot_pd_code_by_name(composite_knot_name: str) -> list[list[int]]:
    """Return the iterated connected-sum PD code for *composite_knot_name*."""

    if not isinstance(composite_knot_name, str):
        raise TypeError("a knot name must be a string")
    names = [name.strip() for name in composite_knot_name.split(",")]
    if not names or any(not name for name in names):
        raise ValueError("a composite name must contain non-empty prime names")
    for name in names:
        _parse_prime_name(name)

    result = get_prime_knot_pd_code_by_name(names[0])
    for name in names[1:]:
        result = solve_connected_sum(result, get_prime_knot_pd_code_by_name(name))
    return result


if __name__ == "__main__":
    print(get_knot_pd_code_by_name("K3a1,mK3a1"))
