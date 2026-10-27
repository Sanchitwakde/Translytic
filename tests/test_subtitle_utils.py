import unittest

from subtitle_utils import format_time, to_srt, get_caption_at


class SubtitleUtilsTests(unittest.TestCase):
    def test_timestamp_format(self):
        self.assertEqual(format_time(0), "00:00:00,000")
        self.assertEqual(format_time(3661.25), "01:01:01,250")

    def test_timestamp_rounding_carries_into_next_second(self):
        self.assertEqual(format_time(59.9996), "00:01:00,000")

    def test_timestamp_rejects_negative_and_non_finite_values(self):
        for value in (-0.01, float("inf"), float("nan")):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    format_time(value)

    def test_srt_serialization(self):
        actual = to_srt([
            {"start": 0, "end": 1.25, "text": "Hello"},
            {"start": 1.5, "end": 2, "text": " नमस्ते "},
        ])
        self.assertEqual(
            actual,
            "1\n00:00:00,000 --> 00:00:01,250\nHello\n\n"
            "2\n00:00:01,500 --> 00:00:02,000\nनमस्ते\n\n",
        )

    def test_srt_rejects_reversed_timestamps(self):
        with self.assertRaises(ValueError):
            to_srt([{"start": 2, "end": 1, "text": "bad"}])

    def test_srt_empty_list(self):
        self.assertEqual(to_srt([]), "")

    def test_caption_lookup(self):
        segments = [
            {"start": 0, "end": 1, "text": "first"},
            {"start": 2, "end": 3, "text": "second"},
        ]
        self.assertEqual(get_caption_at(segments, 0.5), "first")
        self.assertEqual(get_caption_at(segments, 2.5), "second")
        self.assertEqual(get_caption_at(segments, 1.5), "")
        self.assertEqual(get_caption_at(segments, 4.0), "")
        self.assertEqual(get_caption_at([], 0.5), "")


if __name__ == "__main__":
    unittest.main()
