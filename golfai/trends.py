"""
GolfAI Trend Intelligence
Version: v0.3

Change Summary:
- Extracts real session dates from MLM2PRO filenames
- Sorts history by actual session date
- Returns date labels for trend plotting
- Backfills older history entries that may not include session_date
"""

import re
from datetime import datetime

from golfai.session_history import load_history


def extract_session_date(session_file):
    if not session_file:
        return None

    match = re.search(r"(\d{6})", session_file)
    if not match:
        return None

    raw = match.group(1)

    try:
        dt = datetime.strptime(raw, "%m%d%y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return None


def build_trend_data():
    history = load_history()

    if not history:
        return {
            "has_history": False,
            "dates": [],
            "performance": [],
            "blueprint": [],
            "lowpoint": [],
            "dispersion": [],
        }

    enriched = []
    for item in history:
        session_date = item.get("session_date")
        if not session_date:
            session_date = extract_session_date(item.get("session_file"))

        enriched.append({
            **item,
            "session_date": session_date
        })

    def sort_key(item):
        session_date = item.get("session_date")
        if session_date:
            try:
                return datetime.strptime(session_date, "%Y-%m-%d")
            except ValueError:
                pass
        return datetime.max

    enriched = sorted(enriched, key=sort_key)

    date_labels = []
    for item in enriched:
        session_date = item.get("session_date")
        if session_date:
            try:
                dt = datetime.strptime(session_date, "%Y-%m-%d")
                date_labels.append(dt.strftime("%d-%b"))
            except ValueError:
                date_labels.append(item.get("session_file", "Unknown"))
        else:
            date_labels.append(item.get("session_file", "Unknown"))

    performance = [h.get("performance_score", 0) for h in enriched]
    blueprint = [h.get("blueprint_match_pct", 0) for h in enriched]
    lowpoint = [h.get("lowpoint_score", 0) for h in enriched]
    dispersion = [h.get("corridor_pct", 0) for h in enriched]

    return {
        "has_history": True,
        "dates": date_labels,
        "performance": performance,
        "blueprint": blueprint,
        "lowpoint": lowpoint,
        "dispersion": dispersion,
    }
