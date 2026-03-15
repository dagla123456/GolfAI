"""
GolfAI Session History
Version: v1.0

Stores session summaries and prevents duplicate entries.
Adds:
- timestamp support
- chronological ordering
- session validation
- optional history size limit
"""

import json
import os
from datetime import datetime

HISTORY_FILE = "session_history.json"

MAX_HISTORY = 200


# -----------------------------------------
# Load history
# -----------------------------------------
def load_history():

    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, "r") as f:
        history = json.load(f)

    # ensure chronological order
    history.sort(key=lambda x: x.get("timestamp", ""))

    return history


# -----------------------------------------
# Validate session structure
# -----------------------------------------
def validate_session(summary):

    required_fields = [
        "session_id",
        "timestamp",
        "performance_score",
        "blueprint_match_pct",
        "lowpoint_score",
        "corridor_pct",
        "strike_quality",
    ]

    for field in required_fields:
        if field not in summary:
            return False

    return True


# -----------------------------------------
# Save session
# -----------------------------------------
def save_session_summary(summary):

    history = load_history()

    if not validate_session(summary):
        return history

    session_id = summary.get("session_id")

    for session in history:
        if session.get("session_id") == session_id:
            return history

    history.append(summary)

    # enforce max history size
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]

    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

    return history


# -----------------------------------------
# Last N sessions
# -----------------------------------------
def last_sessions(n=5):

    history = load_history()

    return history[-n:]


# -----------------------------------------
# Create session ID
# -----------------------------------------
def generate_session_id():

    return datetime.utcnow().strftime("%Y%m%d_%H%M%S")
