import unittest
from datetime import timezone

from ualf import parse_ualf, parse_ualf_line

SAMPLE = (
    "0 2025 08 15 12 54 11 233363712 64.2117 10.5121 25 0 18 33 "
    "117.17 0.23 0.11 0.97 16.8 14.6 2.8 0 1 0 1"
)


class TestParser(unittest.TestCase):
    def test_parse_line_happy_path(self):
        evt = parse_ualf_line(SAMPLE)
        self.assertEqual(evt.version, 0)
        self.assertEqual(evt.timestamp.year, 2025)
        self.assertEqual(evt.timestamp.tzinfo, timezone.utc)
        # nanoseconds truncated to microseconds
        self.assertEqual(evt.timestamp.microsecond, 233363)
        self.assertAlmostEqual(evt.lat, 64.2117)
        self.assertAlmostEqual(evt.lon, 10.5121)
        self.assertEqual(evt.peak_current, 25)
        self.assertEqual(evt.multiplicity, 0)
        self.assertEqual(evt.sensors, 18)
        self.assertEqual(evt.degrees_of_freedom, 33)
        self.assertAlmostEqual(evt.angle, 117.17)
        self.assertTrue(evt.angle_indicator)
        self.assertFalse(evt.cloud_indicator)
        self.assertFalse(evt.signal_indicator)
        self.assertTrue(evt.timing_indicator)

    def test_parse_line_invalid_token_count(self):
        with self.assertRaises(ValueError):
            parse_ualf_line("0 2025 08 15")

    def test_parse_batch_skips_comments_and_blank(self):
        text = "\n# comment\n" + SAMPLE + "\n"
        events = parse_ualf(text)
        self.assertEqual(len(events), 1)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
