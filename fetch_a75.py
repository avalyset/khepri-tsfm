"""Step 3: fetch ENTSO-E A75 (Actual Generation per Production Type) for 2026.

Same schema as the Khepri v1 raw CSVs ({zone}_generation_{year}.csv, one column per
production type, 'Actual Aggregated' only, local-time index with offset), following the
Khepri v1 fetch pattern (entsoe-py query_generation, psr_type=None). Raw data is written
to $V/data/raw/entsoe-rest-2026 on the Vault volume only and never committed.

Discipline: token read from ~/.config/khepri/entsoe.env, never printed (only len/prefix
checks); error text is sanitised before logging; 5 s between calls; HTTP 429 -> 90 s,
max 3; 5xx and transient 400s -> 20 s, max 3; UTC month boundaries, max P1M per call.

Usage: python fetch_a75.py <end-utc-hour, e.g. 2026-11-02T07:00Z> [--start YYYY-MM-DD] [--out DIR]
(defaults: --start 2026-01-01, --out $V/data/raw/entsoe-rest-2026). Files are split by
UTC calendar year as in the v1 raw tree.
"""

import json
import os
import sys
import time

import pandas as pd
import requests
from entsoe import EntsoePandasClient
from entsoe.exceptions import NoMatchingDataError

V = os.environ["V"]
OUT = os.path.join(V, "data", "raw", "entsoe-rest-2026")
ZONES = {"NO1": "NO_1", "NO2": "NO_2", "NO3": "NO_3", "NO4": "NO_4", "NO5": "NO_5",
         "SE1": "SE_1", "SE2": "SE_2", "SE3": "SE_3", "SE4": "SE_4"}
TRANSIENT_400 = ("Timeout deadline", "unexpected error occurred", "I/O error")


def load_token():
    tok = None
    with open(os.path.expanduser("~/.config/khepri/entsoe.env")) as f:
        for line in f:
            k, _, v = line.strip().partition("=")
            if k.replace("export ", "").strip() == "ENTSOE_API_TOKEN":
                tok = v.strip().strip('"').strip("'")
    if not tok or len(tok) != 36:
        sys.exit("FATAL: ENTSOE_API_TOKEN missing or unexpected length (value not shown)")
    return tok


def sanitise(text, tok):
    return str(text).replace(tok, "***")[:200]


def flatten_to_v1_schema(df):
    """Keep 'Actual Aggregated' production, flatten columns to bare psrType names."""
    if hasattr(df.columns, "levels"):
        agg = [c for c in df.columns if c[1] == "Actual Aggregated"]
        df = df[agg]
        df.columns = [c[0] for c in agg]
    return df


def query(client, area, start, end, tok, log):
    n429 = ntr = 0
    while True:
        try:
            time.sleep(5)
            return flatten_to_v1_schema(client.query_generation(area, start=start, end=end,
                                                                psr_type=None))
        except NoMatchingDataError as ex:
            log.append({"area": area, "start": str(start), "exc": type(ex).__name__})
            return None
        except requests.HTTPError as ex:
            code = ex.response.status_code if ex.response is not None else None
            body = ex.response.text if ex.response is not None else ""
            rec = {"area": area, "start": str(start), "exc": type(ex).__name__,
                   "http": code, "msg": sanitise(body, tok)}
            log.append(rec)
            if code == 429 and n429 < 3:
                n429 += 1; time.sleep(90); continue
            transient = (code is not None and code >= 500) or (
                code == 400 and any(t in body for t in TRANSIENT_400))
            if transient and ntr < 3:
                ntr += 1; time.sleep(20); continue
            raise RuntimeError(f"{area} {start}: HTTP {code} {type(ex).__name__}") from None
        except (requests.ConnectionError, requests.Timeout) as ex:
            log.append({"area": area, "start": str(start), "exc": type(ex).__name__})
            if ntr < 3:
                ntr += 1; time.sleep(20); continue
            raise RuntimeError(f"{area} {start}: {type(ex).__name__}") from None


def main(end_hour, start="2026-01-01", out=OUT):
    tok = load_token()
    client = EntsoePandasClient(api_key=tok)
    os.makedirs(out, exist_ok=True)
    end = pd.Timestamp(end_hour.rstrip("Z"), tz="UTC")
    s0 = pd.Timestamp(start, tz="UTC")
    starts = [s0] + [s for s in pd.date_range(s0, end, freq="MS") if s > s0]
    log, summary = [], []
    for zid, area in ZONES.items():
        parts = []
        for s in starts:
            e = min(s + pd.offsets.MonthBegin(1), end)
            df = query(client, area, s, e, tok, log)
            if df is not None and len(df):
                parts.append(df)
        df = pd.concat(parts).sort_index()
        df = df[~df.index.duplicated(keep="first")]
        years = df.index.tz_convert("UTC").year
        for y in sorted(set(years)):
            df[years == y].to_csv(os.path.join(out, f"{zid}_generation_{y}.csv"))
        summary.append({"zone": zid, "rows": int(len(df)), "first": str(df.index.min()),
                        "last": str(df.index.max()), "cols": sorted(map(str, df.columns))})
        print(json.dumps(summary[-1]), flush=True)
    with open(os.path.join(out, "_fetchlog.json"), "w") as f:
        json.dump({"end_utc": str(end), "fetched_at_utc": pd.Timestamp.now("UTC").isoformat(),
                   "entsoe_py": __import__("entsoe").__version__, "summary": summary,
                   "events": log}, f, indent=2)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("end"); ap.add_argument("--start", default="2026-01-01")
    ap.add_argument("--out", default=OUT)
    a = ap.parse_args()
    main(a.end, a.start, a.out)
