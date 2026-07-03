import unittest
import pathlib

from utils import styles


class StylesModuleTests(unittest.TestCase):
    def test_exposes_dark_theme_css_constant(self):
        self.assertTrue(hasattr(styles, "DARK_THEME_CSS"))
        self.assertEqual(styles.DARK_THEME_CSS, styles.DARK_CSS)

    def test_exposes_page_helper_aliases(self):
        self.assertTrue(hasattr(styles, "initials_avatar"))
        self.assertTrue(hasattr(styles, "tag"))
        self.assertTrue(hasattr(styles, "team_badge"))
        self.assertIs(styles.initials_avatar, styles.initials_html)
        self.assertIs(styles.tag, styles.make_tag)
        self.assertIs(styles.team_badge, styles.make_team_badge)

    def test_exposes_archive_design_helpers(self):
        self.assertTrue(hasattr(styles, "ARCHIVE_THEME_CSS"))
        self.assertTrue(hasattr(styles, "safe_text"))
        self.assertTrue(hasattr(styles, "format_event_date"))
        self.assertTrue(hasattr(styles, "format_event_time"))
        self.assertTrue(hasattr(styles, "render_event_chip"))
        self.assertTrue(hasattr(styles, "render_status_chip"))
        self.assertTrue(hasattr(styles, "render_avatar_markup"))

    def test_archive_theme_uses_consistent_banner_containment(self):
        self.assertIn("object-fit: contain", styles.ARCHIVE_THEME_CSS)
        self.assertIn("padding: 14px", styles.ARCHIVE_THEME_CSS)
        self.assertIn(".ckt-timeline-columns", styles.ARCHIVE_THEME_CSS)
        self.assertIn("grid-template-columns: repeat(2, minmax(0, 1fr))", styles.ARCHIVE_THEME_CSS)
        self.assertIn(".ckt-member-pair", styles.ARCHIVE_THEME_CSS)
        self.assertIn(".ckt-member-pill", styles.ARCHIVE_THEME_CSS)
        self.assertIn("text-overflow: ellipsis", styles.ARCHIVE_THEME_CSS)
        self.assertIn("white-space: nowrap", styles.ARCHIVE_THEME_CSS)

    def test_navbar_brand_and_credit_links_exist(self):
        source = pathlib.Path("utils/styles.py").read_text(encoding="utf-8")

        self.assertIn("Chekicha Timeline", source)
        self.assertIn("Every roulette draw, remembered.", source)
        self.assertIn("https://x.com/estrellawin19", source)
        self.assertIn("https://tako.id/Sportagame19Win", source)
        self.assertIn("ct-tako-btn", source)


if __name__ == "__main__":
    unittest.main()
