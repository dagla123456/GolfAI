"""
GolfAI Session Pipeline
Version: v1.0

Purpose:
Takes detector results, builds a scored session summary,
saves it to history, and returns learning insights for the UI.
"""

from datetime import datetime

from golfai.scoring import build_session_score
from golfai.session_history import save_session_summary, generate_session_id
from golfai.learning_engine import build_learning_insights


def build_session_summary(detector_results, club="7i"):

    score_data = build_session_score(detector_results)

    session_summary = {
        "session_id": f"{club}_{detector_results.get('source_session_file', generate_session_id())}",
        "timestamp": datetime.utcnow().isoformat(),
        "club": club,

        "performance_score": score_data.get("performance_score", 0),
        "primary_issue": score_data.get("primary_issue", "Unknown"),
        "secondary_issue": score_data.get("secondary_issue", "Unknown"),

        "strike_quality": detector_results.get("strike_quality", 0),
        "start_line_control": detector_results.get("start_line_control", 0),
        "lowpoint_score": detector_results.get("lowpoint_score", 0),
        "sequencing_score": detector_results.get("sequencing_score", 0),

        "carry_std_score": detector_results.get("carry_std_score", 0),
        "blueprint_match_pct": detector_results.get("blueprint_match_pct", 0),
        "corridor_pct": detector_results.get("corridor_pct", 0),

        "momentum_last20": detector_results.get("momentum_last20", 0),
        "drift_detected": detector_results.get("drift_detected", False),
    }

    return session_summary


def run_session_pipeline(detector_results, club="7i"):

    session_summary = build_session_summary(detector_results, club)

    history = save_session_summary(session_summary)

    learning_insights = build_learning_insights()

    return {
        "session_summary": session_summary,
        "history_count": len(history),
        "learning_insights": learning_insights,
    }
