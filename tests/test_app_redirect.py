import pathlib
import unittest


class AppRedirectTests(unittest.TestCase):
    def test_app_redirects_with_streamlit_navigation_api(self):
        app_source = pathlib.Path("app.py").read_text(encoding="utf-8")

        self.assertIn('st.switch_page("pages/1_📊_Overview.py")', app_source)
        self.assertNotIn("http-equiv=\"refresh\"", app_source)


if __name__ == "__main__":
    unittest.main()
