
"""
GolfAI Detectors
Version: v0.2
"""

import math
import pandas as pd

from golfai.config import (
    DISPERSION_CORRIDOR_M,
    SMASH_GOOD, SMASH_BAD,
    SMASH_STD_GOOD, SMASH_STD_BAD,
    LAUNCH_BIAS_GOOD, LAUNCH_BIAS_BAD,
    LAUNCH_STD_GOOD, LAUNCH_STD_BAD,
)
from golfai.metrics import safe_mean, safe_std, safe_cv, safe_median, bounded_score

def compute_strike_quality(df):
    smash_avg = safe_mean(df["Smash Factor"]) if "Smash Factor" in df.columns else 0.0
    smash_std = safe_std(df["Smash Factor"]) if "Smash Factor" in df.columns else 0.0

    smash_avg_score = bounded_score(smash_avg, good=SMASH_GOOD, bad=SMASH_BAD, higher_is_better=True)
    smash_std_score = bounded_score(smash_std, good=SMASH_STD_GOOD, bad=SMASH_STD_BAD, higher_is_better=False)

    strike_quality = round((smash_avg_score * 0.7) + (smash_std_score * 0.3))

    return strike_quality, {
        "smash_avg": round(smash_avg, 3),
        "smash_std": round(smash_std, 3),
    }

def compute_start_line_control(df):
    launch_avg = safe_mean(df["Launch Direction"]) if "Launch Direction" in df.columns else 0.0
    launch_std = safe_std(df["Launch Direction"]) if "Launch Direction" in df.columns else 0.0

    launch_bias_score = bounded_score(abs(launch_avg), good=LAUNCH_BIAS_GOOD, bad=LAUNCH_BIAS_BAD, higher_is_better=False)
    launch_std_score = bounded_score(launch_std, good=LAUNCH_STD_GOOD, bad=LAUNCH_STD_BAD, higher_is_better=False)

    score = round((launch_bias_score * 0.6) + (launch_std_score * 0.4))

    return score, {
        "launch_avg": round(launch_avg, 2),
        "launch_std": round(launch_std, 2),
    }

def compute_lowpoint_score(df):
    smash_std = safe_std(df["Smash Factor"]) if "Smash Factor" in df.columns else 0.0
    carry_cv = safe_cv(df["Carry Distance"]) if "Carry Distance" in df.columns else 0.0
    attack_std = safe_std(df["Attack Angle"]) if "Attack Angle" in df.columns else 0.0
    launch_std = safe_std(df["Launch Angle"]) if "Launch Angle" in df.columns else 0.0
    spin_cv = safe_cv(df["Spin Rate"]) if "Spin Rate" in df.columns else 0.0

    score_smash = bounded_score(smash_std, good=0.025, bad=0.100, higher_is_better=False)
    score_carry = bounded_score(carry_cv, good=0.05, bad=0.20, higher_is_better=False)
    score_attack = bounded_score(attack_std, good=0.6, bad=2.5, higher_is_better=False)
    score_launch = bounded_score(launch_std, good=1.0, bad=4.0, higher_is_better=False)
    score_spin = bounded_score(spin_cv, good=0.08, bad=0.30, higher_is_better=False)

    lowpoint_score = round(
        (score_smash * 0.30) +
        (score_carry * 0.25) +
        (score_attack * 0.25) +
        (score_launch * 0.10) +
        (score_spin * 0.10)
    )

    return lowpoint_score, {
        "carry_cv": round(carry_cv, 3),
        "attack_std": round(attack_std, 2),
        "launch_angle_std": round(launch_std, 2),
        "spin_cv": round(spin_cv, 3),
        "lp_score_smash": score_smash,
        "lp_score_carry": score_carry,
        "lp_score_attack": score_attack,
        "lp_score_launch": score_launch,
        "lp_score_spin": score_spin
    }

def classify_sequence_row(attack_angle):
    if pd.isna(attack_angle):
        return "Outlier / Review"
    if -5.5 <= attack_angle <= -4.0:
        return "Good Sequence"
    elif -6.5 <= attack_angle < -5.5:
        return "Borderline"
    elif attack_angle < -6.5:
        return "Early Chest / Steep"
    elif -4.0 < attack_angle <= -2.5:
        return "Very Shallow / Monitor"
    return "Outlier / Review"

def compute_sequencing_score(df):
    if "Attack Angle" not in df.columns:
        return 0, {
            "good_sequence_pct": 0.0,
            "borderline_pct": 0.0,
            "early_chest_pct": 0.0,
            "very_shallow_pct": 0.0,
            "outlier_pct": 0.0,
            "avg_attack_angle": 0.0
        }

    work = df.copy()
    work["Attack Angle"] = pd.to_numeric(work["Attack Angle"], errors="coerce")
    work = work.dropna(subset=["Attack Angle"]).copy()

    if len(work) == 0:
        return 0, {
            "good_sequence_pct": 0.0,
            "borderline_pct": 0.0,
            "early_chest_pct": 0.0,
            "very_shallow_pct": 0.0,
            "outlier_pct": 0.0,
            "avg_attack_angle": 0.0
        }

    work["Sequence_Class"] = work["Attack Angle"].apply(classify_sequence_row)
    counts = work["Sequence_Class"].value_counts(dropna=False)
    total = len(work)

    good_pct = 100.0 * counts.get("Good Sequence", 0) / total
    borderline_pct = 100.0 * counts.get("Borderline", 0) / total
    early_pct = 100.0 * counts.get("Early Chest / Steep", 0) / total
    shallow_pct = 100.0 * counts.get("Very Shallow / Monitor", 0) / total
    outlier_pct = 100.0 * counts.get("Outlier / Review", 0) / total

    raw_score = (
        good_pct * 1.0 +
        borderline_pct * 0.6 +
        shallow_pct * 0.35 -
        early_pct * 0.45 -
        outlier_pct * 0.25
    )

    sequencing_score = max(0, min(100, round(raw_score)))

    return sequencing_score, {
        "good_sequence_pct": round(good_pct, 1),
        "borderline_pct": round(borderline_pct, 1),
        "early_chest_pct": round(early_pct, 1),
        "very_shallow_pct": round(shallow_pct, 1),
        "outlier_pct": round(outlier_pct, 1),
        "avg_attack_angle": round(safe_mean(work["Attack Angle"]), 2)
    }

def build_blueprint_signature(df, top_percent=0.20):
    required_cols = ["Smash Factor", "Club Path", "Launch Direction", "Carry Distance"]
    for col in required_cols:
        if col not in df.columns:
            return None

    work = df.copy()
    for col in required_cols:
        work[col] = pd.to_numeric(work[col], errors="coerce")
    work = work.dropna(subset=required_cols).copy()

    if len(work) < 10:
        return None

    n_top = max(3, round(len(work) * top_percent))
    best = work.nlargest(n_top, "Smash Factor").copy()

    bp_smash = safe_median(best["Smash Factor"])
    bp_path = safe_median(best["Club Path"])
    bp_start = safe_median(best["Launch Direction"])
    bp_carry = safe_median(best["Carry Distance"])

    return {
        "n_top": int(n_top),
        "bp_smash_target": round(bp_smash, 3),
        "bp_path_target": round(bp_path, 2),
        "bp_start_target": round(bp_start, 2),
        "bp_carry_target": round(bp_carry, 1),
        "bp_smash_min": round(bp_smash - 0.018, 3),
        "bp_path_min": round(bp_path - 2.33, 2),
        "bp_path_max": round(bp_path + 2.33, 2),
        "bp_start_min": round(bp_start - 1.25, 2),
        "bp_start_max": round(bp_start + 1.25, 2),
    }

def count_blueprint_matches(df, signature):
    if signature is None:
        return {"blueprint_matches": 0, "blueprint_total": 0, "blueprint_match_pct": 0.0}

    required_cols = ["Smash Factor", "Club Path", "Launch Direction"]
    for col in required_cols:
        if col not in df.columns:
            return {"blueprint_matches": 0, "blueprint_total": 0, "blueprint_match_pct": 0.0}

    work = df.copy()
    for col in required_cols:
        work[col] = pd.to_numeric(work[col], errors="coerce")
    work = work.dropna(subset=required_cols).copy()

    if len(work) == 0:
        return {"blueprint_matches": 0, "blueprint_total": 0, "blueprint_match_pct": 0.0}

    mask = (
        (work["Smash Factor"] >= signature["bp_smash_min"]) &
        (work["Club Path"] >= signature["bp_path_min"]) &
        (work["Club Path"] <= signature["bp_path_max"]) &
        (work["Launch Direction"] >= signature["bp_start_min"]) &
        (work["Launch Direction"] <= signature["bp_start_max"])
    )

    matches = int(mask.sum())
    total = int(len(work))
    pct = round(100.0 * matches / total, 1) if total > 0 else 0.0

    return {
        "blueprint_matches": matches,
        "blueprint_total": total,
        "blueprint_match_pct": pct
    }

def compute_block_quality(df_block):
    if len(df_block) == 0:
        return 0

    smash_avg = safe_mean(df_block["Smash Factor"]) if "Smash Factor" in df_block.columns else 0.0
    launch_avg = safe_mean(df_block["Launch Direction"]) if "Launch Direction" in df_block.columns else 0.0
    path_avg = safe_mean(df_block["Club Path"]) if "Club Path" in df_block.columns else 0.0

    smash_score = bounded_score(smash_avg, good=SMASH_GOOD, bad=SMASH_BAD, higher_is_better=True)
    launch_score = bounded_score(abs(launch_avg), good=LAUNCH_BIAS_GOOD, bad=LAUNCH_BIAS_BAD, higher_is_better=False)
    path_distance = abs(path_avg - (-4.5))
    path_score = bounded_score(path_distance, good=0.5, bad=3.5, higher_is_better=False)

    return round((smash_score * 0.45) + (launch_score * 0.35) + (path_score * 0.20))

def compute_session_momentum(df, window=20):
    if len(df) < max(10, window):
        return {
            "momentum_first20": 0,
            "momentum_last20": 0,
            "momentum_delta": 0.0,
            "momentum_label": "Not enough shots"
        }

    work = df.copy()
    for col in ["Smash Factor", "Launch Direction", "Club Path"]:
        if col in work.columns:
            work[col] = pd.to_numeric(work[col], errors="coerce")

    first_block = work.head(window).copy()
    last_block = work.tail(window).copy()

    first_quality = compute_block_quality(first_block)
    last_quality = compute_block_quality(last_block)
    delta = round(last_quality - first_quality, 1)

    if delta >= 5:
        label = "↑ Improving"
    elif delta <= -5:
        label = "↓ Fading"
    else:
        label = "→ Flat"

    return {
        "momentum_first20": first_quality,
        "momentum_last20": last_quality,
        "momentum_delta": delta,
        "momentum_label": label
    }

def compute_swing_drift(df, lookback=15, start_thresh=1.5, path_thresh=1.5):
    required = ["Launch Direction", "Club Path"]
    for col in required:
        if col not in df.columns:
            return {
                "drift_start_session": 0.0,
                "drift_start_last15": 0.0,
                "drift_path_session": 0.0,
                "drift_path_last15": 0.0,
                "drift_start_delta": 0.0,
                "drift_path_delta": 0.0,
                "drift_detected": False,
                "drift_label": "Unavailable"
            }

    work = df.copy()
    for col in required:
        work[col] = pd.to_numeric(work[col], errors="coerce")
    work = work.dropna(subset=required).copy()

    if len(work) < max(10, lookback):
        return {
            "drift_start_session": 0.0,
            "drift_start_last15": 0.0,
            "drift_path_session": 0.0,
            "drift_path_last15": 0.0,
            "drift_start_delta": 0.0,
            "drift_path_delta": 0.0,
            "drift_detected": False,
            "drift_label": "Not enough shots"
        }

    last_block = work.tail(lookback).copy()

    start_session = safe_mean(work["Launch Direction"])
    path_session = safe_mean(work["Club Path"])
    start_last = safe_mean(last_block["Launch Direction"])
    path_last = safe_mean(last_block["Club Path"])

    start_delta = round(start_last - start_session, 2)
    path_delta = round(path_last - path_session, 2)
    drift_detected = (abs(start_delta) >= start_thresh) or (abs(path_delta) >= path_thresh)

    return {
        "drift_start_session": round(start_session, 2),
        "drift_start_last15": round(start_last, 2),
        "drift_path_session": round(path_session, 2),
        "drift_path_last15": round(path_last, 2),
        "drift_start_delta": start_delta,
        "drift_path_delta": path_delta,
        "drift_detected": drift_detected,
        "drift_label": "⚠️ Drift Detected" if drift_detected else "Stable"
    }

def compute_dispersion_intelligence(df, corridor_m=DISPERSION_CORRIDOR_M):
    required = ["Side Carry", "Carry Distance"]
    for col in required:
        if col not in df.columns:
            return {
                "side_avg": 0.0,
                "side_std": 0.0,
                "carry_std_disp": 0.0,
                "corridor_m": corridor_m,
                "corridor_pct": 0.0,
                "dispersion_area": 0.0,
                "miss_bias": "Unavailable"
            }

    work = df.copy()
    work["Side Carry"] = pd.to_numeric(work["Side Carry"], errors="coerce")
    work["Carry Distance"] = pd.to_numeric(work["Carry Distance"], errors="coerce")
    work = work.dropna(subset=["Side Carry", "Carry Distance"]).copy()

    if len(work) == 0:
        return {
            "side_avg": 0.0,
            "side_std": 0.0,
            "carry_std_disp": 0.0,
            "corridor_m": corridor_m,
            "corridor_pct": 0.0,
            "dispersion_area": 0.0,
            "miss_bias": "Unavailable"
        }

    side_avg = safe_mean(work["Side Carry"])
    side_std = safe_std(work["Side Carry"])
    carry_std_disp = safe_std(work["Carry Distance"])

    inside = ((work["Side Carry"] >= -corridor_m) & (work["Side Carry"] <= corridor_m)).sum()
    total = len(work)
    corridor_pct = round(100.0 * inside / total, 1) if total > 0 else 0.0
    dispersion_area = round(math.pi * side_std * carry_std_disp, 1)

    if side_avg <= -3.0:
        miss_bias = "Left Bias"
    elif side_avg >= 3.0:
        miss_bias = "Right Bias"
    else:
        miss_bias = "Neutral Bias"

    return {
        "side_avg": round(side_avg, 1),
        "side_std": round(side_std, 2),
        "carry_std_disp": round(carry_std_disp, 2),
        "corridor_m": corridor_m,
        "corridor_pct": corridor_pct,
        "dispersion_area": dispersion_area,
        "miss_bias": miss_bias
    }

def build_shot_pattern_data(df):
    required = ["Side Carry", "Carry Distance"]
    for col in required:
        if col not in df.columns:
            return {
                "shot_pattern_points": [],
                "mean_side": 0.0,
                "mean_carry": 0.0,
                "ellipse_width": 0.0,
                "ellipse_height": 0.0
            }

    work = df.copy()
    work["Side Carry"] = pd.to_numeric(work["Side Carry"], errors="coerce")
    work["Carry Distance"] = pd.to_numeric(work["Carry Distance"], errors="coerce")
    work = work.dropna(subset=["Side Carry", "Carry Distance"]).copy()

    if len(work) == 0:
        return {
            "shot_pattern_points": [],
            "mean_side": 0.0,
            "mean_carry": 0.0,
            "ellipse_width": 0.0,
            "ellipse_height": 0.0
        }

    points = list(zip(work["Side Carry"].round(2), work["Carry Distance"].round(2)))
    mean_side = round(float(work["Side Carry"].mean()), 2)
    mean_carry = round(float(work["Carry Distance"].mean()), 2)

    ellipse_width = round(float(work["Side Carry"].std()) * 2, 2) if len(work) > 1 else 0.0
    ellipse_height = round(float(work["Carry Distance"].std()) * 2, 2) if len(work) > 1 else 0.0

    return {
        "shot_pattern_points": points,
        "mean_side": mean_side,
        "mean_carry": mean_carry,
        "ellipse_width": ellipse_width,
        "ellipse_height": ellipse_height
    }

def build_detector_results(df):
    """
    Run all detector functions and return a single detector_results dictionary.
    """

    strike_quality, strike_info = compute_strike_quality(df)
    start_line_control, start_line_info = compute_start_line_control(df)
    lowpoint_score, lowpoint_info = compute_lowpoint_score(df)
    sequencing_score, sequencing_info = compute_sequencing_score(df)

    momentum_info = compute_session_momentum(df)
    drift_info = compute_swing_drift(df)
    dispersion_info = compute_dispersion_intelligence(df)
    shot_pattern_data = build_shot_pattern_data(df)

    # Optional blueprint logic
    blueprint_signature = build_blueprint_signature(df)
    blueprint_info = count_blueprint_matches(df, blueprint_signature)

    # Optional carry consistency score
    carry_std_score = lowpoint_info.get("lp_score_carry", 0)

    detector_results = {
        # core scores
        "strike_quality": strike_quality,
        "start_line_control": start_line_control,
        "lowpoint_score": lowpoint_score,
        "sequencing_score": sequencing_score,

        # secondary scores
        "carry_std_score": carry_std_score,
        "blueprint_match_pct": blueprint_info.get("blueprint_match_pct", 0.0),
        "corridor_pct": dispersion_info.get("corridor_pct", 0.0),

        # momentum / drift
        "momentum_last20": momentum_info.get("momentum_last20", 0),
        "momentum_delta": momentum_info.get("momentum_delta", 0.0),
        "momentum_label": momentum_info.get("momentum_label", "Unavailable"),
        "drift_detected": drift_info.get("drift_detected", False),
        "drift_label": drift_info.get("drift_label", "Unavailable"),

        # detail blocks for UI / future use
        "strike_info": strike_info,
        "start_line_info": start_line_info,
        "lowpoint_info": lowpoint_info,
        "sequencing_info": sequencing_info,
        "momentum_info": momentum_info,
        "drift_info": drift_info,
        "dispersion_info": dispersion_info,
        "shot_pattern_data": shot_pattern_data,
        "blueprint_signature": blueprint_signature,
        "blueprint_info": blueprint_info,
    }

    return detector_results
