
"""
GolfAI Scoring
Version: v0.1
"""

def build_session_score(detector_results):
    strike_quality = detector_results.get("strike_quality", 0)
    start_line_control = detector_results.get("start_line_control", 0)
    lowpoint_score = detector_results.get("lowpoint_score", 0)
    sequencing_score = detector_results.get("sequencing_score", 0)

    carry_std_score = detector_results.get("carry_std_score", 0)
    blueprint_match_pct = detector_results.get("blueprint_match_pct", 0)
    momentum_last20 = detector_results.get("momentum_last20", 0)
    drift_detected = detector_results.get("drift_detected", False)
    corridor_pct = detector_results.get("corridor_pct", 0)

    performance_score = round(
        (strike_quality * 0.22) +
        (start_line_control * 0.14) +
        (lowpoint_score * 0.16) +
        (sequencing_score * 0.14) +
        (carry_std_score * 0.06) +
        (blueprint_match_pct * 0.08) +
        (max(0, momentum_last20) * 0.06) +
        ((0 if drift_detected else 100) * 0.06) +
        (corridor_pct * 0.08)
    )

    issue_scores = {
        "Strike Quality": strike_quality,
        "Start Line Control": start_line_control,
        "Sequencing": sequencing_score,
        "Low Point Stability": lowpoint_score
    }

    sorted_issues = sorted(issue_scores.items(), key=lambda x: x[1])

    primary_issue = sorted_issues[0][0]
    secondary_issue = sorted_issues[1][0]

    return {
        "performance_score": performance_score,
        "primary_issue": primary_issue,
        "secondary_issue": secondary_issue
    }
