import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

def plot_centered_telemetry(df, time_col, telemetry_col, title):
    df_centered = df.copy()
    df_centered[telemetry_col] = pd.to_numeric(df_centered[telemetry_col], errors='coerce')
    df_centered = df_centered.dropna(subset=[telemetry_col])
    
    df_centered[telemetry_col] -= df_centered[telemetry_col].mean()
    
    plt.figure(figsize=(14, 7))
    plt.plot(df_centered[time_col], df_centered[telemetry_col], label=f"Centered {telemetry_col}", linewidth=2)
    plt.title(title)
    plt.xlabel(time_col)
    plt.ylabel(f"Centered {telemetry_col}")
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_bar_chart(df, numeric_col, category_col, ylabel: str, title=None):
    """
    Plots a bar chart showing the mean of a numeric column grouped by a categorical column.
    """

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x=category_col, y=numeric_col, hue=category_col, dodge=False)
    plt.title(title if title else f"Mean {numeric_col} by {category_col}")
    plt.xlabel(category_col)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.show()