"""
GolfAI Data Loader
Version: v0.2

Changes in v0.2:
- Added uploaded CSV support
- Keeps local session listing/loading for non-cloud use
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


def filter_club(df, club_filter=DEFAULT_CLUB_FILTER):
    if "Club" in df.columns:
        df = df[df["Club"].astype(str).str.contains(club_filter, na=False)].copy()
    return df


def load_session(session_file, club_filter=DEFAULT_CLUB_FILTER):
    path = os.path.join(DATA_FOLDER, session_file)
    df = pd.read_csv(path)
    return filter_club(df, club_filter=club_filter)


def load_uploaded_session(uploaded_file, club_filter=DEFAULT_CLUB_FILTER):
    df = pd.read_csv(uploaded_file)
    return filter_club(df, club_filter=club_filter)
