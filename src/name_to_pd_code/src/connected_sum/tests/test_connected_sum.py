from copy import deepcopy
from pathlib import Path
import subprocess
import sys
import unittest


SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))

from connected_sum import connected_sum  # noqa: E402
from in_out_code import in_out_code  # noqa: E402
from input_sanity import input_sanity  # noqa: E402


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


def assert_structural_pd(test_case: unittest.TestCase, pd_code: list[list[int]]) -> None:
    flat = [label for crossing in pd_code for label in crossing]
    test_case.assertEqual(set(flat), set(range(1, 2 * len(pd_code) + 1)))
    test_case.assertTrue(all(flat.count(label) == 2 for label in set(flat)))


class ConnectedSumTests(unittest.TestCase):
    def test_trefoil_sum_has_six_crossings_and_valid_labels(self):
        left = deepcopy(TREFOIL)
        right = deepcopy(TREFOIL)
        result = connected_sum(left, right)
        self.assertEqual(len(result), 6)
        assert_structural_pd(self, result)
        self.assertEqual(left, TREFOIL)
        self.assertEqual(right, TREFOIL)

    def test_negative_sparse_labels_cannot_collide(self):
        mapping = {1: -30, 2: 90, 3: -10, 4: 70, 5: 20, 6: 50}
        relabelled = [[mapping[label] for label in crossing] for crossing in TREFOIL]
        result = connected_sum(relabelled, relabelled)
        self.assertEqual(len(result), 6)
        assert_structural_pd(self, result)

    def test_unknot_is_identity(self):
        result = connected_sum([], TREFOIL)
        self.assertEqual(len(result), 3)
        assert_structural_pd(self, result)

    def test_rejects_code_execution(self):
        with self.assertRaisesRegex(ValueError, "Python literal"):
            connected_sum("__import__('os').getcwd()", "[]")

    def test_incidence_helper_validates_canonical_labels(self):
        self.assertEqual(len(in_out_code(TREFOIL)), 3)
        with self.assertRaisesRegex(ValueError, "1..2n"):
            in_out_code([[10, 20, 20, 10]])

    def test_input_sanity_returns_a_copy(self):
        source = deepcopy(TREFOIL)
        parsed = input_sanity(source)
        parsed[0][0] = 99
        self.assertEqual(source, TREFOIL)

    def test_cli_requires_two_lines(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="[]\n",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("expected two input lines", completed.stderr)


if __name__ == "__main__":
    unittest.main()
