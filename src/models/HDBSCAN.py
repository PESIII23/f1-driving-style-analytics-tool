import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import HDBSCAN as _HDBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

pkl_path = 'notebooks/exports/eda_summaries/2024_abuDhabi_sector3_qualifying.pkl'
df = pd.read_pickle(pkl_path)

def perform_hdbscan_clustering(df):
    """
    Performs HDBSCAN clustering on sector 3 qualifying telemetry features
    from the 2024 Abu Dhabi Grand Prix and appends cluster labels to the DataFrame.
    Returns:
        pd.DataFrame: DataFrame with an additional 'Cluster' column.
    """

    # Comment out feature columns to be included in clustering
    X = df.drop(columns=[
        'Driver',
        'Turn',
        'RowCount',
        'MaxSpeed',
        'MeanSpeed',
        'MedianSpeed',
        'SDSpeed',
        'MaxAccel',
        'MeanAccel',
        'MedianAccel',
        'SDAccel',
        'MaxGs',
        'MeanGs',
        'MedianGs',
        'SDGs',
        'GearShifts',
        'ThrottleEvents',
        'MeanThrottle',
        'SDThrottle',
        'BrakeEvents',
        # 'InitialBrakeTime',
        'BrakeDuration',
        'ThrottleRampTime',
        'SpeedMin',
        # 'ExitSpeed',
        'ExitAccelDuration',
        'TurnDuration'
    ])

    X = X.fillna(0)
    X_scaled = StandardScaler().fit_transform(X)
    clusterer = _HDBSCAN(min_cluster_size=2, min_samples=3)
    labels = clusterer.fit_predict(X_scaled)
    probabilities = clusterer.probabilities_
    df['Cluster'] = labels
    
    return (X_scaled, labels, probabilities, df)

def plot_hdbscan_clustering(
    X,
    labels,
    probabilities=None,
    parameters=None,
    ground_truth=False,
    ax=None
):
    """
    Plot HDBSCAN clustering results.

    Authors: The scikit-learn developers
    SPDX-License-Identifier: BSD-3-Clause
    """

    # Create axis if not provided
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))

    # Default values if None passed
    labels = labels if labels is not None else np.ones(X.shape[0])
    probabilities = probabilities if probabilities is not None else np.ones(X.shape[0])

    # Determine unique cluster labels
    unique_labels = set(labels)

    # Generate a color map for clusters
    colors = [
        plt.cm.Spectral(each)
        for each in np.linspace(0, 1, len(unique_labels))
    ]

    # Map index → probability
    proba_map = {idx: probabilities[idx] for idx in range(len(labels))}

    # Plot each cluster
    for k, col in zip(unique_labels, colors):

        # Use black for noise points
        if k == -1:
            col = [0, 0, 0, 1]

        class_indices = np.where(labels == k)[0]

        for idx in class_indices:
            ax.plot(
                X[idx, 0],
                X[idx, 1],
                "x" if k == -1 else "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                markersize=4 if k == -1 else 1 + 5 * proba_map[idx],
            )

    # Count clusters (excluding noise)
    n_clusters = len(unique_labels) - (1 if -1 in labels else 0)

    # Build plot title
    preamble = "True" if ground_truth else "Estimated"
    title = f"{preamble} number of clusters: {n_clusters}"

    if parameters is not None:
        parameters_str = ", ".join(f"{k}={v}" for k, v in parameters.items())
        title += f" | {parameters_str}"

    ax.set_title(title)
    plt.tight_layout()


# Perform clustering and plot results
X_scaled, labels, probabilities, df_clustered = perform_hdbscan_clustering(df)
X_pca = PCA(n_components=2).fit_transform(X_scaled)

plot_hdbscan_clustering(
    X_pca, labels,
    probabilities=probabilities,
    parameters={'min_cluster_size': 2, 'min_samples': 2}
)

plt.show()

# The resulting DataFrame with cluster labels can be used for further analysis
os.makedirs('notebooks/exports/clustered_dfs', exist_ok=True)
export_path = 'notebooks/exports/clustered_dfs/2024_abuDhabi_sector3_qualifying_clustered.pkl'
df_clustered.to_pickle(export_path)
print(f"Clustered dataframe exported to: {export_path}")