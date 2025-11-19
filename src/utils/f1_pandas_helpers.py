import pandas as pd
import src.preprocessing.telemetry_cleaning as telemetry_cleaning

def filter_driver_lap_data(df, safety_car_laps=[]):
    """
    Filters dataframe of all laps for a single driver based on control parameters and data accuracy of Fast-F1 API.
    """
    df = df.copy()

    df['LapNumber'] = df['LapNumber'].astype(int)

    if safety_car_laps:
        df = df[~df['LapNumber'].isin(safety_car_laps)]
    
    df = df.drop([
        'Stint', 'PitOutTime', 'PitInTime', 'SpeedI1', 'SpeedI2', 'SpeedFL',
        'SpeedST', 'IsPersonalBest', 'TyreLife', 'FreshTyre',
        'Team', 'LapStartDate', 'TrackStatus', 'Position', 'Deleted', 'DeletedReason',
        'FastF1Generated'
    ], axis=1)

    df = df[df['IsAccurate'] == True]

    required_sector_cols = [
    'Sector1SessionTime',
    'Sector2SessionTime',
    'Sector3SessionTime'
    ]

    df = df[~df[required_sector_cols].isna().any(axis=1)]

    return df

def get_valid_lap_telemetry(df):
    """
    Returns list of telemetry dataframes for all valid laps for a single driver.
    """
    all_telemetry_list = []

    for lap in df.iterlaps():
        telemetry = lap[1].get_telemetry().copy()
        telemetry['LapNumber'] = lap[1].LapNumber
        all_telemetry_list.append(telemetry)

    return all_telemetry_list

def get_valid_lap_sector_timestamps(laps):
    """
    Returns a dictionary with LapNumber as keys and sector start/end timestamps as values.
    `laps` should be a FastF1 Laps object.
    """
    sector_timestamps = {}

    for lap in laps.iterlaps():
        s1_start = lap[1].Sector1SessionTime - lap[1].Sector1Time
        s1_end_s2_start = lap[1].Sector1SessionTime
        s2_end_s3_start = lap[1].Sector2SessionTime
        s3_end = lap[1].Sector3SessionTime

        sector_timestamps[lap[1].LapNumber] = {
            'Sector1Start': s1_start,
            'Sector1End_Sector2Start': s1_end_s2_start,
            'Sector2End_Sector3Start': s2_end_s3_start,
            'Sector3End': s3_end
        }

    return sector_timestamps


def filter_timestamp_range(df, start, end, timestamp_col='SessionTime'):
    """
    Returns rows in df where timestamp_col is between start and end (inclusive).
    
    Parameters:
        df (pd.DataFrame): The dataframe to filter.
        start: Start timestamp (same type as df[timestamp_col]).
        end: End timestamp (same type as df[timestamp_col]).
        timestamp_col (str): Name of the timestamp column.
        
    Returns:
        pd.DataFrame: Filtered dataframe.
    """
    return df[(df[timestamp_col] >= start) & (df[timestamp_col] <= end)]

def get_fastest_and_second_fastest_lap_details(df):
    """
    Returns sector end timestamps for the fastest lap and, if it exists, the second fastest lap,
    while preserving session order to correctly reference previous lap timestamps.
    If all remaining laps after the fastest are NaT, only the fastest lap is returned.
    If there is no valid second fastest lap, returns None for second_fastest_lap.
    """
    df = df.copy()

    fastest_idx = df['LapTime'].idxmin()
    fastest_lap = df.loc[fastest_idx]

    prev_fastest_idx = fastest_idx - 1
    prev_fastest_lap = df.loc[prev_fastest_idx] if prev_fastest_idx in df.index else None

    fastest_previous_sector3_end = (
        prev_fastest_lap['Sector3SessionTime'] if prev_fastest_lap is not None else None
    )

    fastest_details = {
        "lap_index": fastest_idx,
        "previous_sector3_end": fastest_previous_sector3_end,
        "sector1_end": fastest_lap['Sector1SessionTime'],
        "sector2_end": fastest_lap['Sector2SessionTime'],
        "sector3_end": fastest_lap['Sector3SessionTime']
    }

    df_no_fastest = df.drop(index=fastest_idx)

    # If all remaining laps after the fastest are NaT or there are no laps left, only the fastest lap is returned
    if df_no_fastest.empty or df_no_fastest['LapTime'].isna().all():
        return {"fastest_lap": fastest_details, "second_fastest_lap": None}

    # Find second fastest lap
    valid_laps = df_no_fastest.dropna(subset=['LapTime'])
    if valid_laps.empty:
        return {"fastest_lap": fastest_details, "second_fastest_lap": None}

    second_fastest_idx = valid_laps['LapTime'].idxmin()
    second_fastest_lap = df.loc[second_fastest_idx]

    prev_second_idx = second_fastest_idx - 1
    prev_second_lap = df.loc[prev_second_idx] if prev_second_idx in df.index else None

    second_previous_sector3_end = (
        prev_second_lap['Sector3SessionTime'] if prev_second_lap is not None else None
    )

    second_details = {
        "lap_index": second_fastest_idx,
        "previous_sector3_end": second_previous_sector3_end,
        "sector1_end": second_fastest_lap['Sector1SessionTime'],
        "sector2_end": second_fastest_lap['Sector2SessionTime'],
        "sector3_end": second_fastest_lap['Sector3SessionTime']
    }

    return {
        "fastest_lap": fastest_details,
        "second_fastest_lap": second_details
    }

def extract_driver_fastest_and_second_fastest_sector3_telemetry(session, driver, qualifying_sessions, corner_position_cleaned=None, critical_turn=None, radius=None):
    """
    Extracts and cleans fastest and second fastest sector 3 telemetry and corner telemetry for a given driver
    for all provided qualifying sessions (e.g., ['q2', 'q3']).
    Returns:
        pd.DataFrame: DataFrame with columns for qualifying session, lap type, and telemetry data.
    """
    q1, q2, q3 = session.get_laps(driver).split_qualifying_sessions()
    session_map = {'q1': q1, 'q2': q2, 'q3': q3}
    records = []

    for qual in qualifying_sessions:
        qual_session = session_map.get(qual)
        if qual_session is None or len(qual_session) == 0:
            continue

        driver_telemetry = session.get_telemetry(qual_session)

        fastest_details = get_fastest_and_second_fastest_lap_details(qual_session)["fastest_lap"]
        fastest_sector_2_end = str(fastest_details["sector2_end"])
        fastest_sector_3_end = str(fastest_details["sector3_end"])

        fastest_sector3_telemetry = filter_timestamp_range(driver_telemetry, start=fastest_sector_2_end, end=fastest_sector_3_end)
        fastest_sector3_telemetry_cleaned = telemetry_cleaning.clean_driver_sector_telemetry(fastest_sector3_telemetry, driver)
        fastest_corner_telemetry = telemetry_cleaning.filter_corner_telemetry(fastest_sector3_telemetry_cleaned, corner_position_cleaned, critical_turn[0], radius)
        records.append({
            'qualifying_session': qual,
            'lap_type': 'fastest',
            'telemetry': fastest_corner_telemetry
        })

        second_fastest_details = get_fastest_and_second_fastest_lap_details(qual_session)["second_fastest_lap"]
        if second_fastest_details is not None:
            second_fastest_sector_2_end = str(second_fastest_details["sector2_end"])
            second_fastest_sector_3_end = str(second_fastest_details["sector3_end"])

            second_fastest_sector3_telemetry = filter_timestamp_range(driver_telemetry, start=second_fastest_sector_2_end, end=second_fastest_sector_3_end)
            second_fastest_sector3_telemetry_cleaned = telemetry_cleaning.clean_driver_sector_telemetry(second_fastest_sector3_telemetry, driver)
            second_fastest_corner_telemetry = telemetry_cleaning.filter_corner_telemetry(second_fastest_sector3_telemetry_cleaned, corner_position_cleaned, critical_turn[0], radius)
            records.append({
                'qualifying_session': qual,
                'lap_type': 'second_fastest',
                'telemetry': second_fastest_corner_telemetry
            })

    return pd.DataFrame(records)

def get_driver_eda_stats(df, driver, critical_turn,
                           speed='Speed (m/s)',
                           accel='Acceleration (m/s²)',
                           jerk='Jerk (m/s³)',
                           g_force='G-force (g)',
                           gear='nGear',
                           throttle='Throttle (%)',
                           brake='BrakesApplied'):
    """
    Returns a DataFrame with basic EDA summary statistics for primary telemetry features of a driver.
    """
    rows = len(df)

    summary = {
        'Driver': driver,
        'Turn': critical_turn,
        'RowCount': rows,
        'MaxSpeed': df[speed].max(),
        'MeanSpeed': df[speed].mean(),
        'MedianSpeed': df[speed].median(),
        'SDSpeed': df[speed].std(),
        'MaxAccel': df[accel].max(),
        'MeanAccel': df[accel].mean(),
        'MedianAccel': df[accel].median(),
        'SDAccel': df[accel].std(),
        # 'MaxJerk': df[jerk].max(),
        # 'MeanJerk': df[jerk].mean(),
        # 'MedianJerk': df[jerk].median(),
        # 'SDJerk': df[jerk].std(),
        'MaxGs': df[g_force].max(),
        'MeanGs': df[g_force].mean(),
        'MedianGs': df[g_force].median(),
        'SDGs': df[g_force].std(),
        'GearShifts': (df[gear] != df[gear].shift()).sum() - 1,
        'ThrottleEvents': ((df[throttle] > 0) & (df[throttle].shift(fill_value=0) == 0)).sum(),
        'MeanThrottle': df[throttle].mean(),
        'SDThrottle': df[throttle].std(),
        'BrakeEvents': ((df[brake] == 1) & (df[brake].shift(fill_value=0) == 0)).sum()
    }

    summary_df = pd.DataFrame([summary])

    return summary_df