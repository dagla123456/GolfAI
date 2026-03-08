"""
GolfAI Session Comparison
Version: v0.1

Builds a simple comparison between the two most recent sessions
in session history.
"""

from golfai.session_history import load_history


def compare_latest_sessions():
    history = load_history()

    if len(history) < 2:
        return {
            "has_comparison": False,
            "message": "Comparison will appear after at least two sessions are stored."
        }

    previous = history[-2]
    current = history[-1]

    def delta(key):
        return round(current.get(key, 0) - previous.get(key, 0), 1)

    return {
        "has_comparison": True,
        "previous_session": previous.get("session_file", "Previous"),
        "current_session": current.get("session_file", "Current"),

        "performance_prev": previous.get("performance_score", 0),
        "performance_curr": current.get("performance_score", 0),
        "performance_delta": delta("performance_score"),

        "blueprint_prev": previous.get("blueprint_match_pct", 0),
        "blueprint_curr": current.get("blueprint_match_pct", 0),
        "blueprint_delta": delta("blueprint_match_pct"),

        "lowpoint_prev": previous.get("lowpoint_score", 0),
        "lowpoint_curr": current.get("lowpoint_score", 0),
        "lowpoint_delta": delta("lowpoint_score"),

        "corridor_prev": previous.get("corridor_pct", 0),
        "corridor_curr": current.get("corridor_pct", 0),
        "corridor_delta": delta("corridor_pct"),
    }
