# buildflow_ai.py

import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# Title and description
st.set_page_config(page_title="BuildFlow AI", layout="wide")
st.title("🏗️ BuildFlow AI — Construction Scheduler MVP")
st.markdown("Upload your construction schedule and simulate delays with AI-powered risk scoring.")

# Upload CSV
uploaded_file = st.file_uploader("📂 Upload Construction Schedule (CSV)", type=["csv"])

# Define main logic
if uploaded_file:
    # Read and display original schedule
    df = pd.read_csv(uploaded_file, parse_dates=["Start", "End"])
    st.subheader("🗂️ Original Schedule")
    st.dataframe(df)

    # Add duration and placeholder risk score
    df["Duration"] = (df["End"] - df["Start"]).dt.days
    df["RiskScore"] = 0.0

    # Simulate delay interface
    st.subheader("⏱ Simulate Delay")
    task_to_delay = st.selectbox("Select a task to delay", df["Task"])
    delay_days = st.slider("Delay by how many days?", 0, 10, 2)

    if st.button("Apply Delay"):
        df.loc[df["Task"] == task_to_delay, "Start"] += datetime.timedelta(days=delay_days)
        df.loc[df["Task"] == task_to_delay, "End"] += datetime.timedelta(days=delay_days)
        df["Duration"] = (df["End"] - df["Start"]).dt.days
        df["RiskScore"] = df["Duration"] / df["Duration"].max() * 100  # Naive risk formula

    # Display updated schedule
    st.subheader("📋 Updated Schedule with Risk Scores")
    st.dataframe(df)

    # Gantt chart with Plotly
    st.subheader("📆 Gantt Chart")
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="End",
        y="Task",
        color="RiskScore",
        color_continuous_scale="OrRd",
        title="Construction Timeline"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    # Download updated CSV
    st.download_button(
        label="⬇️ Download Updated Schedule",
        data=df.to_csv(index=False),
        file_name="updated_schedule.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload a CSV file with columns: `Task`, `Start`, `End` (dates in YYYY-MM-DD format).")

# Footer
st.markdown("---")
st.caption("🚧 Prototype version — BuildFlow AI © 2025")
