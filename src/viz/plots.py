import matplotlib.pyplot as plt
import pandas as pd

def plot_two_driver_telemetry_delta(dfs):
    return None

def plot_multiple_drivers_telemetry(dfs, drivers=[], time_col='SectorTime (s)', telemetry_cols=[]):
    """
    Dynamically generates a multi-axis plot for multiple drivers' telemetry columns over a shared time axis.
    Assumes that the time_col is already in seconds (numeric).
    """
    import matplotlib.pyplot as plt

    colors = ['red', 'yellow', 'green', 'orange', 'blue', 'pink', 'brown', 'gray', 'olive', 'cyan', 'magenta', 
              'purple', 'lime', 'teal', 'navy', 'maroon', 'gold', 'silver', 'coral', 'turquoise', 'violet']

    fig, ax = plt.subplots(figsize=(42, 10))
    fig.subplots_adjust(right=0.5)

    axes = [ax]
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.set_xlabel(time_col, color='white')
    ax.tick_params(colors='white')
    ax.grid(True)

    for i in range(1, len(telemetry_cols)):
        ax_new = axes[0].twinx()
        ax_new.spines['right'].set_position(('axes', 1 + 0.1 * (i - 1)))
        axes.append(ax_new)

    for j, df in enumerate(dfs):
        df = df.copy()
        
        if not pd.api.types.is_numeric_dtype(df[time_col]):
            raise ValueError(f"{time_col} must be numeric (seconds) before plotting.")
        
        df = df.dropna(subset=[time_col])
        
        df[time_col] -= df[time_col].iloc[0]
        
        df = df.set_index(time_col, drop=True)

        for i, col in enumerate(telemetry_cols):
            color = colors[j % len(colors)]
            axes[i].plot(df.index, df[col], color=color, label=f"{drivers[j]} - {col}", linewidth=1.5)
            axes[i].set_ylabel(col, color=color)
            axes[i].tick_params(axis='y', colors=color)

    lines, labels = [], []
    for a in axes:
        line, label = a.get_legend_handles_labels()
        lines += line
        labels += label

    unique = dict(zip(labels, lines))
    axes[0].legend(unique.values(), unique.keys(), loc='center right', fontsize=10)
    plt.show()

def plot_cluster_distribution(df_clustered, title='Cluster Distribution'):
    """
    Plots a pie chart showing the distribution of clusters vs noise points.
    Treats noise points (-1) as anomalies.
    """
    cluster_counts = df_clustered['Cluster'].value_counts().sort_index()
    
    # Separate noise from clusters
    labels = []
    sizes = []
    colors = []
    
    # Bold color palette matching telemetry plot
    cluster_colors = ['red', 'yellow', 'green', 'orange', 'blue', 'pink', 'brown', 'gray', 'olive', 'cyan', 'magenta', 
                     'purple', 'lime', 'teal', 'navy', 'maroon', 'gold', 'silver', 'coral', 'turquoise', 'violet']
    
    for cluster, count in cluster_counts.items():
        if cluster == -1:
            labels.append(f'Noise/Anomalies ({count})')
            colors.append('red')
        else:
            labels.append(f'Cluster {cluster} ({count})')
            colors.append(cluster_colors[cluster % len(cluster_colors)])
        sizes.append(count)
    
    # Create figure with black background
    fig, ax = plt.subplots(figsize=(16, 8))
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Create pie chart with enhanced styling
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, 
                                      autopct='%1.1f%%', startangle=140,
                                      textprops={'color': 'white', 'fontsize': 12},
                                      wedgeprops={'edgecolor': 'white', 'linewidth': 1})
    
    # Style the percentage text
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontweight('bold')
        autotext.set_fontsize(11)
    
    # Highlight noise/anomalies with thicker border
    for i, label in enumerate(labels):
        if 'Noise' in label:
            wedges[i].set_edgecolor('gold')
            wedges[i].set_linewidth(2)
    
    # Style the title
    ax.set_title(title, fontsize=16, color='white', fontweight='bold', pad=20)
    
    # Add a subtle grid effect
    ax.grid(True, alpha=0.1, color='white')
    
    plt.tight_layout()
    plt.show()