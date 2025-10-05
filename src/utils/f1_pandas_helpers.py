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

def get_driver_eda_summary(df, driver, speed='Speed (m/s)', accel='Acceleration (m/s²)', jerk='Jerk (m/s³)', g_force='G-force (g)', gear='nGear', throttle='Throttle (%)', brake='BrakesApplied'):
    """
    Prints basic EDA summary statistics for primary telemetry features of a driver.
    
    Parameters:
    - df (pd.DataFrame): containing driver telemetry.
    - driver (str): driver name or identifier.
    - speed (str): column name for speed.
    - accel (str): column name for acceleration.
    - jerk (str): column name for jerk.
    - g_force (str): column name for g-force
    - gear (str): column name for gear.
    - throttle (str): column name for throttle.
    - brake (str): column name for brake.
    """
    rows = len(df)

    max_speed = df[speed].max()
    mean_speed = df[speed].mean()
    median_speed = df[speed].median()
    stdev_speed = df[speed].std()

    max_accel = df[accel].max()
    mean_accel = df[accel].mean()
    median_accel = df[accel].median()
    stdev_accel = df[accel].std()

    max_jerk = df[jerk].max()
    mean_jerk = df[jerk].mean()
    median_jerk = df[jerk].median()
    stdev_jerk = df[jerk].std()

    max_g_force = df[g_force].max()
    mean_g_force = df[g_force].mean()
    median_g_force = df[g_force].median()
    stdev_g_force = df[g_force].std()

    brake_events = ((df[brake] == 1) & (df[brake].shift(fill_value=0) == 0)).sum()

    gear_shifts = (df[gear] != df[gear].shift()).sum() - 1

    throttle_events = ((df[throttle] > 0) & (df[throttle].shift(fill_value=0) == 0)).sum()
    mean_throttle = df[throttle].mean()
    stdev_throttle = df[throttle].std()

    print(f"--- EDA Summary for {driver} ---")
    print(f"Row Count: {rows}\n")

    print(f"{speed} -->")
    print(f"Max   : {max_speed:.6f}")
    print(f"Mean  : {mean_speed:.6f}")
    print(f"Median: {median_speed:.6f}")
    print(f"StdDev: {stdev_speed:.6f}\n")

    print(f"{accel} -->")
    print(f"Max   : {max_accel:.6f}")
    print(f"Mean  : {mean_accel:.6f}")
    print(f"Median: {median_accel:.6f}")
    print(f"StdDev: {stdev_accel:.6f}\n")

    print(f"{jerk} -->")
    print(f"Max   : {max_jerk:.6f}")
    print(f"Mean  : {mean_jerk:.6f}")
    print(f"Median: {median_jerk:.6f}")
    print(f"StdDev: {stdev_jerk:.6f}\n")

    print(f"{g_force} -->")
    print(f"Max   : {max_g_force:.6f}")
    print(f"Mean  : {mean_g_force:.6f}")
    print(f"Median: {median_g_force:.6f}")
    print(f"StdDev: {stdev_g_force:.6f}\n")

    print(f"{gear} -->")
    print(f"Shifts: {gear_shifts}\n")

    print(f"{throttle} -->")
    print(f"Events: {throttle_events}")
    print(f"Mean  : {mean_throttle:.6f}")
    print(f"StdDev: {stdev_throttle:.6f}\n")

    print(f"{brake} -->")
    print(f"Events: {brake_events}\n")
