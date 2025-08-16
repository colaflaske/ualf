from __future__ import annotations

import argparse
import json
from typing import Iterable

from .client import fetch_lightning_events
from .parser import Lightning, to_dataframe


def _events_to_json(events: Iterable[Lightning]) -> str:
    """Serialize events to JSON string."""
    return json.dumps([e.to_dict() for e in events], ensure_ascii=False, indent=2)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="UALF client CLI")
    p.add_argument("--lat", type=float, required=True)
    p.add_argument("--lon", type=float, required=True)
    p.add_argument("--size", type=float, default=1.0)
    p.add_argument("--max-age", dest="max_age", default="P1D")
    p.add_argument("--referencetime", default="latest")
    p.add_argument("--format", choices=["json", "table"], default="json")
    p.add_argument("--client-id", type=str, default=None)
    args = p.parse_args(argv)
    events = fetch_lightning_events(
        (args.lat, args.lon),
        size=args.size,
        max_age=args.max_age,
        referencetime=args.referencetime,
        client_id=args.client_id,
    )

    if args.format == "json":
        print(_events_to_json(events))
    else:
        df = to_dataframe(events)
        # Print as a table when pandas is installed
        try:
            import pandas as pd

            if isinstance(df, pd.DataFrame):
                print(df.to_string(index=False))
            else:
                print(df)
        except Exception:
            print(df)

    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
