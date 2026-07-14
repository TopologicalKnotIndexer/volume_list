# volume_list

A 1,871-record catalog of numerical geometric-decomposition volumes for the
prime, mirror, and composite knots used by TopologicalKnotIndexer.

For a hyperbolic prime knot, the value is its knot-complement hyperbolic volume.
For a non-hyperbolic prime knot, the value is `0`. For a composite knot, this
catalog uses the additive sum of the hyperbolic pieces of its prime factors.
This is why a composite containing a hyperbolic factor can have a positive
entry even though the composite complement itself is not hyperbolic.

## Files and format

- `src/combined_knot_name.txt` contains 1,871 names in catalog order.
- `src/volume_info_list.txt` contains one matching volume record per name.

Every record has the form:

```text
[KNOT_NAME|NONNEGATIVE_DECIMAL]
```

Values have twenty digits after the decimal point. Mirror pairs are stored with
exactly equal decimals because volume is orientation-insensitive. Composite
entries are exact decimal sums of the committed prime entries. Prime values
remain numerical SnapPy results and are not claimed to be certified unless the
catalog is regenerated in verified SageMath mode.

## Validation and normalization

Check all names, records, mirror pairs, and additive composite values:

```bash
python src/normalize_volume_catalog.py
```

Use `--write` to perform the deterministic normalization. This does not call
SnapPy and does not change base prime measurements.

## Regeneration

Full regeneration computes each of the 802 base prime diagrams once, copies
each value to its mirror, and obtains all 268 composite values by addition:

```bash
python src/generate_volume_list.py --timeout 30
```

Certified mode requires a Python interpreter with SnapPy and SageMath:

```bash
python src/generate_volume_list.py --verified --bits-prec 100
```

Output is written atomically only after every computation succeeds. Missing
SnapPy, invalid diagrams, timeouts, and backend failures are explicit errors;
they are not converted to zero or partial files.

## Independent repository layout

The name resolver and volume solver are regular tracked source trees. Runtime
code uses fixed local programs or static imports and never changes `sys.path`
or invokes Git submodule commands. See `VENDORED_DEPENDENCIES.md` for audited
source revisions.

## Development

```bash
python -m unittest discover -s tests -v
```

No Python packages are installed or published by repository maintenance.

## Citation

If you use this repository in academic work, please cite it as:

```bibtex
@software{topologicalknotindexer_volume_list,
  author = {{TopologicalKnotIndexer contributors}},
  title = {{volume\_list}},
  year = {2026},
  url = {https://github.com/TopologicalKnotIndexer/volume_list}
}
```
