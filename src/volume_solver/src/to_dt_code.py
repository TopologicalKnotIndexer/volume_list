"""Static compatibility wrapper for the bundled PD-to-DT converter."""

from pd_code_to_dt_code.src.pd_code_to_dt_code import pd_code_to_dt_code


def to_dt_code(pd_code: list[list[int]]) -> tuple[int, ...]:
    """Return the validated signed DT tuple of a one-component knot."""

    return pd_code_to_dt_code(pd_code)
