"""
GolfAI Practice Effectiveness Engine
Version: v1.1

Purpose:
Evaluates whether the most recent practice session was effective
compared with the prior session, and identifies the biggest
improvement, biggest risk, and next recommendation.
"""

from golfai.session_history import load_history


TRACKED_METRICS = {
    "performance_score": "Performance",
    "blueprint_match_pct": "Blueprint",
    "lowpoint_score": "Low Point",
    "corridor_pct": "Dispersion",
    "strike_quality": "Strike",
}


def _delta(current, previous, key):
    return current.get(key, 0) - previous.get(key, 0)


def build_practice_effectiveness():
    history = load_history()

    if len(history) < 2:
        return {
            "has_effectiveness": False,
            "message": "Practice effectiveness appears after at least two sessions."
        }

    previous = history[-2]
    current = history[-1]

    deltas = {}
    for key, label in TRACKED_METRICS.items():
        deltas[label] = _delta(current, previous, key)

    best_metric = max(deltas, key=deltas.get)
    worst_metric = min(deltas, key=deltas.get)

    overall_change = sum(deltas.values())

    if overall_change > 5:
        overall_direction = "Positive"
    elif overall_change < -5:
        overall_direction = "Negative"
    else:
        overall_direction = "Neutral"

    if worst_metric == "Low Point":
        recommendation = "Prioritise low point control next session."
    elif worst_metric == "Dispersion":
        recommendation = "Prioritise start line and face control next session."
    elif worst_metric == "Strike":
        recommendation = "Prioritise strike quality and centered contact next session."
    elif worst_metric == "Blueprint":
        recommendation = "Prioritise blueprint match and movement pattern consistency."
    else:
        recommendation = "Stay with current plan but monitor changes closely."

    return {
        "has_effectiveness": True,
        "overall_direction": overall_direction,
        "best_improvement": best_metric,
        "best_delta": round(deltas[best_metric], 1),
        "biggest_risk": worst_metric,
        "risk_delta": round(deltas[worst_metric], 1),
        "recommendation": recommendation,
    }
