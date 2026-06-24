import os
import sys
import unittest
import re

# Set up paths so we can import src.translations
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))

from src.translations import STRINGS, t


class TestTranslations(unittest.TestCase):
    def test_strings_structure(self):
        """Verify that every entry in STRINGS has exactly 'en' and 'km' keys."""
        for key, translations in STRINGS.items():
            with self.subTest(key=key):
                self.assertIsInstance(
                    translations, dict, f"Translation for '{key}' is not a dict"
                )
                self.assertIn("en", translations, f"Missing English translation for '{key}'")
                self.assertIn("km", translations, f"Missing Khmer translation for '{key}'")
                self.assertIsInstance(
                    translations["en"], str, f"English translation for '{key}' is not a string"
                )
                self.assertIsInstance(
                    translations["km"], str, f"Khmer translation for '{key}' is not a string"
                )

    def test_placeholder_alignment(self):
        """Ensure that English and Khmer translations contain the exact same curly brace placeholders (except language-specific pluralization)."""
        placeholder_regex = re.compile(r"\{(\w+)\}")
        for key, translations in STRINGS.items():
            with self.subTest(key=key):
                en_placeholders = set(placeholder_regex.findall(translations["en"]))
                km_placeholders = set(placeholder_regex.findall(translations["km"]))
                diff = en_placeholders.symmetric_difference(km_placeholders)
                diff.discard("plural")
                self.assertEqual(
                    len(diff),
                    0,
                    f"Placeholder mismatch for '{key}': en has {en_placeholders}, km has {km_placeholders}"
                )

    def test_translation_function_basic(self):
        """Test the lookup and formatting capabilities of the t() helper function."""
        # Test basic lookup
        self.assertEqual(t("btn_homework", "en"), "📚  Homework")
        self.assertEqual(t("btn_homework", "km"), "📚  កិច្ចការផ្ទះ")

        # Test fallback to English for unsupported languages
        self.assertEqual(t("btn_homework", "fr"), "📚  Homework")

        # Test fallback for missing key (should return key string itself)
        self.assertEqual(t("non_existent_key_999", "en"), "non_existent_key_999")

    def test_translation_formatting(self):
        """Test that string interpolation functions correctly and handles parameters."""
        # menu_welcome_back has: en: "👋 *Welcome back, {name}!*\n..."
        rendered_en = t("menu_welcome_back", "en", name="John", code="GRADE-10", date="2026-06-20")
        self.assertIn("John", rendered_en)
        self.assertIn("GRADE-10", rendered_en)
        self.assertIn("2026-06-20", rendered_en)

        rendered_km = t("menu_welcome_back", "km", name="John", code="GRADE-10", date="2026-06-20")
        self.assertIn("John", rendered_km)
        self.assertIn("GRADE-10", rendered_km)
        self.assertIn("2026-06-20", rendered_km)


if __name__ == "__main__":
    unittest.main()
