"""
GolfAI Engine
Version: v1.3

Changes in v1.3:
- Added session history foundation
- Saves lightweight session summaries after analysis
- Still supports CSV upload workflow
"""

from golfai.data_loader import load_session, load_uploaded_session
from golfai.detectors import (
    compute_strike_quality,
    compute_start_line_control,
    compute_lowpoint_score,
    compute_sequencing_score,
    build_blueprint_signature,
    count_blueprint_matches,
    compute_session_momentum,
    compute_swing_drift,
    compute_dispersion_intelligence,
    build_shot_pattern_data,
)
from golfai.metrics import safe_std, bounded_score
from golfai.config import CARRY_STD_GOOD, CARRY_STD_BAD
from golfai.scoring import build_session_score
from golfai.practice_coach import build_practice_plan
from golfai.session_history import save_session_summary


def run_golfai_analysis(session_file=None, uploaded_file=None):
    if session_file is None and uploaded_file is None:
        return {
            "session_file": "None selected",
            "shots_analysed": 0,
            "performance_score": 0,
            "primary_issue": "No session loaded",
            "secondary_issue": "",
            "practice_focus": [],
            "one_cue": "",
            "sequencing_score": 0,
            "lowpoint_score": 0,
            "strike_quality": 0,
            "start_line_control": 0,
            "session_summary": {},
            "practice_plan": {}
        }

    if uploaded_file is not None:
        df = load_uploaded_session(uploaded_file)
        session_label = getattr(uploaded_file, "name", "Uploaded CSV")
    else:
        df = load_session(session_file)
        session_label = session_file

    shots = len(df)

    if shots == 0:
        return {
            "session_file": session_label,
            "shots_analysed": 0,
            "performance_score": 0,
            "primary_issue": "No 7-iron shots found",
            "secondary_issue": "",
            "practice_focus": [],
            "one_cue": "",
            "sequencing_score": 0,
            "lowpoint_score": 0,
            "strike_quality": 0,
            "start_line_control": 0,
            "session_summary": {},
            "practice_plan": {}
        }

    strike_quality, strike_diag = compute_strike_quality(df)
    start_line_control, start_diag = compute_start_line_control(df)
    lowpoint_score, lp_diag = compute_lowpoint_score(df)
    sequencing_score, seq_diag = compute_sequencing_score(df)

    blueprint_sig = build_blueprint_signature(df, top_percent=0.20)
    blueprint_diag = count_blueprint_matches(df, blueprint_sig)

    momentum_diag = compute_session_momentum(df, window=20)
    drift_diag = compute_swing_drift(df, lookback=15, start_thresh=1.5, path_thresh=1.5)
    dispersion_diag = compute_dispersion_intelligence(df)
    shot_pattern_diag = build_shot_pattern_data(df)

    carry_std = safe_std(df["Carry Distance"]) if "Carry Distance" in df.columns else 0.0
    carry_std_score = bounded_score(
        carry_std,
        good=CARRY_STD_GOOD,
        bad=CARRY_STD_BAD,
        higher_is_better=False
    )

    detector_results = {
        "strike_quality": strike_quality,
        "start_line_control": start_line_control,
        "lowpoint_score": lowpoint_score,
        "sequencing_score": sequencing_score,
        "carry_std_score": carry_std_score,
        **strike_diag,
        **start_diag,
        **lp_diag,
        **seq_diag,
        **blueprint_diag,
        **momentum_diag,
        **drift_diag,
        **dispersion_diag,
        **shot_pattern_diag,
    }

    scoring_results = build_session_score(detector_results)

    one_cue = "Pause at the top, let the arms fall, then turn."

    session_summary = {
        "performance_score": scoring_results.get("performance_score", 0),
        "primary_issue": scoring_results.get("primary_issue", ""),
        "secondary_issue": scoring_results.get("secondary_issue", ""),
        "one_cue": one_cue,
        "blueprint_matches": blueprint_diag.get("blueprint_matches", 0),
        "blueprint_total": blueprint_diag.get("blueprint_total", 0),
        "blueprint_match_pct": blueprint_diag.get("blueprint_match_pct", 0),
        "momentum_label": momentum_diag.get("momentum_label", ""),
        "momentum_delta": momentum_diag.get("momentum_delta", 0),
        "drift_label": drift_diag.get("drift_label", ""),
        "drift_detected": drift_diag.get("drift_detected", False),
        "miss_bias": dispersion_diag.get("miss_bias", ""),
        "corridor_pct": dispersion_diag.get("corridor_pct", 0),
    }

    result = {
        "session_file": session_label,
        "shots_analysed": shots,
        **scoring_results,
        "practice_focus": [
            "Neutral forearm setup",
            "Pause at top",
            "Arms fall before chest"
        ],
        "one_cue": one_cue,
        "session_summary": session_summary,
        **detector_results,
    }

    if blueprint_sig is not None:
        result.update(blueprint_sig)
    else:
        result.update({
            "n_top": 0,
            "bp_smash_target": 0.0,
            "bp_path_target": 0.0,
            "bp_start_target": 0.0,
            "bp_carry_target": 0.0,
            "bp_smash_min": 0.0,
            "bp_path_min": 0.0,
            "bp_path_max": 0.0,
            "bp_start_min": 0.0,
            "bp_start_max": 0.0,
        })

    result["practice_plan"] = build_practice_plan(result)

    # Save lightweight summary for future trend intelligence
    history_summary = {
        "session_file": result.get("session_file"),
        "performance_score": result.get("performance_score"),
        "primary_issue": result.get("primary_issue"),
        "sequencing_score": result.get("sequencing_score"),
        "lowpoint_score": result.get("lowpoint_score"),
        "strike_quality": result.get("strike_quality"),
        "blueprint_match_pct": result.get("blueprint_match_pct"),
        "corridor_pct": result.get("corridor_pct"),
    }

    save_session_summary(history_summary)

    return result
