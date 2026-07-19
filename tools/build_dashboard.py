#!/usr/bin/env python3
"""Build a self-contained HTML dashboard from the running journal logs.

Usage:  python3 tools/build_dashboard.py

Reads every log in logs/**/*.md, normalizes the four frontmatter schema
generations into one record shape, and writes dashboard.html.
No third-party dependencies.
"""

import json
import os
import re
from datetime import date, datetime, timedelta

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGS = os.path.join(ROOT, "logs")
# index.html at the repo root so GitHub Pages serves it directly.
OUT = os.path.join(ROOT, "index.html")


# --------------------------------------------------------------------------
# Minimal YAML subset parser (nested maps, lists, scalars — enough for these logs)
# --------------------------------------------------------------------------

def _scalar(tok):
    tok = tok.strip()
    if tok == "" or tok in ("null", "~", "None"):
        return None
    if tok == "[]":
        return []
    if tok == "{}":
        return {}
    if len(tok) >= 2 and tok[0] == tok[-1] and tok[0] in "\"'":
        return tok[1:-1]
    low = tok.lower()
    if low == "true":
        return True
    if low == "false":
        return False
    if re.fullmatch(r"-?\d+", tok):
        return int(tok)
    if re.fullmatch(r"-?\d*\.\d+", tok):
        return float(tok)
    return tok


def parse_yaml(text):
    """Parse the indentation-based YAML subset used in the journal frontmatter."""
    lines = []
    for raw in text.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        lines.append((len(raw) - len(raw.lstrip()), raw.strip()))

    def block(i, indent):
        """Parse lines[i:] at the given indent. Returns (value, next_index)."""
        if i >= len(lines):
            return None, i
        if lines[i][1].startswith("- "):
            items = []
            while i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
                body = lines[i][1][2:].strip()
                if ":" in body and not body.startswith(("\"", "'")):
                    # list of maps: "- name: Squat" plus deeper sibling keys
                    key, _, rest = body.partition(":")
                    item = {key.strip(): _scalar(rest)}
                    i += 1
                    child = indent + 2
                    while i < len(lines) and lines[i][0] >= child and not lines[i][1].startswith("- "):
                        k, _, v = lines[i][1].partition(":")
                        item[k.strip()] = _scalar(v)
                        i += 1
                    items.append(item)
                else:
                    items.append(_scalar(body))
                    i += 1
            return items, i

        out = {}
        while i < len(lines) and lines[i][0] == indent:
            ind, content = lines[i]
            if content.startswith("- "):
                break
            key, _, rest = content.partition(":")
            key = key.strip()
            rest = rest.strip()
            if rest:
                out[key] = _scalar(rest)
                i += 1
            else:
                i += 1
                if i < len(lines) and lines[i][0] > ind:
                    out[key], i = block(i, lines[i][0])
                elif i < len(lines) and lines[i][0] == ind and lines[i][1].startswith("- "):
                    out[key], i = block(i, ind)
                else:
                    out[key] = None
        return out, i

    value, _ = block(0, lines[0][0] if lines else 0)
    return value or {}


def frontmatter(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    m = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not m:
        return {}, text
    return parse_yaml(m.group(1)), text[m.end():]


# --------------------------------------------------------------------------
# Normalization across schema generations
# --------------------------------------------------------------------------

def dig(d, *path):
    """Walk nested dicts, returning None on any missing/non-dict hop."""
    for key in path:
        if not isinstance(d, dict):
            return None
        d = d.get(key)
    return d


def num(v):
    """Coerce to float, unwrapping {value:, unit:} wrappers."""
    if isinstance(v, dict):
        v = v.get("value")
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    m = re.match(r"^\s*(\d+(?:\.\d+)?)", str(v))
    return float(m.group(1)) if m else None


def to_minutes(v):
    """Accept 44.63, '44:40', '01:08:10', {value: 43.92} -> minutes as float."""
    if isinstance(v, dict):
        v = v.get("value")
    if isinstance(v, (int, float)):
        return float(v)
    if not isinstance(v, str):
        return None
    parts = v.strip().split(":")
    try:
        parts = [float(p) for p in parts]
    except ValueError:
        return num(v)
    if len(parts) == 3:
        return parts[0] * 60 + parts[1] + parts[2] / 60
    if len(parts) == 2:
        return parts[0] + parts[1] / 60
    return parts[0]


def pace_minutes(v):
    """'8:22/km' or '8:22' or 8.58 -> minutes per km as float."""
    if isinstance(v, dict):
        v = v.get("value")
    if isinstance(v, (int, float)):
        return float(v)
    if not isinstance(v, str):
        return None
    return to_minutes(v.replace("/km", "").strip())


# Ordered keyword -> canonical bucket. First match wins, so "recovery walk"
# must be tested before the bare "recovery" and "walk" cases.
ACTIVITY_RULES = [
    (("walk",), "Recovery Walk"),
    (("interval", "repeat", "400m", "on-off", "tempo", "speed"), "Interval Run"),
    (("long",), "Long Run"),
    (("recovery",), "Recovery Run"),
    (("easy",), "Easy Run"),
]


def classify(kind, tags):
    """Collapse the free-form activity strings into one of five buckets.

    The declared activity type wins outright; tags are only consulted when it is
    generic ("run"), since tags describe context too ("pre-long-run" on a
    recovery run) and would otherwise misfile the session.
    """
    for keywords, label in ACTIVITY_RULES:
        if any(k in kind for k in keywords):
            return label
    hay = " ".join(str(t).lower() for t in tags)
    for keywords, label in ACTIVITY_RULES:
        if any(k in hay for k in keywords):
            return label
    return "Run"


def normalize(fm, body, path):
    d = fm.get("date")
    if isinstance(d, str):
        d = d.strip()
    elif isinstance(d, date):
        d = d.isoformat()
    if not d:
        return None

    # activity type — differs per generation
    act = fm.get("activity")
    kind = None
    if isinstance(act, dict):
        kind = act.get("primary") or act.get("category") or act.get("type")
    elif isinstance(act, str):
        kind = act
    kind = kind or fm.get("type")
    if not kind:
        planned = dig(fm, "planned", "workout") or dig(fm, "training", "planned", "workout")
        kind = str(planned).lower().replace(" ", "-") if planned else "run"
    kind = str(kind).strip().lower()

    distance = (num(fm.get("distance"))
                or num(dig(fm, "metrics", "distance_km"))
                or num(dig(fm, "actual", "distance"))
                or num(dig(fm, "training", "actual", "distance_km")))
    duration = (to_minutes(fm.get("duration"))
                or to_minutes(dig(fm, "metrics", "duration"))
                or to_minutes(dig(fm, "actual", "duration")))
    pace = (pace_minutes(fm.get("pace"))
            or pace_minutes(dig(fm, "metrics", "pace_min_per_km"))
            or pace_minutes(dig(fm, "actual", "pace")))
    if pace is None and distance and duration:
        pace = duration / distance

    avg_hr = (num(dig(fm, "heart_rate", "average"))
              or num(dig(fm, "metrics", "avg_hr"))
              or num(dig(fm, "actual", "average_hr")))
    max_hr = (num(dig(fm, "heart_rate", "max"))
              or num(dig(fm, "metrics", "max_hr"))
              or num(dig(fm, "actual", "max_hr")))
    cadence = (num(fm.get("cadence"))
               or num(dig(fm, "metrics", "cadence"))
               or num(dig(fm, "actual", "cadence")))
    weight = num(fm.get("weight")) or num(fm.get("weight_kg"))
    if weight is None:
        m = re.search(r"\|\s*Weight\s*\|\s*\*\*([\d.]+)\s*KG", body, re.I)
        weight = float(m.group(1)) if m else None

    milestones = fm.get("milestones") or []
    if not isinstance(milestones, list):
        milestones = [milestones]
    # snake_case entries ("first_night_run") get title-cased so they sit
    # alongside the prose ones ("First Full Continuous 7K") consistently.
    milestones = [
        str(x).replace("_", " ").title() if "_" in str(x) else str(x)
        for x in milestones if x
    ]

    tags = fm.get("tags") or []
    if not isinstance(tags, list):
        tags = [tags]
    label = classify(kind, tags)

    title = fm.get("title")
    if not title:
        m = re.search(r"^#\s+(.+)$", body, re.M)
        title = re.sub(r"[^\w\s\-—:/+.()]", "", m.group(1)).strip() if m else label

    return {
        "date": d,
        "kind": kind,
        "label": label,
        "title": title,
        "distance": round(distance, 2) if distance else None,
        "duration": round(duration, 4) if duration else None,
        "pace": round(pace, 3) if pace else None,
        "avgHr": int(avg_hr) if avg_hr else None,
        "maxHr": int(max_hr) if max_hr else None,
        "cadence": int(cadence) if cadence else None,
        "weight": weight,
        "milestones": milestones,
        "tags": [str(t) for t in tags],
        "file": os.path.relpath(path, ROOT),
    }


def collect():
    runs = []
    for dirpath, _, files in os.walk(LOGS):
        for name in sorted(files):
            if not name.endswith(".md") or name.isupper():
                continue
            path = os.path.join(dirpath, name)
            fm, body = frontmatter(path)
            if not fm:
                continue
            rec = normalize(fm, body, path)
            if rec:
                runs.append(rec)
    runs.sort(key=lambda r: (r["date"], r["file"]))
    return runs


def weekly(runs):
    """Aggregate distance by ISO week (Monday-started), no gaps."""
    buckets = {}
    for r in runs:
        if not r["distance"]:
            continue
        day = datetime.strptime(r["date"], "%Y-%m-%d").date()
        start = day - timedelta(days=day.weekday())
        b = buckets.setdefault(start, {"km": 0.0, "runs": 0})
        b["km"] += r["distance"]
        b["runs"] += 1
    if not buckets:
        return []
    cur, last = min(buckets), max(buckets)
    out = []
    while cur <= last:
        b = buckets.get(cur, {"km": 0.0, "runs": 0})
        out.append({"week": cur.isoformat(), "km": round(b["km"], 2), "runs": b["runs"]})
        cur += timedelta(days=7)
    return out


def build_payload():
    runs = collect()
    moving = [r for r in runs if r["distance"]]
    weights = [r for r in runs if r["weight"]]
    return {
        "generated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "runs": runs,
        "weekly": weekly(runs),
        "totals": {
            "sessions": len(runs),
            "distance": round(sum(r["distance"] for r in moving), 1),
            "duration": round(sum(r["duration"] for r in runs if r["duration"]) / 60, 1),
            "longest": max((r["distance"] for r in moving), default=0),
            "startWeight": weights[0]["weight"] if weights else None,
            "currentWeight": weights[-1]["weight"] if weights else None,
            "bestWeeklyKm": max((w["km"] for w in weekly(runs)), default=0),
        },
    }


def to_fragment(html):
    """Strip the document shell, keeping <style> + body content.

    Claude Artifacts supply their own doctype/head/body wrapper, so a full
    document would nest <html> inside <body>. Pass --artifact <path> to emit
    this variant alongside the standalone file.
    """
    style = re.search(r"<style>.*?</style>", html, re.S)
    body = re.search(r"<body>(.*?)</body>", html, re.S)
    if not style or not body:
        raise SystemExit("template shape changed: expected a <style> block and a <body>")
    return style.group(0) + "\n" + body.group(1).strip() + "\n"


def main():
    import sys

    payload = build_payload()
    template = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dashboard_template.html")
    with open(template, encoding="utf-8") as fh:
        html = fh.read()
    html = html.replace("/*__DATA__*/null", json.dumps(payload, ensure_ascii=False))
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(html)

    if "--artifact" in sys.argv:
        dest = sys.argv[sys.argv.index("--artifact") + 1]
        with open(dest, "w", encoding="utf-8") as fh:
            fh.write(to_fragment(html))
        print(f"Wrote artifact fragment {dest}")
    t = payload["totals"]
    print(f"Wrote {os.path.relpath(OUT, ROOT)}")
    print(f"  {t['sessions']} sessions · {t['distance']} km · longest {t['longest']} km")


if __name__ == "__main__":
    main()
