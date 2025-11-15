# Authors: The scikit-learn developers
# SPDX-License-Identifier: BSD-3-Clause

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
        'MaxJerk',
        'MeanJerk',
        'MedianJerk',
        'SDJerk',
        'MaxGs',
        'MeanGs',
        'MedianGs',
        'SDGs',
        'GearShifts',
        'ThrottleEvents',
        'MeanThrottle',
        'SDThrottle',
        'BrakeEvents',
        'InitialBrakeTime',
        'BrakeDuration',
        'ThrottleRampTime',
        'SpeedMin',
        'ExitSpeed',
        'ExitAccelDuration',
        'TurnDuration'
    ])


    X = X.fillna(0)
    X_scaled = StandardScaler().fit_transform(X)
    clusterer = _HDBSCAN(min_cluster_size=2, min_samples=2)
    labels = clusterer.fit_predict(X_scaled)
    probabilities = clusterer.probabilities_
    df['Cluster'] = labels
    
    return (X_scaled, labels, probabilities, df)

def plot_hdbscan_clustering(X, labels, probabilities=None, parameters=None, ground_truth=False, ax=None):
    """
    Templte from scikit-learn that plots HDBSCAN clustering results.
    """
    if ax is None:
        _, ax = plt.subplots(figsize=(10, 4))
    labels = labels if labels is not None else np.ones(X.shape[0])
    probabilities = probabilities if probabilities is not None else np.ones(X.shape[0])
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    # The probability of a point belonging to its labeled cluster determines
    # the size of its marker
    proba_map = {idx: probabilities[idx] for idx in range(len(labels))}
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = [0, 0, 0, 1]

        class_index = (labels == k).nonzero()[0]
        for ci in class_index:
            ax.plot(
                X[ci, 0],
                X[ci, 1],
                "x" if k == -1 else "o",
                markerfacecolor=tuple(col),
                markeredgecolor="k",
                markersize=4 if k == -1 else 1 + 5 * proba_map[ci],
            )
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    preamble = "True" if ground_truth else "Estimated"
    title = f"{preamble} number of clusters: {n_clusters_}"
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