"""
GolfAI Streamlit App
Version: v2.2

Change Summary:
- Uses premium dashboard
- Keeps On Course mode
- Keeps tablet-friendly top mode switch
- Loads latest Kaggle CSV session
- Filters latest 7i session
- Runs detectors + session pipeline
- Passes real pipeline data into the premium dashboard
"""

import streamlit as st
import pandas as pd
import glob
import os

from golfai.detectors import build_detector_results
from golfai.session_pipeline import run_session_pipeline
from golfai.v4_dashboard_premium import render_v4_dashboard_premium
from golfai.oncourse_ui import oncourse_page

st.set_page_config(
    page_title="GolfAI",
    layout="wide"
)

st.markdown("""
<style>
div[data-testid="stRadio"] > div {
    flex-direction: row;
    gap: 0.75rem;
}

div[data-testid="stRadio"] label {
    background: #e9edf2;
    padding: 0.55rem 1rem;
    border-radius: 0.7rem;
    border: 1px solid #d8dee8;
}

div[data-testid="stRadio"] label p {
    color: #1f2430 !important;
    font-weight: 600 !important;
}

div[data-testid="stRadio"] label:has(input:checked) {
    background: #1f4a35 !important;
    border: 1px solid #1f4a35 !important;
}

div[data-testid="stRadio"] label:has(input:checked) p {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

mode = st.radio(
    "GolfAI Mode",
    ["Command Centre", "On Course"],
    horizontal=True,
    label_visibility="collapsed"
)

detector_results = None
pipeline_output = None

data_path = "/kaggle/input/datasets/daveg1234/golf-ai-data"
csv_files = glob.glob(os.path.join(data_path, "*.csv"))

if csv_files:
    dfs = []
    for file in csv_files:
        df_temp = pd.read_csv(file)
        df_temp["session_file"] = os.path.basename(file)
        dfs.append(df_temp)

    df = pd.concat(dfs, ignore_index=True)

    session_dates = df[["session_file"]].drop_duplicates().copy()
    session_dates["session_date"] = session_dates["session_file"].str.extract(r"_(\d{6})")[0]
    session_dates["session_date"] = pd.to_datetime(
        session_dates["session_date"],
        format="%m%d%y",
        errors="coerce"
    )
    session_dates = session_dates.sort_values("session_date")

    latest_file = session_dates.iloc[-1]["session_file"]
    latest_session_df = df[df["session_file"] == latest_file].copy()

    latest_7i_df = latest_session_df[
        latest_session_df["Club Type"].astype(str).str.lower().str.contains("7")
    ].copy()

    if len(latest_7i_df) > 0:
        detector_results = build_detector_results(latest_7i_df)
        pipeline_output = run_session_pipeline(detector_results, club="7i")

if mode == "Command Centre":
    render_v4_dashboard_premium(
        detector_results=detector_results,
        pipeline_output=pipeline_output
    )
else:
    oncourse_page()
