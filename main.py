import streamlit as st
import fastf1
import datetime

from telemetry import load_lap_telemetry
from plots import plot_comparison
from utils import setup

# Setup cache
setup()

st.title("F1 Comparative Telemetry Tool")

# --- Sidebar: Season ---
current_year = datetime.datetime.now().year
year = st.sidebar.number_input(
    "Year",
    min_value=2018,
    max_value=current_year,
    value=current_year
)

# --- Sidebar: GP dropdown (only past events) ---
schedule = fastf1.get_event_schedule(year)
schedule = schedule[schedule['EventName'] != 'Preseason Testing']

today = datetime.datetime.now().date()
completed_events = schedule[schedule['EventDate'].dt.date <= today]

gp_names = completed_events['EventName'].tolist()
gp_rounds = completed_events['RoundNumber'].tolist()
gp_dict = dict(zip(gp_names, gp_rounds))

gp_name = st.sidebar.selectbox("Grand Prix", gp_names)

# --- Sidebar: Session type ---
session_type = st.sidebar.selectbox("Session Type", ["Q", "R", "FP1", "FP2", "FP3"])

# --- Load session safely ---
try:
    session = fastf1.get_session(year, gp_dict[gp_name], session_type)
    session.load()
except Exception as e:
    st.error(f"Could not load session: {e}")
    st.stop()

# --- Driver dropdown setup ---
driver_options = {}
for drv in session.drivers:
    info = session.get_driver(drv)
    code = info['Abbreviation']
    name = f"{info['FullName']} ({info['TeamName']})"
    driver_options[name] = code

channels = st.sidebar.multiselect(
    "Telemetry Channels",
    ["Speed", "Throttle", "Brake", "nGear", "DRS", "RPM"],
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

# --- Compare laps ---
if st.sidebar.button("Compare Laps"):
    try:
        telemetries = {}

        lap_a_data = load_lap_telemetry(year, gp_dict[gp_name], session_type, driver_a, lap_a)
        lap_b_data = load_lap_telemetry(year, gp_dict[gp_name], session_type, driver_b, lap_b)

        telemetries[f"{driver_a} Lap {lap_a}"] = lap_a_data["telemetry"]
        telemetries[f"{driver_b} Lap {lap_b}"] = lap_b_data["telemetry"]

        figs = plot_comparison(telemetries, channels)

        for fig in figs:
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {e}")

