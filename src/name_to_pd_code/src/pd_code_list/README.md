# PD-code list

A compact table of standard planar-diagram codes for the unknot and 801
prime-knot representatives with at most 11 crossings, considered without a
separate mirror entry.

## Data format

`data/pd_code_list.txt` contains 802 records:

```text
[KNOT_NAME|[[a, b, c, d], ...]]
```

`K0a1` is represented by the empty PD code `[]`. Each nonempty crossing has
four integer arc labels. The file provides one usable diagram per listed name;
it is not a claim that the diagram is unique or crossing-minimal after every
downstream transformation.

## Scope

- Mirror-prefixed names are not listed separately.
- Composite knots are not included.
- Consumers that need mirrors must apply a PD-code mirror operation.
- Consumers that need composites must construct connected sums explicitly.

## Example

```python
from ast import literal_eval
from pathlib import Path

line = Path("data/pd_code_list.txt").read_text(encoding="utf-8").splitlines()[1]
name, raw_pd = line[1:-1].split("|", 1)
pd_code = literal_eval(raw_pd)
print(name, len(pd_code))
```

This repository is a data artifact and has no runtime dependency.

