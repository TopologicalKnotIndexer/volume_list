"""Compute numerical or certified hyperbolic knot-complement volume."""

import math
import sys

from to_dt_code import to_dt_code


EPS = 1e-5


class SnapPyUnavailableError(RuntimeError):
    """Raised when neither a system nor compatible bundled SnapPy is usable."""


class NonHyperbolicError(RuntimeError):
    """Raised when SnapPy does not find or certify a hyperbolic structure."""


def _load_snappy():
    try:
        import snappy  # type: ignore

        return snappy
    except (ImportError, OSError) as system_error:
        if sys.platform.startswith("linux") and sys.version_info[:2] == (3, 12):
            try:
                from portable_snappy import snappy  # type: ignore

                return snappy
            except (ImportError, OSError) as bundled_error:
                raise SnapPyUnavailableError(
                    f"system SnapPy failed ({system_error}); bundled Linux CPython 3.12 "
                    f"SnapPy failed ({bundled_error})"
                ) from bundled_error
        raise SnapPyUnavailableError(
            "SnapPy is not installed for this interpreter, and the bundled fallback "
            "supports only Linux CPython 3.12"
        ) from system_error


def _dt_specification(pd_code: list[list[int]]) -> str:
    return f"DT:[{to_dt_code(pd_code)!r}]"


def raw_get_volume(
    pd_code: list[list[int]],
    *,
    snappy_module=None,
    verified: bool = False,
    bits_prec: int = 80,
) -> float:
    """Return a positive hyperbolic volume or raise ``NonHyperbolicError``.

    ``verified=True`` requires SnapPy running inside SageMath and certifies the
    hyperbolic structure before requesting an interval-certified volume.
    """

    if isinstance(bits_prec, bool) or not isinstance(bits_prec, int) or bits_prec < 20:
        raise ValueError("bits_prec must be an integer of at least 20")
    backend = snappy_module if snappy_module is not None else _load_snappy()
    manifold = backend.Manifold(_dt_specification(pd_code))

    if verified:
        success, _ = manifold.verify_hyperbolicity(bits_prec=bits_prec)
        if not success:
            raise NonHyperbolicError("SnapPy could not certify hyperbolicity")
        value = float(manifold.volume(verified=True, bits_prec=bits_prec))
    else:
        manifold = manifold.with_hyperbolic_structure()
        solution_type = manifold.solution_type(enum=True)
        if solution_type != 1:
            raise NonHyperbolicError(
                f"SnapPy did not find a geometric solution (solution type {solution_type})"
            )
        value = float(manifold.volume())

    if not math.isfinite(value):
        raise RuntimeError(f"SnapPy returned a non-finite volume: {value!r}")
    if value < -EPS:
        raise RuntimeError(f"SnapPy returned a negative volume: {value!r}")
    if abs(value) <= EPS:
        raise NonHyperbolicError("the computed hyperbolic volume is zero")
    return value


def get_volume(
    pd_code: list[list[int]],
    *,
    snappy_module=None,
    verified: bool = False,
    bits_prec: int = 80,
) -> float:
    """Return the hyperbolic volume, or ``0.0`` for a non-hyperbolic result.

    Invalid input, unavailable dependencies, and backend failures are not
    converted to zero; callers receive the original explicit exception.
    """

    try:
        return raw_get_volume(
            pd_code,
            snappy_module=snappy_module,
            verified=verified,
            bits_prec=bits_prec,
        )
    except NonHyperbolicError:
        return 0.0


if __name__ == "__main__":
    print(get_volume([[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]))
