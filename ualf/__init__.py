__version__ = "0.1.1"

from .parser import Lightning, parse_ualf, parse_ualf_line, to_dataframe

# Client is optional; allow import even if requests/dotenv not yet installed
try:
    from .client import (
        build_url,
        create_geojson_polygon,
        fetch_lightning_events,
        fetch_lightning_ualf,
    )

    __all__ = [
        "__version__",
        "Lightning",
        "parse_ualf_line",
        "parse_ualf",
        "to_dataframe",
        "fetch_lightning_ualf",
        "fetch_lightning_events",
        "create_geojson_polygon",
        "build_url",
    ]
except Exception:  # pragma: no cover - optional dependency path
    __all__ = [
        "__version__",
        "Lightning",
        "parse_ualf_line",
        "parse_ualf",
        "to_dataframe",
    ]
