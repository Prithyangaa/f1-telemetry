import streamlit as st
import fastf1
from telemetry import load_lap_telemetry
from plots import plot_comparison
from utils import setup

# Setup
setup()

st.title("F1 Comparative Telemetry Tool")

# Sidebar: year and GP
year = st.sidebar.number_input("Year", min_value=2018, max_value=2025, value=2023)

# Load all events for that year
schedule = fastf1.get_event_schedule(year)
gp_names = schedule['EventName'].tolist()

gp_name = st.sidebar.selectbox("Grand Prix", gp_names, index=gp_names.index("Italian Grand Prix"))
session_type = st.sidebar.selectbox("Session Type", ["Q", "R", "FP1", "FP2", "FP3"])

# Load session for dropdown drivers
session = fastf1.get_session(year, gp_name, session_type)
session.load()

# Driver dropdown setup
driver_options = {}
for drv in session.drivers:
    info = session.get_driver(drv)
    code = info['Abbreviation']
    name = f"{info['FullName']} ({info['TeamName']})"
    driver_options[name] = code

channels = st.sidebar.multiselect(
    "Telemetry Channels",
    ["Speed", "Throttle", "Brake", "nGear"],
    default=["Speed", "Throttle", "Brake"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Driver A")
driver_a_name = st.sidebar.selectbox("Driver A", list(driver_options.keys()))
lap_a = st.sidebar.number_input("Lap Number A", min_value=1, value=1)

st.sidebar.markdown("### Driver B")
driver_b_name = st.sidebar.selectbox("Driver B", list(driver_options.keys()), index=1)
lap_b = st.sidebar.number_input("Lap Number B", min_value=1, value=1)

driver_a = driver_options[driver_a_name]
driver_b = driver_options[driver_b_name]

# Load and compare
if st.sidebar.button("Compare Laps"):
    try:
        telemetries = {}

        lap_a_data = load_lap_telemetry(year, gp_name, session_type, driver_a, lap_a)
        lap_b_data = load_lap_telemetry(year, gp_name, session_type, driver_b, lap_b)

        telemetries[f"{driver_a} Lap {lap_a}"] = lap_a_data["telemetry"]
        telemetries[f"{driver_b} Lap {lap_b}"] = lap_b_data["telemetry"]

        figs = plot_comparison(telemetries, channels)

        for fig in figs:
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")
