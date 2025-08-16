from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Iterable, List, Union

if TYPE_CHECKING:  # for type checkers only; pandas is optional at runtime
    import pandas as pd

__all__ = [
    "Lightning",
    "parse_ualf_line",
    "parse_ualf",
    "to_dataframe",
]


@dataclass(frozen=True)
class Lightning:
    version: int
    timestamp: datetime  # timezone-aware (UTC), microsecond precision
    lat: float
    lon: float
    peak_current: int
    multiplicity: int
    sensors: int
    degrees_of_freedom: int
    angle: float
    semi_major_axis: float
    semi_minor_axis: float
    chi_square: float
    rise_time: float
    peak_to_zero_time: float
    max_rate_of_rise: float
    cloud_indicator: bool
    angle_indicator: bool
    signal_indicator: bool
    timing_indicator: bool

    def to_dict(self) -> dict:
        d = asdict(self)
        d["timestamp"] = self.timestamp.isoformat()
        return d


def _to_bool_int(x: str) -> bool:
    s = x.strip()
    if s in {"0", "0.0", "false", "False"}:
        return False
    if s in {"1", "1.0", "true", "True"}:
        return True
    try:
        return float(s) != 0.0
    except Exception as e:
        raise ValueError(f"Invalid boolean token: {x!r}") from e


def parse_ualf_line(line: str) -> Lightning:
    """Parse a single UALF line into a Lightning event.

    Raises ValueError for malformed lines.
    """
    tokens = line.strip().split()
    if not tokens:
        raise ValueError("Empty UALF line")
    if len(tokens) < 25:
        raise ValueError(
            f"UALF line has {len(tokens)} tokens; expected 25. Line: {line!r}"
        )

    version = int(tokens[0])
    year = int(tokens[1])
    month = int(tokens[2])
    day = int(tokens[3])
    hour = int(tokens[4])
    minute = int(tokens[5])
    second = int(tokens[6])
    nanosecond = int(tokens[7])

    micro = nanosecond // 1000
    base_dt = datetime(
        year, month, day, hour, minute, second, microsecond=micro, tzinfo=timezone.utc
    )

    lat = float(tokens[8])
    lon = float(tokens[9])
    peak_current = int(float(tokens[10]))
    multiplicity = int(float(tokens[11]))
    sensors = int(float(tokens[12]))
    dof = int(float(tokens[13]))
    angle = float(tokens[14])
    semi_major = float(tokens[15])
    semi_minor = float(tokens[16])
    chi_square = float(tokens[17])
    rise_time = float(tokens[18])
    peak_to_zero = float(tokens[19])
    max_rate = float(tokens[20])
    cloud = _to_bool_int(tokens[21])
    angle_ind = _to_bool_int(tokens[22])
    signal_ind = _to_bool_int(tokens[23])
    timing_ind = _to_bool_int(tokens[24])

    return Lightning(
        version=version,
        timestamp=base_dt,
        lat=lat,
        lon=lon,
        peak_current=peak_current,
        multiplicity=multiplicity,
        sensors=sensors,
        degrees_of_freedom=dof,
        angle=angle,
        semi_major_axis=semi_major,
        semi_minor_axis=semi_minor,
        chi_square=chi_square,
        rise_time=rise_time,
        peak_to_zero_time=peak_to_zero,
        max_rate_of_rise=max_rate,
        cloud_indicator=cloud,
        angle_indicator=angle_ind,
        signal_indicator=signal_ind,
        timing_indicator=timing_ind,
    )


def parse_ualf(text: str, *, strict: bool = False) -> List[Lightning]:
    """Parse a UALF text blob, skipping blank lines and comments.

    When strict=True, any malformed line will raise; otherwise bad lines are skipped.
    """
    results: List[Lightning] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        try:
            results.append(parse_ualf_line(line))
        except Exception:
            if strict:
                raise
            # else skip bad lines
            continue
    return results


def to_dataframe(events: Iterable[Lightning]) -> Union["pd.DataFrame", List[dict]]:
    try:
        import pandas as pd

        # Construct via records for speed; keep typing flexible at runtime
        return pd.DataFrame([e.to_dict() for e in events])
    except Exception:
        return [e.to_dict() for e in events]
