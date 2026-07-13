# name_to_pd_code

Resolve a Hoste-Thistlethwaite-style prime or composite knot name to a
canonical planar diagram (PD) code from the TopologicalKnotIndexer catalog.

The repository is independently cloneable and requires only Python 3.10 or
newer. Catalog and connected-sum sources are regular tracked files rather than
Git submodules; runtime imports are static.

## Supported names

A prime name has the form `[m]K<c>a<i>` or `[m]K<c>n<i>`, such as `K7a7` or
`mK8n2`. Input is case-insensitive. The optional leading `m` requests the
mirror. Composite knots are comma-separated prime factors:

```text
K3a1,mK3a1,K4a1
```

All base factors must occur in the bundled 802-entry `pd_code_list` catalog.
`K0a1` represents the unknot and is an identity factor.

## Command-line usage

```bash
echo 'K3a1,mK3a1' | python src/main.py
```

The PD code is written to standard output. Invalid names, missing catalog
entries, and corrupt data produce diagnostics and exit status 2.

## Python API

```python
from get_knot_pd_code_by_name import get_knot_pd_code_by_name
from get_prime_knot_pd_code_by_name import get_prime_knot_pd_code_by_name

trefoil = get_prime_knot_pd_code_by_name("K3a1")
composite = get_knot_pd_code_by_name("K3a1,mK3a1")
```

Every call returns new lists; modifying a result cannot alter cached catalog
data.

## Data and algorithm

The catalog is decoded as UTF-8, parsed with `ast.literal_eval`, and completely
validated once per process. Every PD label must be the contiguous range
`1..2n` and occur exactly twice. The historical `need_mirror.txt` table toggles
the base diagram where the organization's naming convention differs from the
source tabulation. A requested leading `m` toggles it again.

Composite factors are combined left-to-right with the bundled deterministic
connected-sum implementation. That implementation normalizes labels before
offsetting, cuts oriented arcs, glues their endpoints crosswise, and performs a
final canonical renumbering.

See `VENDORED_DEPENDENCIES.md` for audited source revisions. No runtime code
modifies `sys.path` or invokes Git submodule commands.

## Development

```bash
python -m unittest discover -s tests -v
```

No PyPI publication is performed as part of repository maintenance.
