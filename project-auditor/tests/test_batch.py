import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import batch


class BatchTests(unittest.TestCase):
    def test_resolves_alias_folder(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            p = base / "sentinel-app"
            p.mkdir()
            item = {"name": "SENTINEL", "aliases": ["sentinel"]}
            self.assertEqual(batch.resolve_project(base, item), p.resolve())

    def test_ambiguous_partial_returns_none(self):
        with tempfile.TemporaryDirectory() as td:
            base = Path(td)
            (base / "reservia-old").mkdir()
            (base / "reservia-new").mkdir()
            item = {"name": "ReservIA", "aliases": ["reservia"]}
            self.assertIsNone(batch.resolve_project(base, item))


if __name__ == "__main__":
    unittest.main()
