"""
GolfAI Trend Intelligence
Version: v1.0

Purpose:
Analyzes recent session history across core metrics and detects
multi-session improvement, stability, or regression.
"""

from golfai.session_history import load_history


TRACKED_METRICS = {
    "performance_score": "Performance",
    "blueprint_match_pct": "Blueprint",
    "lowpoint_score": "Low Point",
    "corridor_pct": "Dispersion",
    "strike_quality": "Strike",
}


def _recent_values(history, key, lookback=3):
    values = [h.get(key, 0) for h in history if key in h]
    return values[-lookback:]


def _classify_trend(values, threshold=2.0):
    if len(values) < 2:
        return "Not enough data", 0

    change = values[-1] - values[0]

    if change > threshold:
        return "Improving", round(change, 1)
    elif change < -threshold:
        return "Worsening", round(change, 1)
    else:
        return "Stable", round(change, 1)


def _priority_from_concern(label):
    if label == "Dispersion":
        return "Start line and face control"
    if label == "Low Point":
        return "Low point control"
    if label == "Strike":
        return "Strike quality"
    if label == "Blueprint":
        return "Blueprint match consistency"
    return "Maintain current priority"


def build_trend_intelligence(lookback=3):
    history = load_history()

    if len(history) < 2:
        return {
            "has_trends": False,
            "message": "Trend intelligence appears after multiple sessions."
        }

    trends = {}
    deltas = {}

    for key, label in TRACKED_METRICS.items():
        values = _recent_values(history, key, lookback=lookback)
        trend_label, delta = _classify_trend(values)
        trends[f"{label.lower().replace(' ', '_')}_trend"] = trend_label
        deltas[label] = delta

    strongest_gain = max(deltas, key=deltas.get)
    biggest_concern = min(deltas, key=deltas.get)

    return {
        "has_trends": True,
        **trends,
        "strongest_gain": strongest_gain,
        "strongest_gain_delta": round(deltas[strongest_gain], 1),
        "biggest_concern": biggest_concern,
        "biggest_concern_delta": round(deltas[biggest_concern], 1),
        "next_priority": _priority_from_concern(biggest_concern),
        "lookback_sessions": min(lookback, len(history)),
    }
