"""
GolfAI On Course Mode
Version: v0.1

Mobile-first cue display.
"""

import os
import streamlit as st
from golfai.cue_engine import build_oncourse_cues


def oncourse_page():
    st.markdown("## GOLF AI")
    st.markdown("### ON COURSE MODE")

    cues = build_oncourse_cues()

    if not cues["has_cues"]:
        st.info(cues["message"])
        return

    st.subheader("Today's Swing Focus")

    primary_image_path = f"/kaggle/working/GolfAI/golfai/cue_images/{cues['primary_image']}"
    if os.path.exists(primary_image_path):
        st.image(primary_image_path, use_container_width=True)

    st.markdown(f"### {cues['primary_cue']}")
    st.caption(cues["primary_desc"])

    st.divider()

    secondary_image_path = f"/kaggle/working/GolfAI/golfai/cue_images/{cues['secondary_image']}"
    if os.path.exists(secondary_image_path):
        st.image(secondary_image_path, use_container_width=True)

    st.markdown(f"### {cues['secondary_cue']}")
    st.caption(cues["secondary_desc"])

    st.divider()

    c1, c2 = st.columns(2)
    c1.metric("Miss Pattern", cues.get("miss_bias", "-"))
    c2.metric("Last Session", cues.get("momentum", "-"))
