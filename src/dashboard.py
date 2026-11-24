
from pathlib import Path

import pandas as pd
import streamlit as st
import plotly.express as px

from database import BatteryDatabase
from fault_detection import BatteryFaultDetector


st.set_page_config(
    page_title="EV Battery Digital Twin",
    page_icon="🔋",
    layout="wide",
)

st.title("EV Battery Digital Twin")
st.caption("CAN-Based Battery Monitoring and Fault Detection")

project = Path(__file__).resolve().parents[1]
db_path = project / "data" / "battery_full.db"

if not db_path.exists():
    st.error("Battery database not found.")
    st.stop()

database = BatteryDatabase(db_path)

df = pd.DataFrame(
    database.fetch_all(),
    columns=[
        "time_s",
        "voltage_V",
        "current_A",
        "soc_pct",
        "temperature_C",
        "soh_pct",
    ],
)

if df.empty:
    st.warning("No battery measurements available.")
    st.stop()

latest = df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

col1.metric("SOC", f"{latest['soc_pct']:.1f}%")
col2.metric("Voltage", f"{latest['voltage_V']:.1f} V")
col3.metric("Temperature", f"{latest['temperature_C']:.1f} °C")
col4.metric("SOH (simulated)", f"{latest['soh_pct']:.1f}%")

st.subheader("Battery Monitoring")

signals = {
    "soc_pct": "State of Charge (%)",
    "voltage_V": "Pack Voltage (V)",
    "current_A": "Pack Current (A)",
    "temperature_C": "Pack Temperature (°C)",
}

for signal, label in signals.items():
    fig = px.line(
        df,
        x="time_s",
        y=signal,
        title=label,
        markers=True,
        labels={
            "time_s": "Simulation Time (s)",
            signal: label,
        },
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Battery Fault Detection")

detector = BatteryFaultDetector()
faults = detector.check(latest.to_dict())

if not faults:
    st.success("Battery status: NORMAL")
else:
    for fault in faults:
        message = f"{fault['code']}: {fault['message']}"

        if fault["severity"] == "CRITICAL":
            st.error(message)
        else:
            st.warning(message)

st.subheader("Decoded CAN Measurements")
st.dataframe(df)

st.caption(
    "Simulation-based educational prototype. "
    "Not validated for real vehicle operation."
)
