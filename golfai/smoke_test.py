
"""
GolfAI Smoke Test
Version: v0.1
"""

from golfai.data_loader import list_sessions
from golfai.engine import run_golfai_analysis

def run_smoke_test():
    sessions = list_sessions()
    if not sessions:
        return {"ok": False, "reason": "No sessions found"}

    result = run_golfai_analysis(sessions[-1])

    required_keys = [
        "performance_score",
        "primary_issue",
        "secondary_issue",
        "practice_plan",
        "blueprint_matches",
        "momentum_label",
        "miss_bias",
        "shot_pattern_points",
    ]

    missing = [k for k in required_keys if k not in result]

    if missing:
        return {"ok": False, "reason": f"Missing keys: {missing}"}

    return {
        "ok": True,
        "session": sessions[-1],
        "performance": result["performance_score"],
        "primary_issue": result["primary_issue"],
        "practice_plan_title": result["practice_plan"].get("practice_plan_title", ""),
    }

if __name__ == "__main__":
    print(run_smoke_test())
