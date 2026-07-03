import pathlib
import unittest


class CleanlinessTests(unittest.TestCase):
    def test_root_gitignore_ignores_python_cache(self):
        source = pathlib.Path(".gitignore").read_text(encoding="utf-8")

        self.assertIn("__pycache__/", source)
        self.assertIn("*.pyc", source)
        self.assertIn(".streamlit/secrets.toml", source)
        self.assertIn("venv/", source)

    def test_readme_exists_with_streamlit_setup_notes(self):
        source = pathlib.Path("README.md").read_text(encoding="utf-8")

        self.assertIn("Chekicha Timeline", source)
        self.assertIn("streamlit run app.py", source)
        self.assertIn("SUPABASE_URL", source)
        self.assertIn("SUPABASE_KEY", source)
        self.assertIn("ADMIN_PASSWORD", source)


if __name__ == "__main__":
    unittest.main()
