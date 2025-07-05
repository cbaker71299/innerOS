import streamlit as st
import pandas as pd
from datetime import datetime
import os

LOG_FILE = "data/user_logs.csv"

if not os.path.exists(LOG_FILE):
    df = pd.DataFrame(columns=["date", "mood", "energy", "goal", "notes"])
    df.to_csv(LOG_FILE, index=False)

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

if st.checkbox("Show Past Logs"):
    df = pd.read_csv(LOG_FILE)
    st.dataframe(df.tail(10))
