from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from pd_code_to_dt_code import parse_pd_code, pd_code_to_dt_code  # noqa: E402


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]
ELEVEN_CROSSING = [
    [4, 1, 5, 2], [15, 1, 16, 22], [10, 4, 11, 3], [2, 12, 3, 11],
    [9, 16, 10, 17], [7, 18, 8, 19], [17, 8, 18, 9], [19, 12, 20, 13],
    [5, 15, 6, 14], [13, 20, 14, 21], [21, 6, 22, 7],
]


class DtConversionTests(unittest.TestCase):
    def test_known_examples(self):
        self.assertEqual(pd_code_to_dt_code(TREFOIL), (-4, -6, -2))
        self.assertEqual(
            pd_code_to_dt_code(ELEVEN_CROSSING),
            (4, 10, -14, -18, -16, 2, -20, -22, -8, -12, -6),
        )
        self.assertEqual(pd_code_to_dt_code([]), ())

    def test_rejects_noncanonical_and_multi_component_codes(self):
        with self.assertRaisesRegex(ValueError, "1..2n"):
            pd_code_to_dt_code([[10, 20, 20, 10]])
        with self.assertRaisesRegex(ValueError, "one-component"):
            pd_code_to_dt_code([[1, 2, 2, 1], [3, 4, 4, 3]])

    def test_safe_parser(self):
        self.assertEqual(parse_pd_code(str(TREFOIL)), TREFOIL)
        with self.assertRaisesRegex(ValueError, "Python literal"):
            parse_pd_code("__import__('os').getcwd()")

    def test_cli_success_and_failure(self):
        success = subprocess.run(
            [sys.executable, str(SRC / "pd_code_to_dt_code.py")],
            input=str(TREFOIL),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(success.returncode, 0)
        self.assertEqual(success.stdout.strip(), "(-4, -6, -2)")
        failure = subprocess.run(
            [sys.executable, str(SRC / "pd_code_to_dt_code.py")],
            input="bad",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(failure.returncode, 2)
        self.assertIn("Python literal", failure.stderr)


if __name__ == "__main__":
    unittest.main()
