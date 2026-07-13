"""Static compatibility wrapper for the bundled connected-sum algorithm."""

try:
    from .connected_sum.src.connected_sum import connected_sum
except ImportError:  # Direct execution from the src directory.
    from connected_sum.src.connected_sum import connected_sum


def solve_connected_sum(
    pd_code1: list[list[int]], pd_code2: list[list[int]]
) -> list[list[int]]:
    """Return the connected sum without mutating either input."""

    return connected_sum(pd_code1, pd_code2)
