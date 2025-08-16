from __future__ import annotations

import os
from typing import List, Optional, Tuple

import requests
from dotenv import load_dotenv

from .parser import Lightning, parse_ualf

FROST_LIGHTNING_URL = "https://frost.met.no/lightning/v0.ualf"


def _ensure_env_loaded() -> None:
    """Load environment variables from a .env file if present."""
    load_dotenv(override=False)


def get_credentials(explicit_client_id: Optional[str] = None) -> Tuple[str, str]:
    """Get credentials for the Frost API.

    Args:
        explicit_client_id: Optional explicit client ID to use instead of environment

    Returns:
        Tuple of (client_id, client_secret)

    Raises:
        RuntimeError: If no client ID is available from env or parameters
    """
    _ensure_env_loaded()
    client_id = explicit_client_id or os.getenv("FROST_CLIENT_ID")
    client_secret = ""
    if not client_id:
        raise RuntimeError(
            "FROST_CLIENT_ID is not set. Either put it in a .env file as FROST_CLIENT_ID=... "
            "or provide it via the --client-id parameter."
        )
    return client_id, client_secret


def create_geojson_polygon(lat_lon: Tuple[float, float], size: float) -> str:
    """Create a GeoJSON polygon from latitude/longitude and size."""
    lat, lon = lat_lon
    return (
        f"POLYGON(({lon-size} {lat-size}, {lon+size} {lat-size}, "
        f"{lon+size} {lat+size}, {lon-size} {lat+size}, {lon-size} {lat-size}))"
    )


def build_url(
    lat_lon: Tuple[float, float],
    size: float,
    max_age: str,
    referencetime: str = "latest",
) -> str:
    geojson = create_geojson_polygon(lat_lon, size)
    return (
        f"{FROST_LIGHTNING_URL}?referencetime={referencetime}"
        f"&geometry={geojson}&maxage={max_age}"
    )


def fetch_lightning_ualf(
    lat_lon: Tuple[float, float],
    *,
    size: float = 1.0,
    max_age: str = "P1D",
    referencetime: str = "latest",
    session: Optional[requests.Session] = None,
    client_id: Optional[str] = None,
) -> str:
    url = build_url(lat_lon, size, max_age, referencetime)
    api_client_id, client_secret = get_credentials(client_id)
    sess = session or requests.Session()
    resp = sess.get(url, auth=(api_client_id, client_secret))
    resp.raise_for_status()
    # Explicitly cast to str to satisfy mypy
    return str(resp.text)


def fetch_lightning_events(
    lat_lon: Tuple[float, float],
    *,
    size: float = 1.0,
    max_age: str = "P1D",
    referencetime: str = "latest",
    session: Optional[requests.Session] = None,
    client_id: Optional[str] = None,
) -> List[Lightning]:
    """
    Fetch lightning events from the MET Norway API for a given location.

    Args:
        lat_lon: Tuple of (latitude, longitude) coordinates
        size: Size of the bounding box in degrees
        max_age: Age of data to fetch (ISO8601 duration)
        referencetime: Reference time (default is "latest")
        session: Optional requests.Session to use
        client_id: Optional explicit client ID to use instead of environment variable

    Returns:
        List of Lightning events
    """
    text = fetch_lightning_ualf(
        lat_lon,
        size=size,
        max_age=max_age,
        referencetime=referencetime,
        session=session,
        client_id=client_id,
    )
    return parse_ualf(text)
