import fastf1

def load_lap_telemetry(year, gp_name, session_type, driver, lap_number):
    """
    Load telemetry data for a given driver and lap.
    """
    session = fastf1.get_session(year, gp_name, session_type)
    session.load()

    driver_laps = session.laps.pick_drivers(driver)
    lap = driver_laps.loc[driver_laps['LapNumber'] == lap_number]

    if lap.empty:
        raise ValueError(f"No lap {lap_number} found for {driver}")

    lap = lap.iloc[0]
    tel = lap.get_car_data().add_distance()

    return {
        "lap": lap,
        "telemetry": tel
    }
