
"""
GolfAI Practice Coach
Version: v0.1
"""

def build_practice_plan(result):
    primary_issue = result.get("primary_issue", "")
    lowpoint_score = result.get("lowpoint_score", 0)
    sequencing_score = result.get("sequencing_score", 0)
    strike_quality = result.get("strike_quality", 0)
    drift_detected = result.get("drift_detected", False)
    miss_bias = result.get("miss_bias", "")
    momentum_label = result.get("momentum_label", "")

    plan = {
        "practice_plan_title": "General Calibration Session",
        "practice_priority": primary_issue if primary_issue else "Strike Quality",
        "recommended_drill": "Pause Transition Drill",
        "session_goal": "Improve strike quality and directional control",
        "target_smash": "≥ 1.28",
        "target_attack_window": "-4° to -5°",
        "target_launch_direction": "-1° to +1°",
        "target_path_window": "-3° to -5°"
    }

    if primary_issue == "Low Point Stability":
        plan["practice_plan_title"] = "Low Point Recovery Session"
        plan["recommended_drill"] = "Pause Transition Drill"
        plan["session_goal"] = "Stabilise strike and low point"
        plan["target_smash"] = "≥ 1.28"
        plan["target_attack_window"] = "-4° to -5°"
        plan["target_launch_direction"] = "-1° to +1°"

    elif primary_issue == "Sequencing":
        plan["practice_plan_title"] = "Sequencing Reset Session"
        plan["recommended_drill"] = "Pause + Arms Fall Rehearsal"
        plan["session_goal"] = "Improve transition order and reduce steepness"
        plan["target_smash"] = "≥ 1.27"
        plan["target_attack_window"] = "-4° to -5.5°"
        plan["target_launch_direction"] = "-1° to +1°"

    elif primary_issue == "Start Line Control":
        plan["practice_plan_title"] = "Start Line Control Session"
        plan["recommended_drill"] = "Start Line Gate Drill"
        plan["session_goal"] = "Reduce face error at impact"
        plan["target_smash"] = "≥ 1.27"
        plan["target_attack_window"] = "-4° to -5°"
        plan["target_launch_direction"] = "-0.5° to +0.5°"

    elif primary_issue == "Strike Quality":
        plan["practice_plan_title"] = "Strike Quality Session"
        plan["recommended_drill"] = "Half Swing Compression Drill"
        plan["session_goal"] = "Improve centered contact and compression"
        plan["target_smash"] = "≥ 1.30"
        plan["target_attack_window"] = "-4° to -5°"
        plan["target_launch_direction"] = "-1° to +1°"

    if drift_detected:
        plan["session_goal"] += " and maintain it later in the session"

    if miss_bias == "Left Bias":
        plan["target_launch_direction"] = "-0.5° to +0.5°"

    if momentum_label == "↓ Fading":
        plan["session_goal"] += "; use shorter blocks of 10–15 balls"

    if strike_quality >= 50 and lowpoint_score >= 30:
        plan["target_smash"] = "≥ 1.29"

    if lowpoint_score < 20 and sequencing_score < 40:
        plan["recommended_drill"] = "Pause Transition Drill"
        plan["session_goal"] = "Let arms fall before chest rotates"

    return plan
