# get-in-out-code

Derive the incoming and outgoing direction of every crossing incidence in a
canonically labelled oriented PD code.

## Input convention

For a code with `n` crossings, labels must be the integers `1` through `2n`,
each appearing exactly twice. Consecutive labels follow the component
orientation, with `2n` followed cyclically by `1`. Each crossing is a
four-item list in the PD convention used throughout this organization.

Inputs that merely satisfy the weak “twice per label” rule but do not use this
canonical numbering are rejected instead of producing guessed directions.

## Usage

```python
from src.get_in_out_code import get_in_out_code

trefoil = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
print(get_in_out_code(trefoil))
```

The output has the same shape as the PD code and contains only `"IN"` and
`"OUT"`. The function does not mutate its input.

## Algorithm

The first and third incidence states are fixed by the local PD convention.
For the second and fourth entries, the algorithm checks which label is the
cyclic successor of the other. Explicit validation prevents the former
fallback behavior from silently assigning a direction when neither ordering
was valid.

## Development

Only Python 3.10 or newer and the standard library are required. Run:

```bash
python -m unittest discover -s tests -v
```

