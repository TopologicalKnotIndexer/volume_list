"""Static wrapper for the bundled isolated volume runner."""

from os import PathLike

from volume_solver.src.reliable_volume_solver import get_volume_safe


def get_volume(
    knot_pdcode: list[list[int]],
    *,
    timeout: float = 15.0,
    python_path: str | PathLike[str] | None = None,
    verified: bool = False,
    bits_prec: int = 80,
) -> float:
    """Return a validated numeric geometric-decomposition volume."""

    return get_volume_safe(
        knot_pdcode,
        timeout=timeout,
        python_path=python_path,
        verified=verified,
        bits_prec=bits_prec,
    )
