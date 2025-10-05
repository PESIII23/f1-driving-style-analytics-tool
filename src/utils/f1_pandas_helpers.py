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

def get_driver_eda_summary(df, driver, critical_turn,
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
        'Max Speed': df[speed].max(),
        'Mean Speed': df[speed].mean(),
        'Median Speed': df[speed].median(),
        'SD Speed': df[speed].std(),
        'Max Accel': df[accel].max(),
        'Mean Accel': df[accel].mean(),
        'Median Accel': df[accel].median(),
        'SD Accel': df[accel].std(),
        'Max Jerk': df[jerk].max(),
        'Mean Jerk': df[jerk].mean(),
        'Median Jerk': df[jerk].median(),
        'SD Jerk': df[jerk].std(),
        'Max Gs': df[g_force].max(),
        'Mean Gs': df[g_force].mean(),
        'Median Gs': df[g_force].median(),
        'SD Gs': df[g_force].std(),
        'Gear Shifts': (df[gear] != df[gear].shift()).sum() - 1,
        'Throttle Events': ((df[throttle] > 0) & (df[throttle].shift(fill_value=0) == 0)).sum(),
        'Mean Throttle': df[throttle].mean(),
        'SD Throttle': df[throttle].std(),
        'Brake Events': ((df[brake] == 1) & (df[brake].shift(fill_value=0) == 0)).sum()
    }

    return pd.DataFrame([summary])


def get_driver_eda_multiple_turns(driver, turn_dfs):
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
        summary_df = get_driver_eda_summary(turn_df, driver, turn)
        summaries.append(summary_df)

    if summaries:
        return pd.concat(summaries, ignore_index=True)
    else:
        return pd.DataFrame()
