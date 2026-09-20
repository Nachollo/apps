import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import auditor


class AuditorTests(unittest.TestCase):
    def test_detects_demo_as_weak(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "demo"
            root.mkdir()
            (root / "index.html").write_text("<html>Demo local - coming soon placeholder</html>", encoding="utf-8")
            (root / "app.js").write_text("const fakeData = []; // mocked demo", encoding="utf-8")
            (root / "README.md").write_text("100% funcional. 145/145 tests passing", encoding="utf-8")
            r = auditor.inspect(root, str(root), run=False, install=False, timeout=10)
            self.assertLess(r.score, 30)
            self.assertEqual(r.verdict, "PAJA / CLAIMS NO ACREDITADAS")
            self.assertGreater(r.mock_hits, 0)
            self.assertTrue(r.readme_claims)

    def test_detects_real_structure_better(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "real"
            (root / "src").mkdir(parents=True)
            (root / "tests").mkdir()
            for i in range(12):
                (root / "src" / f"m{i}.py").write_text(
                    "def f(x):\n    return x + 1\n" * 30, encoding="utf-8"
                )
            for i in range(5):
                (root / "tests" / f"test_{i}.py").write_text("def test_ok():\n    assert 1 + 1 == 2\n", encoding="utf-8")
            (root / "requirements.txt").write_text("pytest\nfastapi\nsqlalchemy\n", encoding="utf-8")
            (root / "README.md").write_text("Aplicación real", encoding="utf-8")
            r = auditor.inspect(root, str(root), run=False, install=False, timeout=10)
            self.assertGreaterEqual(r.score, 45)
            self.assertGreaterEqual(r.test_files, 5)
            self.assertGreaterEqual(r.source_files, 10)


if __name__ == "__main__":
    unittest.main()
