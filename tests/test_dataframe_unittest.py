import unittest

from ualf import parse_ualf_line, to_dataframe

SAMPLE = (
    "0 2025 08 15 12 54 11 233363712 64.2117 10.5121 25 0 18 33 "
    "117.17 0.23 0.11 0.97 16.8 14.6 2.8 0 1 0 1"
)


class TestDataFrame(unittest.TestCase):
    def test_to_dataframe_type(self):
        evt = parse_ualf_line(SAMPLE)
        result = to_dataframe([evt])
        # If pandas is installed, result should look like a DataFrame
        if hasattr(result, "columns"):
            cols = list(result.columns)  # type: ignore[attr-defined]
            self.assertIn("lat", cols)
        else:
            # Without pandas, we return a list of dicts
            if isinstance(result, list) and result:
                self.assertIsInstance(result[0], dict)
            else:
                # Fallback shape check
                self.fail("Unexpected result type when pandas is unavailable")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
