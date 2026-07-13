# connected_sum

Compute a deterministic connected sum of two oriented knot PD codes. The
repository is self-contained and does not require Git submodules or external
Python packages.

## Requirements

- Python 3.10 or newer

## Usage

Run the command-line program and provide one Python-literal PD code on each of
two input lines:

```bash
python src/main.py
```

Example input:

```text
[[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
[[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
```

The result is printed as a canonically oriented, contiguously labelled PD code.
The library API is also available from `src/connected_sum.py`:

```python
from connected_sum import connected_sum

result = connected_sum(left_pd_code, right_pd_code)
```

## Algorithm

Each input is safely parsed and checked for four-entry crossings, integer arc
labels, and exactly two occurrences of every label. The component cycles are
then reconstructed from opposite incidences, oriented deterministically, and
renumbered before the second input is offset. The algorithm cuts one oriented
arc in each knot, glues the two pairs of endpoints crosswise, and performs a
final canonical renumbering.

Normalizing before applying the offset is important: directly offsetting raw
negative or sparse labels can cause collisions. Empty PD codes represent the
unknot and act as the identity. The function returns new lists and does not
mutate its inputs.

For multi-component links, the component containing the smallest label in each
input is selected. This repository is primarily intended for knots.

## Development

Run the complete test suite with:

```bash
python -m unittest discover -s tests -v
```

The source snapshots under `src/get_in_out_code` and
`src/pd_code_input_sanity` are regular tracked files retained for provenance;
runtime code no longer performs dynamic submodule-style imports. See
`VENDORED_DEPENDENCIES.md` for the audited source commits.

No PyPI publication is performed as part of repository maintenance.
