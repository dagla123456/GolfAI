"""
GolfAI Cue Engine
Version: v0.1

Builds on-course swing cues from latest session.
"""

from golfai.session_history import load_history
from golfai.cue_library import CUE_LIBRARY


def build_oncourse_cues():
    history = load_history()

    if not history:
        return {
            "has_cues": False,
            "message": "No practice session available."
        }

    latest = history[-1]

    primary_issue = latest.get("primary_issue")
    secondary_issue = latest.get("secondary_issue")

    primary = CUE_LIBRARY.get(primary_issue, {})
    secondary = CUE_LIBRARY.get(secondary_issue, {})

    return {
        "has_cues": True,

        "primary_issue": primary_issue,
        "primary_cue": primary.get("cue"),
        "primary_desc": primary.get("description"),
        "primary_image": primary.get("image"),

        "secondary_issue": secondary_issue,
        "secondary_cue": secondary.get("cue"),
        "secondary_desc": secondary.get("description"),
        "secondary_image": secondary.get("image"),

        "miss_bias": latest.get("miss_bias"),
        "momentum": latest.get("momentum_label")
    }
