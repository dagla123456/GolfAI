
"""
GolfAI Data Loader
Version: v0.1
"""

import os
import pandas as pd
from golfai.config import DATA_FOLDER, DEFAULT_CLUB_FILTER

def list_sessions():
    if not os.path.exists(DATA_FOLDER):
        return []

    files = [f for f in os.listdir(DATA_FOLDER) if f.endswith(".csv")]
    files.sort()
    return files

def load_session(session_file, club_filter=DEFAULT_CLUB_FILTER):
    path = os.path.join(DATA_FOLDER, session_file)
    df = pd.read_csv(path)

    if "Club" in df.columns:
        df = df[df["Club"].astype(str).str.contains(club_filter, na=False)].copy()

    return df
