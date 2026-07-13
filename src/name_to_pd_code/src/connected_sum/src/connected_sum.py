"""Compute a deterministic connected sum of two oriented knot PD codes."""

from copy import deepcopy

try:
    from .input_sanity import input_sanity
except ImportError:  # Direct execution from the src directory.
    from input_sanity import input_sanity


def _labels(pd_code: list[list[int]]) -> list[int]:
    return sorted({label for crossing in pd_code for label in crossing})


def _canonical_cycle(component: set[int], adjacency: dict[int, set[int]]) -> list[int]:
    start = min(component)
    neighbors = sorted(adjacency[start])
    if len(component) == 2 and len(neighbors) == 1:
        return [start, neighbors[0]]
    if len(neighbors) != 2:
        raise ValueError("the PD component graph is not a cycle")

    candidates: list[list[int]] = []
    for first in neighbors:
        cycle = [start]
        previous, current = start, first
        while current != start:
            if current in cycle:
                raise ValueError("the PD component graph contains a short cycle")
            cycle.append(current)
            next_nodes = adjacency[current] - {previous}
            if len(next_nodes) != 1:
                raise ValueError("the PD component graph is not 2-regular")
            previous, current = current, next(iter(next_nodes))
        if len(cycle) != len(component):
            raise ValueError("the PD component graph is disconnected")
        candidates.append(cycle)
    return min(candidates)


def _pre_nxt(pd_code: list[list[int]]) -> tuple[dict[int, int], dict[int, int]]:
    adjacency: dict[int, set[int]] = {}
    for crossing in pd_code:
        for left, right in ((crossing[0], crossing[2]), (crossing[1], crossing[3])):
            adjacency.setdefault(left, set()).add(right)
            adjacency.setdefault(right, set()).add(left)

    pre: dict[int, int] = {}
    nxt: dict[int, int] = {}
    seen: set[int] = set()
    for start in _labels(pd_code):
        if start in seen:
            continue
        component: set[int] = set()
        stack = [start]
        while stack:
            node = stack.pop()
            if node in component:
                continue
            component.add(node)
            stack.extend(adjacency[node] - component)
        cycle = _canonical_cycle(component, adjacency)
        seen.update(component)
        for index, node in enumerate(cycle):
            pre[node] = cycle[index - 1]
            nxt[node] = cycle[(index + 1) % len(cycle)]
    return pre, nxt


def _normalize(pd_code: list[list[int]]) -> tuple[list[list[int]], dict[int, int]]:
    """Orient components deterministically and relabel them contiguously."""

    if not pd_code:
        return [], {}
    _, nxt = _pre_nxt(pd_code)
    old_to_new: dict[int, int] = {}
    next_label = 1
    for start in _labels(pd_code):
        if start in old_to_new:
            continue
        current = start
        while current not in old_to_new:
            old_to_new[current] = next_label
            next_label += 1
            current = nxt[current]

    normalized = [[old_to_new[label] for label in crossing] for crossing in pd_code]
    normalized_next = {old_to_new[label]: old_to_new[target] for label, target in nxt.items()}
    for index, crossing in enumerate(normalized):
        if normalized_next[crossing[0]] == crossing[2]:
            continue
        if normalized_next[crossing[2]] == crossing[0]:
            normalized[index] = crossing[2:] + crossing[:2]
        else:
            raise ValueError("a crossing is inconsistent with the component orientation")
    normalized.sort()
    return normalized, old_to_new


def _endpoint(
    pd_code: list[list[int]], label: int, nxt: dict[int, int], pre: dict[int, int]
) -> tuple[int, int]:
    """Locate the crossing incidence immediately after the selected arc."""

    slots = [
        (row, column)
        for row, crossing in enumerate(pd_code)
        for column, value in enumerate(crossing)
        if value == label
    ]
    if len(slots) != 2:
        raise ValueError("a connected-sum label must occur exactly twice")
    if nxt[label] == pre[label]:
        return slots[1]
    target = nxt[label]
    for row, column in slots:
        if pd_code[row][(column + 2) % 4] == target:
            return row, column
    raise ValueError("could not locate the oriented endpoint of the selected arc")


def connected_sum(
    pd_code1: str | list[list[int]], pd_code2: str | list[list[int]]
) -> list[list[int]]:
    """Return a canonical PD code for the connected sum of two oriented knots.

    The component containing the smallest label in each input is selected. For
    the intended knot inputs this is the unique component. Empty PD codes are
    treated as the unknot. Caller-owned lists are never mutated.
    """

    first_input = input_sanity(pd_code1)
    second_input = input_sanity(pd_code2)
    if not first_input or not second_input:
        return _normalize(deepcopy(first_input or second_input))[0]

    first, _ = _normalize(first_input)
    second_base, _ = _normalize(second_input)
    offset = 2 * len(first)
    second = [[label + offset for label in crossing] for crossing in second_base]

    first_label = min(_labels(first))
    second_label = min(_labels(second))
    pre_first, nxt_first = _pre_nxt(first)
    pre_second, nxt_second = _pre_nxt(second)
    first_row, first_column = _endpoint(first, first_label, nxt_first, pre_first)
    second_row, second_column = _endpoint(second, second_label, nxt_second, pre_second)

    first[first_row][first_column] = second_label
    second[second_row][second_column] = first_label
    return _normalize(first + second)[0]


if __name__ == "__main__":
    trefoil = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
    print(connected_sum(trefoil, trefoil))
