import pandas as pd

def _confidence_from_spread(spread):
    if spread <= 10:
        return "High"
    elif spread <= 18:
        return "Medium"
    return "Low"

def _recommendation(confidence, rmin, rmax):
    if confidence == "High":
        return f"Use this club confidently for {rmin:.0f}–{rmax:.0f} m."
    elif confidence == "Medium":
        return f"This club is usable for {rmin:.0f}–{rmax:.0f} m, but club up above {rmax:.0f} m."
    return f"Distance spread is wide. Treat {rmin:.0f}–{rmax:.0f} m as the safest range."

def build_distance_intelligence(df, club_label="7i"):
    if df is None or len(df) == 0:
        return {"has_distance_intel": False}

    if "Carry Distance" not in df.columns:
        return {"has_distance_intel": False}

    work = df.copy()
    work["Carry Distance"] = pd.to_numeric(work["Carry Distance"], errors="coerce")
    work = work.dropna(subset=["Carry Distance"])

    if len(work) < 5:
        return {"has_distance_intel": False}

    carry = work["Carry Distance"]

    avg = float(carry.mean())
    rmin = float(carry.quantile(0.25))
    rmax = float(carry.quantile(0.75))
    fmin = float(carry.min())
    fmax = float(carry.max())
    spread = float(fmax - fmin)

    confidence = _confidence_from_spread(spread)
    rec = _recommendation(confidence, rmin, rmax)

    return {
        "has_distance_intel": True,
        "club": club_label,
        "avg_carry": round(avg,1),
        "reliable_min": round(rmin,1),
        "reliable_max": round(rmax,1),
        "full_min": round(fmin,1),
        "full_max": round(fmax,1),
        "distance_spread": round(spread,1),
        "confidence": confidence,
        "recommendation": rec
    }
