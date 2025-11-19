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