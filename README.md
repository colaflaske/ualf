# ualf

[![PyPI version](https://img.shields.io/pypi/v/ualf.svg)](https://pypi.org/project/ualf/)
[![CI](https://github.com/colaflaske/ualf/actions/workflows/ci.yml/badge.svg)](https://github.com/colaflaske/ualf/actions/workflows/ci.yml)

Parser and client utilities for the Universal ASCII Lightning Format (UALF), including:

- `parse_ualf_line` and `parse_ualf` to convert UALF text into structured `Lightning` events
- `fetch_lightning_events` helper to call the Norwegian Meteorological Institute (met.no) Frost API lightning endpoint and parse into events
- Optional DataFrame support via `to_dataframe` (install with `pip install ualf[pandas]`)

## Install

```sh
pip install ualf
```

Or for DataFrame support:

```sh
pip install "ualf[pandas]"
```

## Usage (Parser)

```python
from ualf import parse_ualf_line

line = "0 2025 08 15 12 54 11 233363712 64.2117 10.5121 25 0 18 33 117.17 0.23 0.11 0.97 16.8 14.6 2.8 0 1 0 1"
event = parse_ualf_line(line)
print(event.timestamp, event.lat, event.lon)
```

## Usage (Client)

Set credentials for Frost API (Basic auth) and fetch recent strikes:

```sh
# .env
FROST_CLIENT_ID=your-id
```

```python
from ualf import fetch_lightning_events, to_dataframe

lat_lon = (60.0000, 10.0000)
events = fetch_lightning_events(lat_lon, size=1.0, max_age="P1D")
print(len(events))

# Optional pandas
df = to_dataframe(events)
```

## CLI

```sh
ualf-cli --lat 60.0000 --lon 10.0000 --size 1 --max-age P1D --format json --client-id your-id
```

## Unit Tests

- Run unit tests:

```sh
python -m unittest discover -s tests -p "test_*py" -v
```

## Development

```sh
python -m pip install -e .[dev,pandas]
ruff check . && mypy ualf
python -m unittest -v
```

See `CHANGELOG.md` for release notes.

## License

MIT

## Credits
Data from The Norwegian Meteorological Institute
[API usage](https://frost.met.no/howto.html)
