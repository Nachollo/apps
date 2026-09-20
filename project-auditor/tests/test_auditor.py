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


    def test_flags_decorative_ci(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "ci-demo"
            (root / "src").mkdir(parents=True)
            (root / ".github" / "workflows").mkdir(parents=True)
            for i in range(10):
                (root / "src" / f"m{i}.py").write_text("def f():\n    return 1\n", encoding="utf-8")
            (root / ".github" / "workflows" / "ci.yml").write_text(
                "jobs:\n  build:\n    steps:\n      - run: echo Hello, world!\n",
                encoding="utf-8",
            )
            r = auditor.inspect(root, str(root), run=False, install=False, timeout=10)
            self.assertTrue(any("CI decorativo" in x for x in r.blockers))

    def test_flags_unused_prominent_dependency(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "unused-ai"
            (root / "src").mkdir(parents=True)
            (root / "src" / "app.js").write_text("export const sum = (a,b) => a+b;", encoding="utf-8")
            (root / "package.json").write_text(
                '{"scripts":{"build":"echo ok"},"dependencies":{"@tensorflow/tfjs":"^4.0.0"}}',
                encoding="utf-8",
            )
            r = auditor.inspect(root, str(root), run=False, install=False, timeout=10)
            self.assertTrue(any("dependencias relevantes declaradas" in x for x in r.blockers))


    def test_flags_legacy_openai_api_with_v1_package(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td) / "openai-broken"
            root.mkdir()
            (root / "app.py").write_text(
                "import openai\nopenai.ChatCompletion.create(model='gpt-4', messages=[])\n",
                encoding="utf-8",
            )
            (root / "requirements.txt").write_text("openai==1.3.0\n", encoding="utf-8")
            r = auditor.inspect(root, str(root), run=False, install=False, timeout=10)
            self.assertTrue(any("OpenAI incompatible" in x for x in r.blockers))


if __name__ == "__main__":
    unittest.main()
