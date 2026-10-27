import unittest
from unittest.mock import patch, MagicMock

from app import translate_segments


class TranslationTests(unittest.TestCase):
    def test_cancellation(self):
        with self.assertRaises(InterruptedError):
            translate_segments(
                [{"start": 0, "end": 1, "text": "hello"}],
                "hi", "Hindi",
                check_cancel=lambda: True
            )

    def test_empty_segments(self):
        self.assertEqual(translate_segments([], "hi", "Hindi"), [])

    @patch("app.OPENROUTER_API_KEY", "")
    @patch("app.GoogleTranslator")
    def test_fallback_to_google_translate(self, mock_gt_cls):
        mock_gt = MagicMock()
        mock_gt.translate.return_value = "नमस्ते"
        mock_gt_cls.return_value = mock_gt

        segments = [{"start": 0, "end": 1, "text": "hello"}]
        results = translate_segments(segments, "hi", "Hindi")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "नमस्ते")
        self.assertFalse(results[0]["translation_failed"])

    @patch("app.OPENROUTER_API_KEY", "")
    @patch("app.GoogleTranslator")
    def test_failed_translation_retains_source(self, mock_gt_cls):
        mock_gt = MagicMock()
        mock_gt.translate.side_effect = Exception("network down")
        mock_gt_cls.return_value = mock_gt

        segments = [{"start": 0, "end": 1, "text": "hello"}]
        results = translate_segments(segments, "hi", "Hindi")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["text"], "hello")
        self.assertTrue(results[0]["translation_failed"])
        self.assertIn("network down", results[0]["translation_error"])


if __name__ == "__main__":
    unittest.main()
