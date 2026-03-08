"""
GolfAI Data Loader
Version: v0.3

Changes in v0.3:
- Added robust uploaded CSV loading from bytes
- Supports Streamlit reruns and page switching safely
- Keeps local session listing/loading
"""

import os
from io import BytesIO

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


def load_uploaded_session(uploaded_source, club_filter=DEFAULT_CLUB_FILTER):
    """
    Supports:
    - Streamlit UploadedFile
    - raw bytes
    - BytesIO
    """

    if uploaded_source is None:
        raise ValueError("No uploaded source provided.")

    if isinstance(uploaded_source, bytes):
        buffer = BytesIO(uploaded_source)
    elif isinstance(uploaded_source, BytesIO):
        buffer = uploaded_source
        buffer.seek(0)
    else:
        # Assume Streamlit UploadedFile-like object
        try:
            raw_bytes = uploaded_source.getvalue()
            buffer = BytesIO(raw_bytes)
        except Exception:
            # Final fallback
            if hasattr(uploaded_source, "seek"):
                uploaded_source.seek(0)
            buffer = uploaded_source

    df = pd.read_csv(buffer)
    return filter_club(df, club_filter=club_filter)
