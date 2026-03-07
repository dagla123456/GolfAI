
"""
GolfAI Metrics
Version: v0.1
"""

import pandas as pd

def safe_numeric(series):
    return pd.to_numeric(series, errors="coerce").dropna()

def safe_mean(series):
    s = safe_numeric(series)
    return float(s.mean()) if len(s) > 0 else 0.0

def safe_std(series):
    s = safe_numeric(series)
    return float(s.std()) if len(s) > 1 else 0.0

def safe_cv(series):
    s = safe_numeric(series)
    if len(s) < 2:
        return 0.0
    mean_val = s.mean()
    if abs(mean_val) < 1e-9:
        return 0.0
    return float(s.std() / mean_val)

def safe_median(series):
    s = safe_numeric(series)
    return float(s.median()) if len(s) > 0 else 0.0

def bounded_score(value, good, bad, higher_is_better=True):
    if higher_is_better:
        if value >= good:
            return 100
        if value <= bad:
            return 0
        return round(100 * (value - bad) / (good - bad))
    else:
        if value <= good:
            return 100
        if value >= bad:
            return 0
        return round(100 * (bad - value) / (bad - good))
