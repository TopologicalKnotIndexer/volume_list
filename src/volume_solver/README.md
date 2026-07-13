# volume_solver

Convert an oriented one-component knot PD code to signed DT code and compute
the hyperbolic volume of its complement with SnapPy.

The repository is independently cloneable and contains its organization-owned
DT converter as regular tracked source rather than a Git submodule. SnapPy is a
native external dependency. A legacy SnapPy 3.1.1 fallback is committed for
Linux CPython 3.12 only; other platforms must provide a compatible `snappy`
installation. This maintenance task does not install or publish Python
packages.

## Requirements

- Python 3.10 or newer
- SnapPy for the active interpreter
- SageMath only when certified computation is requested

See the [official SnapPy Manifold documentation](https://snappy.computop.org/manifold.html)
for `solution_type()`, `verify_hyperbolicity()`, and `volume()` semantics.

## Command-line usage

```bash
echo '[[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]' | python src/main.py
```

The command prints a positive floating-point volume when SnapPy finds a
geometric solution. It prints `0.0` when no geometric hyperbolic solution is
found. Invalid PD codes, missing/incompatible SnapPy, and backend failures are
reported as errors with exit status 2; they are never silently converted to
zero.

Certified mode must run in an interpreter with SageMath support:

```bash
python src/main.py --verified --bits-prec 100
```

## Python API

```python
from volume_solver import get_volume, raw_get_volume
from reliable_volume_solver import get_volume_safe

approximate = get_volume(pd_code)
certified = raw_get_volume(pd_code, verified=True, bits_prec=100)
isolated = get_volume_safe(pd_code, timeout=15)
```

`raw_get_volume()` raises `NonHyperbolicError` when no geometric/certified
structure is available. `get_volume()` converts only that condition to `0.0`.
Input errors, dependency errors, NaN/infinite results, and negative volumes
remain explicit exceptions. `get_volume_safe()` runs the CLI in a child process
and enforces a hard timeout without shell parsing or timer threads.

## Algorithm and limitations

The bundled converter validates canonical labels, one-component topology,
encounter parity, and complete DT pairing. SnapPy constructs the manifold from
`DT:[(...)]`. Approximate mode accepts only solution type 1 (`all tetrahedra
positively oriented`); certified mode calls `verify_hyperbolicity()` before
requesting `volume(verified=True)`.

Floating-point approximate mode is evidence of a geometric solution, not a
formal proof. Use certified mode when mathematical certification is required.
No code dynamically loads former submodules or modifies `sys.path`.

## Development

Tests inject a deterministic fake SnapPy backend, so dependency and error
contracts can be verified on unsupported platforms:

```bash
python -m unittest discover -s tests -v
```

No PyPI publication is performed as part of repository maintenance.
