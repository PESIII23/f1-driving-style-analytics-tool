import pandas as pd

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

import pandas as pd

def get_fastest_and_second_fastest_lap_details(df):
    """
    Returns sector end timestamps for the fastest lap and, if it exists, the second fastest lap,
    while preserving session order to correctly reference previous lap timestamps.
    If all remaining laps after the fastest are NaT, only the fastest lap is returned.
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

    if df_no_fastest['LapTime'].isna().all():
        return {"fastest_lap": fastest_details}

    second_fastest_idx = df_no_fastest['LapTime'].idxmin()
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

def get_driver_eda_summary(df, driver, critical_turn, feature_df,
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
        # 'Turn': critical_turn,
        # 'RowCount': rows,
        # 'MaxSpeed': df[speed].max(),
        'MeanSpeed': df[speed].mean(),
        # 'MedianSpeed': df[speed].median(),
        'SDSpeed': df[speed].std(),
        'MaxAccel': df[accel].max(),
        # 'MeanAccel': df[accel].mean(),
        # 'MedianAccel': df[accel].median(),
        'SDAccel': df[accel].std(),
        # 'MaxJerk': df[jerk].max(),
        # 'MeanJerk': df[jerk].mean(),
        # 'MedianJerk': df[jerk].median(),
        # 'SDJerk': df[jerk].std(),
        'MaxGs': df[g_force].max(),
        # 'MeanGs': df[g_force].mean(),
        # 'MedianGs': df[g_force].median(),
        'SDGs': df[g_force].std(),
        # 'GearShifts': (df[gear] != df[gear].shift()).sum() - 1,
        'ThrottleEvents': ((df[throttle] > 0) & (df[throttle].shift(fill_value=0) == 0)).sum(),
        'MeanThrottle': df[throttle].mean(),
        # 'SDThrottle': df[throttle].std(),
        # 'BrakeEvents': ((df[brake] == 1) & (df[brake].shift(fill_value=0) == 0)).sum()
    }

    summary_df = pd.DataFrame([summary])
    combined_df = pd.concat([summary_df, feature_df.reset_index(drop=True)], axis=1)

    return combined_df