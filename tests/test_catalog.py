from decimal import Decimal
from pathlib import Path
from unittest.mock import Mock, patch
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from generate_volume_list import compute_records  # noqa: E402
from name_to_pd_code import name_to_pd_code  # noqa: E402
from volume_catalog import (  # noqa: E402
    canonicalize_catalog,
    load_catalog,
    load_names,
    render_catalog,
)


class VolumeCatalogTests(unittest.TestCase):
    def test_complete_catalog_is_canonical(self):
        names = load_names()
        order, records = load_catalog()
        self.assertEqual(len(names), 1871)
        self.assertEqual(order, names)
        canonical = canonicalize_catalog(names, records)
        self.assertEqual(records, canonical)
        self.assertEqual(render_catalog(names, records), (SRC / "volume_info_list.txt").read_text(encoding="utf-8"))

    def test_mirror_and_composite_invariants(self):
        names = load_names()
        _, records = load_catalog()
        mirror_pairs = 0
        composites = 0
        for name in names:
            if "," in name:
                composites += 1
                self.assertEqual(records[name], sum(records[x] for x in name.split(",")))
            elif name.startswith("m"):
                mirror_pairs += 1
                self.assertEqual(records[name], records[name[1:]])
        self.assertEqual(mirror_pairs, 801)
        self.assertEqual(composites, 268)

    def test_generation_computes_only_base_primes(self):
        names = ["K0a1", "K3a1", "mK3a1", "K3a1,mK3a1"]
        resolver = Mock(side_effect=lambda name: [] if name == "K0a1" else [[1, 2, 2, 1]])
        volumes = {"[]": 0.0, "[[1, 2, 2, 1]]": 2.5}

        def compute(code, **kwargs):
            return volumes[repr(code)]

        records = compute_records(names, resolve=resolver, compute_volume=compute)
        self.assertEqual(resolver.call_count, 2)
        self.assertEqual(records["K3a1"], Decimal("2.5"))
        self.assertEqual(records["mK3a1"], Decimal("2.5"))
        self.assertEqual(records["K3a1,mK3a1"], Decimal("5.0"))

    def test_bundled_name_resolver_end_to_end(self):
        self.assertEqual(
            name_to_pd_code("K3a1"),
            [[1, 5, 2, 4], [3, 1, 4, 6], [5, 3, 6, 2]],
        )

    def test_name_resolver_failure_is_not_silenced(self):
        completed = subprocess.CompletedProcess([], 2, "", "unknown knot")
        with patch("name_to_pd_code.subprocess.run", return_value=completed):
            with self.assertRaisesRegex(RuntimeError, "unknown knot"):
                name_to_pd_code("K99a1")

    def test_normalizer_cli_check(self):
        completed = subprocess.run(
            [sys.executable, str(SRC / "normalize_volume_catalog.py")],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertIn("1871 records", completed.stdout)


if __name__ == "__main__":
    unittest.main()
