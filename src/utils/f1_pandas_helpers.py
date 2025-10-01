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

def get_eda_summary(df, driver, speed='Speed (m/s)', gear='nGear', throttle='Throttle (%)', brake='BrakesApplied'):
    """
    Prints basic statistics for primary features in a clean block.
    """
    rows = len(df)

    max_speed = df[speed].max()
    mean_speed = df[speed].mean()
    median_speed = df[speed].median()
    stdev_speed = df[speed].std()

    brake_events = ((df["BrakesApplied"] == 1) & (df["BrakesApplied"].shift(fill_value=0) == 0)).sum()

    gear_shifts = ((df["nGear"]) != (df["nGear"].shift() )).sum() - 1

    throttle_events = ((df["Throttle (%)"] > 0) & (df["Throttle (%)"].shift(fill_value=0) == 0.000000)).sum()
    mean_throttle = df[throttle].mean()
    stdev_throttle = df[throttle].std()

    print(f"--- EDA Summary for {driver} ---")

    print(f"Row Count: {rows}")
    print()

    print(f"{speed} -->")
    print(f"Max   : {max_speed:.6f}")
    print(f"Mean  : {mean_speed:.6f}")
    print(f"Median: {median_speed:.6f}")
    print(f"StdDev: {stdev_speed:.6f}")
    print()

    print(f"{gear} -->")
    print(f"Shifts: {gear_shifts}")
    print()

    print(f"{throttle} -->")
    print(f"Events: {throttle_events}")
    print(f"Mean  : {mean_throttle:.6f}")
    print(f"StdDev: {stdev_throttle:.6f}")
    print()

    print(f"{brake} -->")
    print(f"Events: {brake_events}")
    print()