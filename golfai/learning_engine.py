"""
GolfAI Learning Engine
Version: v1.0

Purpose:
Analyzes session history to detect whether key metrics
are improving, stable, or worsening over time.
"""

from golfai.session_history import load_history


def evaluate_trend(values, threshold=3):
    if len(values) < 2:
        return "Not enough data"

    latest = values[-1]
    previous = values[-2]
    change = latest - previous

    if change > threshold:
        return "Improving"
    elif change < -threshold:
        return "Worsening"
    else:
        return "Stable"


def build_learning_insights():
    history = load_history()

    if len(history) < 2:
        return {
            "has_learning": False,
            "message": "Learning insights appear after multiple sessions."
        }

    performance = [h.get("performance_score", 0) for h in history]
    blueprint = [h.get("blueprint_match_pct", 0) for h in history]
    lowpoint = [h.get("lowpoint_score", 0) for h in history]
    dispersion = [h.get("corridor_pct", 0) for h in history]
    strike = [h.get("strike_quality", 0) for h in history]

    return {
        "has_learning": True,
        "performance_trend": evaluate_trend(performance),
        "blueprint_trend": evaluate_trend(blueprint),
        "lowpoint_trend": evaluate_trend(lowpoint),
        "dispersion_trend": evaluate_trend(dispersion),
        "strike_trend": evaluate_trend(strike),
    }
