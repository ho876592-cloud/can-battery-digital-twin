
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

st.title("🔋 EV Battery Digital Twin")
st.caption("CAN-Based Battery Monitoring & Diagnostics")

project = Path(__file__).resolve().parents[1]
db_path = project / "data" / "battery_full.db"

if not db_path.exists():
    st.error("Run pipeline.py to generate the battery database.")
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

first = df.iloc[0]
latest = df.iloc[-1]

# Historical fault detection
detector = BatteryFaultDetector()
fault_events = []

for _, row in df.iterrows():
    for fault in detector.check(row.to_dict()):
        fault_events.append({
            "time_s": row["time_s"],
            **fault
        })

latest_faults = detector.check(latest.to_dict())

if latest_faults:
    st.error("Current battery status: FAULT DETECTED")
else:
    st.success("Current battery status: NORMAL")

# Battery KPI cards
c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "State of Charge",
    f"{latest['soc_pct']:.1f}%",
    f"{latest['soc_pct'] - first['soc_pct']:.1f} pp",
    delta_color="off",
)

c2.metric(
    "Pack Voltage",
    f"{latest['voltage_V']:.1f} V",
    f"{latest['voltage_V'] - first['voltage_V']:.1f} V",
    delta_color="off",
)

c3.metric(
    "Pack Current",
    f"{latest['current_A']:.1f} A",
)

c4.metric(
    "Pack Temperature",
    f"{latest['temperature_C']:.1f} °C",
    f"{latest['temperature_C'] - first['temperature_C']:.1f} °C",
    delta_color="off",
)

st.caption(
    f"SOH: {latest['soh_pct']:.1f}% "
    "(fixed simulated assumption)"
)

st.divider()
st.subheader("Battery Signal Monitoring")


def create_chart(signal, title, color):
    fig = px.line(
        df,
        x="time_s",
        y=signal,
        title=title,
        labels={
            "time_s": "Simulation Time (s)",
            signal: title,
        },
    )

    fig.update_traces(
        line=dict(color=color, width=2)
    )

    fig.update_layout(
        height=300,
        margin=dict(l=10, r=10, t=45, b=10),
        hovermode="x unified",
    )

    return fig


left, right = st.columns(2)

with left:
    st.plotly_chart(
        create_chart("soc_pct", "State of Charge (%)", "#2563EB"),
        use_container_width=True,
    )

    st.plotly_chart(
        create_chart("current_A", "Pack Current (A)", "#8B5CF6"),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        create_chart("voltage_V", "Pack Voltage (V)", "#0891B2"),
        use_container_width=True,
    )

    st.plotly_chart(
        create_chart("temperature_C", "Pack Temperature (°C)", "#EA580C"),
        use_container_width=True,
    )

st.divider()
st.subheader("Communication & Diagnostic Statistics")

s1, s2, s3, s4 = st.columns(4)

s1.metric("Battery Samples", len(df))
s2.metric("Expected CAN Frames", len(df) * 2)
s3.metric(
    "Simulation Duration",
    f"{df['time_s'].max() - df['time_s'].min():.0f} s"
)
s4.metric("Fault Events", len(fault_events))

st.subheader("Battery Fault History")

if fault_events:
    st.dataframe(
        pd.DataFrame(fault_events),
        use_container_width=True,
    )
else:
    st.success("No faults detected in the stored measurements.")

with st.expander("View Decoded CAN Measurements"):
    st.dataframe(df, use_container_width=True)

st.divider()

st.caption(
    "Simulation-based educational prototype | "
    "MATLAB/Simulink | Python | CAN-Bus | DBC | SQLite"
)

st.caption(
    "Not validated for real vehicle operation."
)
