import streamlit as st
import pandas as pd

# Load the data
def load_data():
    df = pd.read_excel("Canceltion Sheet.xlsx", sheet_name="Cancelation Date (Aug)")
    df["Diploma_clean"] = df["Diploma"].astype(str).str.strip().str.lower()
    df["Status"] = df["Statues Of The Compensation"].astype(str).str.strip().str.lower()
    return df

df = load_data()

st.title("📊 Diploma Cancelation Dashboard")

# Sidebar: choose diploma track
tracks = sorted(df["Diploma_clean"].unique())
selected_track = st.sidebar.selectbox("اختر التراك", tracks)

# Filter data by track
track_df = df[df["Diploma_clean"] == selected_track].copy()

# Overall stats
total_cancelations = len(track_df)
compensated_count = (track_df["Status"] == "compensated").sum()
not_compensated_count = (track_df["Status"] == "not compensated").sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Cancelations", total_cancelations)
with col2:
    st.metric("Compensated Sessions", compensated_count)
with col3:
    st.metric("Not Compensated Sessions", not_compensated_count)

# Instructor stats
st.subheader(f"{selected_track.title()} — Instructor Cancelation & Compensation")
instructor_stats = track_df.groupby("Instructor Name")["Status"].value_counts().unstack(fill_value=0)
st.dataframe(instructor_stats)
st.bar_chart(instructor_stats)

# ------------------- Data Analysis View (with filters) -------------------
st.subheader("🔎 Advanced Filters")
selected_instructor = st.multiselect("Select Instructor", sorted(track_df["Instructor Name"].unique()))
selected_status = st.multiselect("Select Status", sorted(track_df["Status"].unique()))

filtered_df = track_df.copy()
if selected_instructor:
    filtered_df = filtered_df[filtered_df["Instructor Name"].isin(selected_instructor)]
if selected_status:
    filtered_df = filtered_df[filtered_df["Status"].isin(selected_status)]

# Stats after filtering
total_cancelations = len(filtered_df)
compensated_count = (filtered_df["Status"] == "compensated").sum()
not_compensated_count = (filtered_df["Status"] == "not compensated").sum()

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Cancelations", total_cancelations)
with col2:
    st.metric("Compensated Sessions", compensated_count)
with col3:
    st.metric("Not Compensated Sessions", not_compensated_count)

st.subheader("Instructor Cancelation & Compensation (Filtered)")
instructor_stats = filtered_df.groupby("Instructor Name")["Status"].value_counts().unstack(fill_value=0)
st.dataframe(instructor_stats)
st.bar_chart(instructor_stats)

import pandas as pd
import openpyxl

print("Pandas version:", pd.__version__)
print("openpyxl version:", openpyxl.__version__)