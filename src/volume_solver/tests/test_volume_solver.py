from pathlib import Path
from unittest.mock import patch
import builtins
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from reliable_volume_solver import get_volume_safe, run  # noqa: E402
from to_dt_code import to_dt_code  # noqa: E402
from volume_solver import (  # noqa: E402
    NonHyperbolicError,
    SnapPyUnavailableError,
    _dt_specification,
    _load_snappy,
    get_volume,
    raw_get_volume,
)


TREFOIL = [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]]


class FakeManifold:
    def __init__(self, specification, *, solution=1, volume=2.0298832128, verified=True):
        self.specification = specification
        self._solution = solution
        self._volume = volume
        self._verified = verified
        self.volume_calls = []

    def with_hyperbolic_structure(self):
        return self

    def solution_type(self, enum=False):
        return self._solution if enum else "fake"

    def verify_hyperbolicity(self, bits_prec=None):
        return self._verified, ["interval"] if self._verified else []

    def volume(self, **kwargs):
        self.volume_calls.append(kwargs)
        return self._volume


class FakeSnapPy:
    def __init__(self, **manifold_options):
        self.options = manifold_options
        self.created = []

    def Manifold(self, specification):
        manifold = FakeManifold(specification, **self.options)
        self.created.append(manifold)
        return manifold


class VolumeSolverTests(unittest.TestCase):
    def test_static_dt_conversion_and_specification(self):
        self.assertEqual(to_dt_code(TREFOIL), (-4, -6, -2))
        self.assertEqual(_dt_specification(TREFOIL), "DT:[(-4, -6, -2)]")

    def test_approximate_geometric_volume(self):
        backend = FakeSnapPy(volume=2.0298832128)
        self.assertAlmostEqual(raw_get_volume(TREFOIL, snappy_module=backend), 2.0298832128)
        self.assertEqual(backend.created[0].solution_type(enum=True), 1)

    def test_nongeometric_result_is_zero_only_through_public_wrapper(self):
        backend = FakeSnapPy(solution=4, volume=999.0)
        with self.assertRaises(NonHyperbolicError):
            raw_get_volume(TREFOIL, snappy_module=backend)
        self.assertEqual(get_volume(TREFOIL, snappy_module=backend), 0.0)

    def test_certified_mode_verifies_before_volume(self):
        backend = FakeSnapPy(verified=True, volume=2.0298832128)
        result = raw_get_volume(TREFOIL, snappy_module=backend, verified=True, bits_prec=100)
        self.assertAlmostEqual(result, 2.0298832128)
        self.assertEqual(backend.created[0].volume_calls, [{"verified": True, "bits_prec": 100}])
        failing = FakeSnapPy(verified=False)
        self.assertEqual(get_volume(TREFOIL, snappy_module=failing, verified=True), 0.0)

    def test_invalid_numeric_results_are_not_silenced(self):
        for value in (float("nan"), float("inf"), -1.0):
            with self.subTest(value=value), self.assertRaises(RuntimeError):
                get_volume(TREFOIL, snappy_module=FakeSnapPy(volume=value))

    def test_incompatible_environment_reports_dependency(self):
        real_import = builtins.__import__

        def import_without_snappy(name, *args, **kwargs):
            if name == "snappy":
                raise ImportError("simulated missing SnapPy")
            return real_import(name, *args, **kwargs)

        with (
            patch("builtins.__import__", side_effect=import_without_snappy),
            patch("volume_solver.sys.platform", "win32"),
            self.assertRaises(SnapPyUnavailableError),
        ):
            _load_snappy()

    def test_isolated_runner_contract(self):
        completed = subprocess.CompletedProcess(
            args=["python"], returncode=0, stdout="2.5\n", stderr=""
        )
        with patch("reliable_volume_solver.subprocess.run", return_value=completed) as invoked:
            self.assertEqual(get_volume_safe(TREFOIL, timeout=7, python_path="custom-python"), 2.5)
        command = invoked.call_args.args[0]
        self.assertEqual(command[0], "custom-python")
        self.assertEqual(invoked.call_args.kwargs["input"], repr(TREFOIL))
        self.assertEqual(invoked.call_args.kwargs["timeout"], 7)

    def test_isolated_runner_rejects_failure_and_bad_output(self):
        with patch(
            "reliable_volume_solver.subprocess.run",
            return_value=subprocess.CompletedProcess([], 2, "", "backend missing"),
        ):
            with self.assertRaisesRegex(RuntimeError, "backend missing"):
                get_volume_safe(TREFOIL)
        with patch(
            "reliable_volume_solver.subprocess.run",
            return_value=subprocess.CompletedProcess([], 0, "not-a-number", ""),
        ):
            with self.assertRaisesRegex(RuntimeError, "invalid output"):
                get_volume_safe(TREFOIL)

    def test_cli_input_is_safe_before_backend_loading(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "main.py")],
            input="__import__('os').getcwd()",
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 2)
        self.assertIn("malformed node", completed.stderr)


if __name__ == "__main__":
    unittest.main()
