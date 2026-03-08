"""
GolfAI Trend Intelligence
Version: v0.2

Reads session history and builds trend data.
"""

from golfai.session_history import load_history


def build_trend_data():
    history = load_history()

    if not history:
        return {
            "has_history": False,
            "sessions": [],
            "performance": [],
            "blueprint": [],
            "lowpoint": [],
            "dispersion": [],
        }

    sessions = list(range(1, len(history) + 1))

    performance = [h.get("performance_score", 0) for h in history]
    blueprint = [h.get("blueprint_match_pct", 0) for h in history]
    lowpoint = [h.get("lowpoint_score", 0) for h in history]
    dispersion = [h.get("corridor_pct", 0) for h in history]

    return {
        "has_history": True,
        "sessions": sessions,
        "performance": performance,
        "blueprint": blueprint,
        "lowpoint": lowpoint,
        "dispersion": dispersion,
    }
