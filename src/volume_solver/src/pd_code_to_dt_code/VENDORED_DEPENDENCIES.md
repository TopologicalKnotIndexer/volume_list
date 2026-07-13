# Vendored dependencies

This repository is self-contained. Former Git submodules are tracked as regular files at the audited commits below. Their original directory layout is preserved so runtime imports and entry points remain compatible.

| Path | Source | Pinned commit |
| --- | --- | --- |
| `src/get_in_out_code` | [get_in_out_code](https://github.com/TopologicalKnotIndexer/get_in_out_code) | `62f331dac998d55d3f38dd6e1fd22468738f1468` |

## Updating a vendored dependency

Replace the listed tree from a reviewed source commit, update this table, and run this repository's complete validation suite. Do not reintroduce Git submodules; every organization project must remain independently cloneable.
