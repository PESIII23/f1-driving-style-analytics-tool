import pandas as pd

def clean_driver_sector_telemetry(df, driver: str):
    """
    Cleans and standardizes a telemetry dataframe for a single driver and sector.
    - Adds a 'DriverCode' column for identification.
    - Drops unnecessary columns to reduce dataset size.
    - Renames columns for clarity and consistent units.
    - Converts speed from km/h to mph.
    - Converts timestamps to strings and removes '0 days ' for easier parsing.
    Returns the cleaned dataframe.
    """
    df.insert(0, 'DriverCode', driver)
    df = df.drop(['Date', 'DriverAhead', 'DistanceToDriverAhead', 'DRS', 'Source', 'RelativeDistance', 'Status'], axis=1)
    df = df.rename(columns={'SessionTime': 'SessionTime (s)', 'Time': 'SectorTime (s)', 'Speed': 'Speed (mph)', 'Throttle': 'Throttle (%)', 
                            'Brake': 'BrakesApplied', 'Distance': 'Distance (m)', 'X': 'X (1/10 m)', 'Y': 'Y (1/10 m)', 'Z': 'Z (1/10 m)'})
    df['Speed (mph)'] = df['Speed (mph)'] * 0.6213711922 # conversion for km/h to mph
    df['SessionTime (s)'] = df['SessionTime (s)'].astype(str).str.replace('0 days ', '')
    df['SectorTime (s)'] = df['SectorTime (s)'].astype(str).str.replace('0 days ', '')

    return df

# def find_steering_wheel_angle():
    # code here