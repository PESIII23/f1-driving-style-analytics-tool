import pandas as pd

def clean_driver_telemetry(df, driver: str):
    """
    Clean and standardize a telemetry dataframe for a single driver.
    - Adds a 'DriverCode' column for identification.
    - Drops unnecessary columns (ignored if missing).
    - Renames columns for clarity and consistent units.
    - Converts speed from km/h to m/s (if present).
    - Converts 'BrakesApplied' to integer type (if present).
    Returns the cleaned dataframe copy.
    """
    df = df.copy()
    df.insert(0, 'DriverCode', driver)

    df = df.drop([
        'Date', 'DriverAhead', 'DistanceToDriverAhead',
        'DRS', 'Source', 'RelativeDistance', 'Status'
    ], axis=1, errors='ignore')

    df = df.rename(columns={
        'SessionTime': 'SessionTime (s)',
        'Time': 'SectorTime (s)',
        'Speed': 'Speed (m/s)',
        'Throttle': 'Throttle (%)',
        'Brake': 'BrakesApplied',
        'Distance': 'Distance (m)',
        'X': 'X (1/10 m)',
        'Y': 'Y (1/10 m)',
        'Z': 'Z (1/10 m)'
    })

    # conversion of km/h to m/s (handle non-numeric safely)
    if 'Speed (m/s)' in df.columns:
        df['Speed (m/s)'] = pd.to_numeric(df['Speed (m/s)'], errors='coerce') * 0.277778

    if 'BrakesApplied' in df.columns:
        df['BrakesApplied'] = pd.to_numeric(df['BrakesApplied'], errors='coerce').fillna(0).astype(int)

    return df

def clean_circuit_corner_data(df):
    """
    Return circuit data with cleaned column names and removed extras.
    """
    df = df.drop([
        'Letter'
    ], axis=1)

    df = df.rename(columns={
        'Number': 'Turn',
        'X': 'X (1/10 m)', 
        'Y': 'Y (1/10 m)',
        'Angle': 'Angle (°)',
        'Distance': 'Distance (1/10 m)'
    })

    cols = df.columns.tolist()
    cols.remove('Turn')
    cols.insert(0, 'Turn')
    df = df[cols]

    return df

def filter_corner_telemetry(telemetry_df, circuit_df, turn: int, radius: int):
   """
   Return filtered telemetry points on or within a circular radius of a given turn.

   Parameters:
   - telmetry_df: pd.Dataframe containing driver telemetry for given session
   - circuit_df: pd.Dataframe containing circuit data
   - turn: int, number of turn on circuit
   - radius: int, 
   """
   turn_data = circuit_df.loc[circuit_df['Turn'] == turn]
   turn_x_pos = turn_data['X (1/10 m)'].iloc[0]
   turn_y_pos = turn_data['Y (1/10 m)'].iloc[0]

   # equation of circle in Cartesian coordinates
   corner_telemetry = telemetry_df[
       ((telemetry_df['X (1/10 m)'] - turn_x_pos)**2 + 
        (telemetry_df['Y (1/10 m)'] - turn_y_pos)**2) <= radius**2]
   
   return corner_telemetry