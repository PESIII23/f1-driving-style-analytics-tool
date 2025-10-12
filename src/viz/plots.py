import matplotlib.pyplot as plt
import pandas as pd

def plot_single_driver_telemetry(df, driver, time_col='SectorTime (s)', telemetry_cols=[]):
    """
    Dynamically generates a multi-axis plot for multiple telemetry columns over a shared time axis.
    """
    df = df.copy()
    df[time_col] = pd.to_timedelta(df[time_col].astype(str), errors='coerce').dt.total_seconds()
    df[time_col] -= df[time_col].iloc[0]
    df = df.set_index(time_col, drop=True)

    fig, ax = plt.subplots(figsize=(18, 10))
    fig.subplots_adjust(right=0.5)

    axes = [ax]
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.set_xlabel('SectorTime (s)', color='white')
    ax.tick_params(colors='white')  # changes color of ticks and tick labels

    ax.plot(df.index, df[telemetry_cols[0]], color=colors[0], label=telemetry_cols[0])
    ax.set_ylabel(telemetry_cols[0], color=colors[0])
    ax.tick_params(axis='y', colors=colors[0])
    ax.grid(True)

    for i, col in enumerate(telemetry_cols[1:], start=1):
        ax_new = axes[0].twinx()
        ax_new.spines['right'].set_position(('axes', 1 + 0.1 * (i - 1)))
        ax_new.plot(df.index, df[col], color=colors[i], label=col)
        ax_new.set_ylabel(col, color=colors[i])
        ax_new.tick_params(axis='y', colors=colors[i])
        axes.append(ax_new)

    lines, labels = [], []
    for a in axes:
        line, label = a.get_legend_handles_labels()
        lines += line
        labels += label

    unique = dict(zip(labels, lines))
    axes[0].legend(unique.values(), unique.keys(), loc='center left', fontsize=15)

    plt.title("{} - Telemetry Overlay".format(driver), fontsize=15, color='white')
    plt.tight_layout()
    plt.show()

def plot_multiple_drivers_telemetry(dfs, drivers=[], time_col='SectorTime (s)', telemetry_cols=[]):
    """
    Dynamically generates a multi-axis plot for multiple drivers' telemetry columns over a shared time axis.
    """
    colors = ['orange', 'red', 'green', 'blue', 'purple', 'pink', 'brown', 'gray', 'olive', 'cyan', 'magenta', 
              'yellow', 'lime', 'teal', 'navy', 'maroon', 'gold', 'silver', 'coral', 'turquoise', 'violet']

    fig, ax = plt.subplots(figsize=(42, 10))
    fig.subplots_adjust(right=0.5)

    axes = [ax]
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.set_xlabel('SectorTime (s)', color='white')
    ax.tick_params(colors='white')
    ax.grid(True)

    for i in range(1, len(telemetry_cols)):
        ax_new = axes[0].twinx()
        ax_new.spines['right'].set_position(('axes', 1 + 0.1 * (i - 1)))
        axes.append(ax_new)

    for j, df in enumerate(dfs):
        df = df.copy()
        df[time_col] = pd.to_timedelta(df[time_col].astype(str), errors='coerce').dt.total_seconds()
        df[time_col] -= df[time_col].iloc[0]
        df = df.set_index(time_col, drop=True)

        for i, col in enumerate(telemetry_cols):
            color = colors[j % len(colors)]
            axes[i].plot(df.index, df[col], color=color, label="{} - {}".format(drivers[j], col))
            axes[i].set_ylabel(col, color=color)
            axes[i].tick_params(axis='y', colors=color)

    lines, labels = [], []
    for a in axes:
        line, label = a.get_legend_handles_labels()
        lines += line
        labels += label

    unique = dict(zip(labels, lines))
    axes[0].legend(unique.values(), unique.keys(), loc='center left', fontsize=10)
    plt.show()
