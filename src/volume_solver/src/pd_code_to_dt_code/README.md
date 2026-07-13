# pd_code_to_dt_code

Convert a canonically labelled oriented knot planar diagram (PD) code to a
signed Dowker-Thistlethwaite (DT) tuple compatible with the convention used by
the organization's SnapPy volume pipeline.

The repository is independently cloneable. Its incidence-direction dependency
is stored as ordinary tracked source, not as a Git submodule, and runtime code
uses a static import.

## Input convention

For a diagram with `n` crossings:

- every crossing is a four-integer list;
- labels are exactly `1..2n` and each occurs twice;
- labels increase cyclically along the oriented knot traversal;
- the diagram contains exactly one component.

Noncanonical labels and multi-component links are rejected explicitly. A DT
tuple for a link needs component boundary data and cannot be represented by
this project's single tuple without ambiguity.

## Python API

```python
from pd_code_to_dt_code import pd_code_to_dt_code

trefoil = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
assert pd_code_to_dt_code(trefoil) == (-4, -6, -2)
```

The empty PD code represents the unknot and returns `()`.

## Command-line usage

```bash
echo '[[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]' | python src/pd_code_to_dt_code.py
```

The input is parsed with `ast.literal_eval`. Invalid input is written to
standard error and exits with status 2.

## Algorithm and sign convention

At every crossing, the first/third PD entries are the under-strand incidences.
The bundled incidence algorithm determines which of the second/fourth entries
is the incoming over-strand encounter. Each crossing therefore pairs one odd
traversal number with one even number. The even number is positive when its
encounter is on the under-strand and negative when the odd encounter is on the
under-strand. Results are ordered by odd encounters `1, 3, ..., 2n-1`.

The converter validates parity, uniqueness, complete odd/even pairing, and the
one-component invariant. It does not rely on `assert`, so validation remains
active under optimized Python.

## Development

```bash
python -m unittest discover -s tests -v
```

Run the bundled dependency tests from `src/get_in_out_code` when refreshing
its snapshot. See `VENDORED_DEPENDENCIES.md` for the audited revision. No PyPI
publication is performed as part of repository maintenance.
