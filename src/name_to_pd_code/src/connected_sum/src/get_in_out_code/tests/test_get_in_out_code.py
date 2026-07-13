import unittest

from src.get_in_out_code import get_in_out_code


class GetInOutCodeTests(unittest.TestCase):
    def test_trefoil_orientation(self):
        trefoil = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
        self.assertEqual(
            get_in_out_code(trefoil),
            [["IN", "OUT", "OUT", "IN"]] * 3,
        )

    def test_opposite_overstrand_orientation(self):
        mirrored = [[1, 4, 2, 5], [3, 6, 4, 1], [5, 2, 6, 3]]
        self.assertEqual(
            get_in_out_code(mirrored),
            [["IN", "IN", "OUT", "OUT"]] * 3,
        )

    def test_empty_code(self):
        self.assertEqual(get_in_out_code([]), [])

    def test_rejects_noncanonical_or_malformed_labels(self):
        invalid = (
            [[1, 5, 2, 4], [3, 1, 4, 7], [5, 3, 7, 2]],
            [[1, 4, 2, 6], [3, 6, 4, 1], [5, 2, 5, 3]],
            [[True, 1, 2, 2]],
        )
        for pd_code in invalid:
            with self.subTest(pd_code=pd_code), self.assertRaises((TypeError, ValueError)):
                get_in_out_code(pd_code)


if __name__ == "__main__":
    unittest.main()
