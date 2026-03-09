from pathlib import Path
import streamlit as st
from golfai.cue_engine import build_oncourse_cues

BASE_DIR = Path(__file__).resolve().parent
CUE_IMAGE_DIR = BASE_DIR / "cue_images"

def oncourse_page():

    st.title("GOLF AI")
    st.subheader("ON COURSE MODE")

    cues = build_oncourse_cues()

    if not cues["has_cues"]:
        st.info(cues["message"])
        return

    st.markdown("### TODAY'S SWING FOCUS")

    primary_image = cues.get("primary_image")
    if primary_image:
        img_path = CUE_IMAGE_DIR / primary_image
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)

    st.markdown(f"## {cues.get('primary_cue','')}")
    st.caption(cues.get("primary_desc",""))

    st.divider()

    secondary_image = cues.get("secondary_image")
    if secondary_image:

        img_path = CUE_IMAGE_DIR / secondary_image
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)

        st.markdown(f"### {cues.get('secondary_cue','')}")
        st.caption(cues.get("secondary_desc",""))

    st.divider()

    col1, col2 = st.columns(2)

    col1.metric("Miss Pattern", cues.get("miss_bias","-"))
    col2.metric("Session Momentum", cues.get("momentum","-"))
