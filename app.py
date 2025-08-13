import streamlit as st
import json
import csv
from datetime import datetime
import os

# ===== CONFIG =====
EXPORT_DIR = "exported_logs"
os.makedirs(EXPORT_DIR, exist_ok=True)

hide_streamlit_style = """
<style>
/* Ẩn header */
header {visibility: hidden;}
/* Ẩn footer "Made with Streamlit" */
footer {visibility: hidden;}
</style>
"""
st.set_page_config(
    page_title="AI Conversation Review",
    layout="centered"
)
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ===== SESSION STATE =====
if "recording" not in st.session_state:
    st.session_state.recording = False
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "tags" not in st.session_state:
    st.session_state.tags = []
if "notes" not in st.session_state:
    st.session_state.notes = ""

# ===== UI TITLE =====
st.title("🎙 AI Conversation Review Tool")

# ===== SESSION CONTROL =====
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔘 Start Session", disabled=st.session_state.recording):
        st.session_state.recording = True
        st.session_state.transcript = ""  # reset
        st.session_state.tags = []
        st.session_state.notes = ""
        st.success("Recording started... (placeholder)")
with col2:
    if st.button("🔘 End Session", disabled=not st.session_state.recording):
        st.session_state.recording = False
        # Simulate AI transcription + tagging
        st.session_state.transcript = "Customer: Hi, I'm looking for running shoes.\nStaff: Sure, do you have a size in mind?\n..."
        st.session_state.tags = ["running_shoes", "size_inquiry", "in_store"]
        st.success("Recording stopped. Transcript & tags generated.")

# ===== TRANSCRIPT DISPLAY =====
st.subheader("📝 Transcript")
st.text_area("Transcribed Conversation", st.session_state.transcript, height=200, disabled=True)

# ===== TAG EDITING =====
st.subheader("🏷️ Tags")
edited_tags = st.text_input(
    "Edit Tags (comma separated)",
    value=", ".join(st.session_state.tags)
)

# ===== NOTES =====
st.subheader("🗒 Notes / Comments")
notes = st.text_area("Optional notes", value=st.session_state.notes, height=100)

# ===== CONFIRM & EXPORT =====
if st.button("✅ Confirm & Export", disabled=(not st.session_state.transcript)):
    st.session_state.tags = [t.strip() for t in edited_tags.split(",") if t.strip()]
    st.session_state.notes = notes
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Prepare data
    export_data = {
        "timestamp": timestamp,
        "transcript": st.session_state.transcript,
        "tags": st.session_state.tags,
        "notes": st.session_state.notes
    }

    # Save JSON
    json_path = os.path.join(EXPORT_DIR, f"session_{timestamp}.json")
    with open(json_path, "w", encoding="utf-8") as jf:
        json.dump(export_data, jf, ensure_ascii=False, indent=2)

    # Save CSV
    csv_path = os.path.join(EXPORT_DIR, f"session_{timestamp}.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as cf:
        writer = csv.writer(cf)
        writer.writerow(["timestamp", "transcript", "tags", "notes"])
        writer.writerow([timestamp, st.session_state.transcript, ";".join(st.session_state.tags), st.session_state.notes])

    st.success(f"Session saved to {json_path} and {csv_path}")

# ===== FOOTER =====
st.caption("Local AI review UI — prototype using Streamlit")
