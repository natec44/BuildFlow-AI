import streamlit as st
import pandas as pd
import datetime
import plotly.express as px
import requests

# Configurations
OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "your_openweather_api_key_here")

def get_weather_forecast(city="New York"):
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        forecast = response.json()
        rain_days = [
            item["dt_txt"].split(" ")[0]
            for item in forecast["list"]
            if "rain" in item and item["rain"].get("3h", 0) > 0
        ]
        return set(rain_days)
    return set()

# Simulated progress API endpoint
def get_site_progress():
    return {
        "Foundation": "complete",
        "Framing": "delayed",
        "Roofing": "on_schedule"
    }

st.set_page_config(page_title="BuildFlow AI", layout="wide")
st.title("🏗️ BuildFlow AI — Real-Time Scheduler")
st.markdown("Upload your construction schedule and simulate disruptions with live data.")

uploaded_file = st.file_uploader("📂 Upload Construction Schedule (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["Start", "End"])
    st.subheader("🗂️ Original Schedule")
    st.dataframe(df)

    df["Duration"] = (df["End"] - df["Start"]).dt.days
    df["RiskScore"] = 0.0

    city = st.text_input("Enter your construction site city:", "New York")
    rain_days = get_weather_forecast(city)
    progress_status = get_site_progress()

    for index, row in df.iterrows():
        task = row["Task"]
        if progress_status.get(task) == "delayed":
            df.at[index, "RiskScore"] += 30
        task_days = pd.date_range(row["Start"], row["End"]).strftime('%Y-%m-%d')
        if any(day in rain_days for day in task_days):
            df.at[index, "RiskScore"] += 40

    st.subheader("📋 Schedule with Real-Time Risk Scores")
    st.dataframe(df)

    st.subheader("📆 Gantt Chart")
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="End",
        y="Task",
        color="RiskScore",
        color_continuous_scale="OrRd",
        title="Live Construction Timeline"
    )
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    st.download_button(
        label="⬇️ Download Updated Schedule",
        data=df.to_csv(index=False),
        file_name="updated_schedule_with_weather.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV file with columns: `Task`, `Start`, `End`.")

st.markdown("---")
st.caption("🚧 Real-time prototype — BuildFlow AI © 2025")
