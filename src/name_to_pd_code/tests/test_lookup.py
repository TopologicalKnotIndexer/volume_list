from collections import Counter
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from get_knot_pd_code_by_name import get_knot_pd_code_by_name  # noqa: E402
from get_prime_knot_pd_code_by_name import (  # noqa: E402
    get_prime_knot_pd_code_by_name,
    load_prime_catalog,
    mirror_pd_code,
)


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


def assert_valid_pd(test_case: unittest.TestCase, pd_code: list[list[int]]) -> None:
    counts = Counter(label for crossing in pd_code for label in crossing)
    test_case.assertEqual(set(counts), set(range(1, 2 * len(pd_code) + 1)))
    test_case.assertTrue(all(count == 2 for count in counts.values()))


class NameLookupTests(unittest.TestCase):
    def test_catalog_is_complete_and_safe(self):
        catalog = load_prime_catalog()
        self.assertEqual(len(catalog), 802)
        self.assertEqual(catalog["K3a1"], TREFOIL)
        for name, pd_code in catalog.items():
            with self.subTest(name=name):
                assert_valid_pd(self, pd_code)

    def test_mirror_and_convention_table(self):
        self.assertEqual(
            get_prime_knot_pd_code_by_name("mK3a1"),
            mirror_pd_code(get_prime_knot_pd_code_by_name("K3a1")),
        )
        raw_k7a7 = load_prime_catalog()["K7a7"]
        self.assertEqual(get_prime_knot_pd_code_by_name("K7a7"), mirror_pd_code(raw_k7a7))
        self.assertEqual(get_prime_knot_pd_code_by_name("mK7a7"), raw_k7a7)

    def test_results_do_not_mutate_cached_catalog(self):
        result = get_prime_knot_pd_code_by_name("K3a1")
        result[0][0] = 999
        self.assertEqual(get_prime_knot_pd_code_by_name("K3a1"), TREFOIL)

    def test_composite_sum_and_unknot_identity(self):
        composite = get_knot_pd_code_by_name("K3a1,mK3a1")
        self.assertEqual(len(composite), 6)
        assert_valid_pd(self, composite)
        self.assertEqual(get_knot_pd_code_by_name("K0a1,K3a1"), TREFOIL)

    def test_invalid_and_missing_names_are_explicit(self):
        for name in ("", "K3x1", "K3a1,", "not-a-knot"):
            with self.subTest(name=name), self.assertRaises((TypeError, ValueError)):
                get_knot_pd_code_by_name(name)
        with self.assertRaises(KeyError):
            get_knot_pd_code_by_name("K99a1")

    def test_cli(self):
        success = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="K3a1",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(success.returncode, 0)
        self.assertEqual(success.stdout.strip(), str(TREFOIL))
        failure = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="bad",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(failure.returncode, 2)
        self.assertIn("invalid prime knot name", failure.stderr)


if __name__ == "__main__":
    unittest.main()
