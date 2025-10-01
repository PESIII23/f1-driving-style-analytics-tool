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

def get_row_count(df):
    """
    Returns the number of rows in the dataframe.
    """
    return len(df)

def print_eda_summary(df, column):
    """
    Prints mean, median, and standard deviation for the specified column in a clean block.
    """
    mean = df[column].mean()
    median = df[column].median()
    stdev = df[column].std()
    print(f"--- EDA Summary for '{column}' ---")
    print(f"Mean   : {mean:.3f}")
    print(f"Median : {median:.3f}")
    print(f"StdDev : {stdev:.3f}")
    print("-------------------------------")