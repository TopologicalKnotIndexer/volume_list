# Vendored dependencies

This repository is self-contained. Former Git submodules are tracked as regular files at the audited commits below. Their original directory layout is preserved so runtime imports and entry points remain compatible.

| Path | Source | Pinned commit |
| --- | --- | --- |
| `src/name_to_pd_code` | [name_to_pd_code](https://github.com/TopologicalKnotIndexer/name_to_pd_code) | `17dd932c7e2e521b83daf6b6c72516a45f390f37` |
| `src/name_to_pd_code/src/pd_code_list` | [pd_code_list](https://github.com/TopologicalKnotIndexer/pd_code_list) | `130b0cf0e531c4ab88328578cb8a90392a58baee` |
| `src/name_to_pd_code/src/connected_sum` | [connected_sum](https://github.com/TopologicalKnotIndexer/connected_sum) | `be88f69ca180905cc29f7ac2fac919fbcb4756f7` |
| `src/name_to_pd_code/src/connected_sum/src/pd_code_input_sanity` | [pd_code_input_sanity](https://github.com/TopologicalKnotIndexer/pd_code_input_sanity) | `9f0233a3b48043a9e164d98ad6cee644cc792a28` |
| `src/name_to_pd_code/src/connected_sum/src/get_in_out_code` | [get_in_out_code](https://github.com/TopologicalKnotIndexer/get_in_out_code) | `62f331dac998d55d3f38dd6e1fd22468738f1468` |
| `src/volume_solver` | [volume_solver](https://github.com/TopologicalKnotIndexer/volume_solver) | `dec150e7227e2349e38f57bdc2a0989358239d77` |
| `src/volume_solver/src/pd_code_to_dt_code` | [pd_code_to_dt_code](https://github.com/TopologicalKnotIndexer/pd_code_to_dt_code) | `1704c25d90253a4cb39d6d3c2ebf69096051d352` |
| `src/volume_solver/src/pd_code_to_dt_code/src/get_in_out_code` | [get_in_out_code](https://github.com/TopologicalKnotIndexer/get_in_out_code) | `62f331dac998d55d3f38dd6e1fd22468738f1468` |

## Updating a vendored dependency

Replace the listed tree from a reviewed source commit, update this table, and run this repository's complete validation suite. Do not reintroduce Git submodules; every organization project must remain independently cloneable.
