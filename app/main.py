import streamlit as st
import pandas as pd
from datetime import datetime
import os

LOG_FILE = "data/user_logs.csv"

# Create data folder and log file if they don't exist
if not os.path.exists("data"):
    os.makedirs("data")

if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["date", "mood", "energy", "goal", "notes"])
    df.to_csv(LOG_FILE, index=False)

# -----------------------------
# App UI
# -----------------------------

st.title("🌱 innerOS – Self-Mastery Logger")

mood = st.slider("How is your mood today? (1-10)", 1, 10, 5)
energy = st.slider("Energy level today? (1-10)", 1, 10, 5)
goal = st.text_input("Main goal/focus today:")
notes = st.text_area("Any other notes or thoughts?")

if st.button("Log Entry"):
    new_entry = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "mood": mood,
        "energy": energy,
        "goal": goal,
        "notes": notes
    }])

    df = pd.read_csv(LOG_FILE)
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)
    st.success("Logged successfully!")

# -----------------------------
# View Past Logs + Trends
# -----------------------------

if st.checkbox("Show Past Logs & Trends"):
    st.markdown("---")
    st.subheader("📈 Mood & Energy Trends")

    df = pd.read_csv(LOG_FILE)

    if not df.empty:
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        mood_chart = df[["date", "mood"]].set_index("date")
        energy_chart = df[["date", "energy"]].set_index("date")

        st.line_chart(mood_chart, use_container_width=True)
        st.line_chart(energy_chart, use_container_width=True)

        st.markdown("### 📋 Recent Logs")
        st.dataframe(df.tail(10))
    else:
        st.info("You need at least one log to show trends.")
