
"""
GolfAI Practice Effectiveness Engine
Version: v1.0

Purpose
-------
Evaluates how effective recent practice sessions have been by
comparing the most recent session against the previous one.

Outputs:
- overall_direction
- best_improvement
- biggest_risk
- recommendation

This engine is designed to evolve into a much deeper learning
system across multiple sessions.
"""

import pandas as pd
from golfai.session_history import load_session_history


def build_practice_effectiveness():

    history = load_session_history()

    if history is None or len(history) < 2:
        return {
            "has_effectiveness": False,
            "message": "Practice effectiveness appears after at least two sessions."
        }

    history = history.sort_values("session_date")

    latest = history.iloc[-1]
    previous = history.iloc[-2]

    metrics = {
        "Performance": "performance_score",
        "Blueprint": "blueprint_match_pct",
        "Low Point": "lowpoint_score",
        "Dispersion": "corridor_pct",
        "Strike": "strike_quality"
    }

    improvements = {}

    for name, col in metrics.items():
        if col in latest and col in previous:
            delta = latest[col] - previous[col]
            improvements[name] = delta

    if not improvements:
        return {
            "has_effectiveness": False,
            "message": "Insufficient metric history for effectiveness analysis."
        }

    best_metric = max(improvements, key=improvements.get)
    best_delta = improvements[best_metric]

    worst_metric = min(improvements, key=improvements.get)
    worst_delta = improvements[worst_metric]

    avg_delta = sum(improvements.values()) / len(improvements)

    if avg_delta > 2:
        direction = "Positive"
    elif avg_delta < -2:
        direction = "Negative"
    else:
        direction = "Neutral"

    recommendation = generate_recommendation(worst_metric)

    return {
        "has_effectiveness": True,
        "overall_direction": direction,
        "best_improvement": best_metric,
        "best_delta": round(best_delta, 2),
        "biggest_risk": worst_metric,
        "risk_delta": round(worst_delta, 2),
        "recommendation": recommendation
    }


def generate_recommendation(metric):

    recommendations = {
        "Dispersion": "Prioritise start line and face control next session.",
        "Low Point": "Work on strike compression and consistent attack angle.",
        "Blueprint": "Focus on repeating the target swing blueprint.",
        "Strike": "Improve contact quality through low point control drills.",
        "Performance": "Focus on overall swing sequencing and rhythm."
    }

    return recommendations.get(metric, "Continue structured practice sessions.")
