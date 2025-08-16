import unittest

try:
    from ualf import build_url, create_geojson_polygon  # type: ignore

    _HAS_CLIENT = True
except Exception:
    build_url = None  # type: ignore
    create_geojson_polygon = None  # type: ignore
    _HAS_CLIENT = False


@unittest.skipUnless(
    _HAS_CLIENT, "client helpers unavailable (requests/python-dotenv not installed)"
)
class TestClientURL(unittest.TestCase):
    def test_create_geojson_polygon(self):
        if create_geojson_polygon is None:
            self.skipTest(
                "client helpers unavailable (requests/python-dotenv not installed)"
            )
        lat_lon = (60.0, 10.0)
        poly = create_geojson_polygon(lat_lon, 1.0)
        self.assertIn("POLYGON((", poly)
        # Ensure lon/lat ordering
        self.assertTrue(poly.startswith("POLYGON((9.0 59.0, 11.0 59.0,"))

    def test_build_url_contains_params(self):
        if build_url is None:
            self.skipTest(
                "client helpers unavailable (requests/python-dotenv not installed)"
            )
        lat_lon = (60.0, 10.0)
        url = build_url(lat_lon, size=1.0, max_age="P1D", referencetime="latest")
        self.assertIn("referencetime=latest", url)
        self.assertIn("maxage=P1D", url)
        self.assertIn("POLYGON((", url)
        self.assertIn("maxage=P1D", url)
        self.assertIn("POLYGON((", url)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
