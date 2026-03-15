"""
GolfAI Scoring
Version: v1.0

Purpose:
Build a session performance score and identify the main coaching priorities.
"""

def clamp(value, min_value=0, max_value=100):
    """Clamp a numeric value into a bounded range."""
    return max(min_value, min(max_value, value))


def get_score_label(score):
    """Convert score into a session label."""
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Good"
    elif score >= 50:
        return "Developing"
    return "Needs Work"


def build_session_score(detector_results):
    # Core metrics
    strike_quality = clamp(detector_results.get("strike_quality", 0))
    start_line_control = clamp(detector_results.get("start_line_control", 0))
    lowpoint_score = clamp(detector_results.get("lowpoint_score", 0))
    sequencing_score = clamp(detector_results.get("sequencing_score", 0))

    # Secondary metrics
    carry_std_score = clamp(detector_results.get("carry_std_score", 0))
    blueprint_match_pct = clamp(detector_results.get("blueprint_match_pct", 0))
    corridor_pct = clamp(detector_results.get("corridor_pct", 0))

    # Dynamic context
    momentum_last20 = detector_results.get("momentum_last20", 0)
    drift_detected = detector_results.get("drift_detected", False)

    # Normalise momentum into a usable scoring band
    # Assumes momentum roughly ranges from negative to positive small values.
    momentum_score = clamp(50 + momentum_last20)

    # Softer drift penalty than full binary removal
    drift_penalty = 8 if drift_detected else 0

    # Weighted session score
    base_score = (
        (strike_quality * 0.24) +
        (start_line_control * 0.16) +
        (lowpoint_score * 0.16) +
        (sequencing_score * 0.14) +
        (carry_std_score * 0.08) +
        (blueprint_match_pct * 0.10) +
        (corridor_pct * 0.08) +
        (momentum_score * 0.04)
    )

    performance_score = round(clamp(base_score - drift_penalty))

    # Rank coaching issues from weakest important categories
    issue_scores = {
        "Strike Quality": strike_quality,
        "Start Line Control": start_line_control,
        "Low Point Stability": lowpoint_score,
        "Sequencing": sequencing_score,
        "Blueprint Match": blueprint_match_pct,
        "Dispersion Control": corridor_pct,
    }

    sorted_issues = sorted(issue_scores.items(), key=lambda x: x[1])

    primary_issue = sorted_issues[0][0]
    secondary_issue = sorted_issues[1][0]

    # Session label
    performance_label = get_score_label(performance_score)

    # Short coaching summary
    if primary_issue == "Strike Quality":
        summary = "Contact quality is the biggest current limiter."
    elif primary_issue == "Start Line Control":
        summary = "Directional control is the biggest current limiter."
    elif primary_issue == "Low Point Stability":
        summary = "Low point consistency is reducing strike reliability."
    elif primary_issue == "Sequencing":
        summary = "Sequencing is limiting efficiency and strike quality."
    elif primary_issue == "Blueprint Match":
        summary = "Swing pattern repeatability is still below target."
    else:
        summary = "Dispersion control is still the main scoring limiter."

    return {
        "performance_score": performance_score,
        "performance_label": performance_label,
        "primary_issue": primary_issue,
        "secondary_issue": secondary_issue,
        "summary": summary,
        "component_scores": {
            "strike_quality": strike_quality,
            "start_line_control": start_line_control,
            "lowpoint_score": lowpoint_score,
            "sequencing_score": sequencing_score,
            "carry_std_score": carry_std_score,
            "blueprint_match_pct": blueprint_match_pct,
            "corridor_pct": corridor_pct,
            "momentum_score": momentum_score,
        },
        "drift_detected": drift_detected,
        "drift_penalty": drift_penalty,
    }
