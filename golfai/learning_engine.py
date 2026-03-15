"""
GolfAI Learning Engine
Version: v1.1

Purpose:
Analyses session history to detect whether key metrics
are improving, stable, or worsening over time.

This version:
- compares latest session to previous session
- compares latest session to recent average
- uses metric-specific thresholds
- returns deltas for UI and coaching use
"""

from golfai.session_history import load_history


# ---------------------------------------
# Metric thresholds
# ---------------------------------------
TREND_THRESHOLDS = {
    "performance_score": 3,
    "blueprint_match_pct": 3,
    "lowpoint_score": 3,
    "corridor_pct": 4,
    "strike_quality": 3,
}


# ---------------------------------------
# Helpers
# ---------------------------------------
def safe_numeric_list(history, key):
    """Extract numeric values for a key from session history."""
    values = []
    for item in history:
        value = item.get(key, None)
        if isinstance(value, (int, float)):
            values.append(value)
    return values


def classify_change(change, threshold):
    """Classify a delta using a threshold."""
    if change > threshold:
        return "Improving"
    elif change < -threshold:
        return "Worsening"
    return "Stable"


def average(values):
    """Return average of a list, or None if empty."""
    if not values:
        return None
    return sum(values) / len(values)


def evaluate_metric(values, threshold):
    """
    Evaluate one metric using:
    - latest vs previous
    - latest vs recent average (excluding latest)
    """
    if len(values) < 2:
        return {
            "trend": "Not enough data",
            "latest": None,
            "previous": None,
            "recent_avg": None,
            "delta_vs_previous": None,
            "delta_vs_recent_avg": None,
        }

    latest = values[-1]
    previous = values[-2]

    prior_values = values[:-1]
    recent_window = prior_values[-5:] if len(prior_values) >= 5 else prior_values
    recent_avg = average(recent_window)

    delta_vs_previous = latest - previous
    delta_vs_recent_avg = latest - recent_avg if recent_avg is not None else None

    trend = classify_change(delta_vs_recent_avg, threshold) if delta_vs_recent_avg is not None else classify_change(delta_vs_previous, threshold)

    return {
        "trend": trend,
        "latest": round(latest, 2),
        "previous": round(previous, 2),
        "recent_avg": round(recent_avg, 2) if recent_avg is not None else None,
        "delta_vs_previous": round(delta_vs_previous, 2),
        "delta_vs_recent_avg": round(delta_vs_recent_avg, 2) if delta_vs_recent_avg is not None else None,
    }


def build_overall_summary(metric_results):
    """
    Build a simple overall summary from metric trends.
    """
    improving = []
    worsening = []
    stable = []

    for metric_name, result in metric_results.items():
        trend = result.get("trend", "Not enough data")
        if trend == "Improving":
            improving.append(metric_name)
        elif trend == "Worsening":
            worsening.append(metric_name)
        elif trend == "Stable":
            stable.append(metric_name)

    if not improving and not worsening:
        return "Not enough data to assess learning trend."

    if improving and not worsening:
        return "Overall trend is improving."

    if worsening and not improving:
        return "Overall trend is worsening."

    # Mixed case
    if "strike_quality" in improving and "corridor_pct" in worsening:
        return "Contact is improving faster than directional control."

    if "blueprint_match_pct" in improving and "corridor_pct" in worsening:
        return "Swing pattern is improving, but shot control is lagging."

    return "Mixed trend: some metrics are improving while others are lagging."


# ---------------------------------------
# Main public function
# ---------------------------------------
def build_learning_insights():
    history = load_history()

    if len(history) < 2:
        return {
            "has_learning": False,
            "message": "Learning insights appear after multiple sessions."
        }

    metric_map = {
        "performance_score": safe_numeric_list(history, "performance_score"),
        "blueprint_match_pct": safe_numeric_list(history, "blueprint_match_pct"),
        "lowpoint_score": safe_numeric_list(history, "lowpoint_score"),
        "corridor_pct": safe_numeric_list(history, "corridor_pct"),
        "strike_quality": safe_numeric_list(history, "strike_quality"),
    }

    metric_results = {}
    for metric_name, values in metric_map.items():
        threshold = TREND_THRESHOLDS.get(metric_name, 3)
        metric_results[metric_name] = evaluate_metric(values, threshold)

    summary = build_overall_summary(metric_results)

    return {
        "has_learning": True,
        "summary": summary,
        "performance": metric_results["performance_score"],
        "blueprint": metric_results["blueprint_match_pct"],
        "lowpoint": metric_results["lowpoint_score"],
        "dispersion": metric_results["corridor_pct"],
        "strike": metric_results["strike_quality"],
    }
