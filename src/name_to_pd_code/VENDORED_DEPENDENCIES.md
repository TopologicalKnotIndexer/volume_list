# Vendored dependencies

This repository is self-contained. Former Git submodules are tracked as regular files at the audited commits below. Their original directory layout is preserved so runtime imports and entry points remain compatible.

| Path | Source | Pinned commit |
| --- | --- | --- |
| `src/pd_code_list` | [pd_code_list](https://github.com/TopologicalKnotIndexer/pd_code_list) | `130b0cf0e531c4ab88328578cb8a90392a58baee` |
| `src/connected_sum` | [connected_sum](https://github.com/TopologicalKnotIndexer/connected_sum) | `be88f69ca180905cc29f7ac2fac919fbcb4756f7` |
| `src/connected_sum/src/pd_code_input_sanity` | [pd_code_input_sanity](https://github.com/TopologicalKnotIndexer/pd_code_input_sanity) | `9f0233a3b48043a9e164d98ad6cee644cc792a28` |
| `src/connected_sum/src/get_in_out_code` | [get_in_out_code](https://github.com/TopologicalKnotIndexer/get_in_out_code) | `62f331dac998d55d3f38dd6e1fd22468738f1468` |

## Updating a vendored dependency

Replace the listed tree from a reviewed source commit, update this table, and run this repository's complete validation suite. Do not reintroduce Git submodules; every organization project must remain independently cloneable.
