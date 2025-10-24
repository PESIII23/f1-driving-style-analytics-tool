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

def get_fastest_lap_details(df):
    """
    Returns list of sector end timestamps based on the fastest lap time.
    """
    df = df.copy()

    fastest_lap_idx = df['LapTime'].idxmin()
    fastest_lap = df.loc[fastest_lap_idx]
    previous_lap = df.loc[fastest_lap_idx - 1]

    previous_sector3_end = previous_lap['Sector3SessionTime'] if not previous_lap.empty else None
    fastest_sector1_end = fastest_lap['Sector1SessionTime']
    fastest_sector2_end = fastest_lap['Sector2SessionTime']
    fastest_sector3_end = fastest_lap['Sector3SessionTime']

    sector_timestamps = [previous_sector3_end, fastest_sector1_end, fastest_sector2_end, fastest_sector3_end]
    return sector_timestamps

def get_driver_eda_summary(df, driver, critical_turn, initial_max_brake,
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
        'Row Count': rows,
        'Initial Brake': initial_max_brake,
        # 'Max Speed': df[speed].max(),
        # 'Mean Speed': df[speed].mean(),
        # 'Median Speed': df[speed].median(),
        # 'SD Speed': df[speed].std(),
        # 'Max Accel': df[accel].max(),
        # 'Mean Accel': df[accel].mean(),
        # 'Median Accel': df[accel].median(),
        # 'SD Accel': df[accel].std(),
        # 'Max Jerk': df[jerk].max(),
        # 'Mean Jerk': df[jerk].mean(),
        # 'Median Jerk': df[jerk].median(),
        # 'SD Jerk': df[jerk].std(),
        'Max Gs': df[g_force].max(),
        # 'Mean Gs': df[g_force].mean(),
        # 'Median Gs': df[g_force].median(),
        # 'SD Gs': df[g_force].std(),
        'Gear Shifts': (df[gear] != df[gear].shift()).sum() - 1,
        'Throttle Events': ((df[throttle] > 0) & (df[throttle].shift(fill_value=0) == 0)).sum(),
        # 'Mean Throttle': df[throttle].mean(),
        # 'SD Throttle': df[throttle].std(),
        'Brake Events': ((df[brake] == 1) & (df[brake].shift(fill_value=0) == 0)).sum()
    }

    return pd.DataFrame([summary])


def get_driver_eda_multiple_turns(driver, turn_dfs, initial_max_brake):
    """
    Returns a concatenated dataframe of EDA summaries for multiple turns.
    
    Parameters:
    - driver (str): driver name
    - turn_dfs (list of tuples): [(turn_number, df_for_turn), ...]
    """
    summaries = []

    for turn, turn_df in turn_dfs:
        if len(turn_df) == 0:
            continue
        summary_df = get_driver_eda_summary(turn_df, driver, turn, initial_max_brake)
        summaries.append(summary_df)

    if summaries:
        return pd.concat(summaries, ignore_index=True)
    else:
        return pd.DataFrame()
