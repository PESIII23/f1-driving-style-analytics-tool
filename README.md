# F1 Driving Style Analytics Tool 🏎️

A machine learning tool that uses telemetry data to cluster F1 drivers by driving style, isolating driver behavior from car performance through braking, throttle usage, and cornering—independent of lap times.

---

## Quick Start

Follow these steps to get up and running:

```bash
git clone https://github.com/PESIII23/f1-driving-style-analytics-tool.git
cd f1-driving-style-analytics-tool
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

Open `notebooks/01_multi_driver_gp_analysis.ipynb` and run all cells to perform the analysis.

---

## Data Requirements & Driver Selection

Before running the analysis, confirm the drivers that participated in your selected session:

1. **Research Session Participants**: Check F1 official timing or race results for the Grand Prix and session.
2. **Query Using FastF1 API**: Identify available drivers dynamically:
   ```python
   import fastf1
   session = fastf1.get_session(2025, 'Bahrain', 'R')
   session.load()
   available_drivers = session.drivers  # List of driver codes
   print(f"Available drivers: {available_drivers}")
   ```
3. **Update Notebook**: Modify driver constants in the notebook to reflect session participants.
4. **Handle Missing Data**: Missing telemetry data for some drivers is skipped automatically.

**Note**: A default configuration based on the 2025 F1 grid is preloaded, but verification for your session is required.

---

## Driver Data Pipeline

The Driver Processing Pipeline includes:

- **Telemetry for 20+ Drivers**: Automated extraction for the grid.
- **Safety Car Filtering**: Removes distorted lap times for clean analysis.
- **Critical Turn Analysis**: Focuses on predefined corners (e.g., Turn 10 at Bahrain).

### Customization
Customize the session parameters:
```python
year = 2025
grand_prix = "Bahrain"
session_type = "R"      # "R" = Race or "Q" = Qualifying
critical_turn = [10]    # Corner to analyze
radius = 2500           # Radius of telemetry capture in meters
```

---

## Feature Engineering

This project generates advanced telemetry performance metrics for analysis and clustering:

- **Acceleration (m/s²)**: Captures changes in speed over time to detect braking and throttle patterns.
- **Jerk (m/s³)**: Measures smoothness of braking/throttle application.
- **G-Force**: Estimates lateral and longitudinal forces acting on the driver.
- **Steering Wheel Angle (°)**: Calculates driver steering behavior using telemetry paths.

These features are saved in an **engineered features pickle file** (`engineered_features.pkl`). The notebook references this file for clustering.

---

## Telemetry Visualizations

The tool supports advanced visualizations for comparing driver telemetry:

1. **Driver and Feature Selection**:
   - Input any combination of driver names and telemetry features:
     ```python
     plots.plot_multiple_drivers_telemetry(
         dfs=all_driver_dataframes,
         drivers=['VER', 'HAM', 'ALO'],  # Specify driver codes
         telemetry_cols=['speed', 'throttle', 'brakes']
     )
     ```

2. **Customizable Analysis**: Analyze specific drivers or focus on particular telemetry features/regions.

3. **Professional Outputs**:
   - **Scatter plots** showing speed, throttle, and brakes across turns.
   - **Cluster distribution graphs**: Highlight driving patterns and anomalies from ML results.

---

## Machine Learning Clustering

The core functionality revolves around extracting driving styles using HDBSCAN clustering:

1. **Feature Selection**:
   - In `src/models/clustering_hdbscan.py`, uncomment desired features:
     ```python
     # 'InitialBrakeTime',
     # 'BrakeDuration',
     # 'ThrottleRampTime',
     # 'ExitAccelDuration',
     ```
   - Ensure PCA components match the number of selected features.

2. **Parameter Tuning**:
   Modify clustering parameters:
   ```python
   min_cluster_size = 13  # Minimum points per cluster
   min_samples = 3        # Core point threshold
   ```

3. **Pickle File Outputs**:
   - **Clustered Dataframe**: After clustering, outputs are saved into `clustered_dataframe.pkl` for review and visualization.

4. **Visualization Examples**:
   - Cluster evaluation:
     ```python
     plots.plot_cluster_distribution(
         df_clustered=clustered_data,
         title="Driving Style Clusters - Anomaly Detection"
     )
     ```
   - PCA-based cluster projections and noise identification.

---

## Key Files

- `notebooks/01_multi_driver_gp_analysis.ipynb` - Main analysis notebook.
- `src/models/clustering_hdbscan.py` - Clustering implementation.
- `src/preprocessing/feature_engineering.py` - Telemetry feature computation.
- `src/viz/plots.py` - Visualization utilities.

---

## Error Handling & Troubleshooting

**Import Errors**:
Ensure you're in the project root directory:
```bash
cd f1-driving-style-analytics-tool
python -c "import src.data.f1_data"  # Should not error
```

**Clustering Results**:
- Too many noise points? Decrease `min_cluster_size`.
- Too few clusters? Increase `min_samples` or add more telemetry features in preprocessing.

**Notebook Loading Errors**:
- If you encounter `ModuleNotFoundError: No module named 'src'`, verify your Python path and run the Jupyter notebook from the project root.

---

## Key Features Summary

- **Multi-Driver Telemetry Analysis**: Process the entire grid.
- **Feature Engineering**: Jerk, acceleration, g-force, and more.
- **ML Clustering**: HDBSCAN algorithm with PCA preprocessing.
- **Customizable Visualizations**: Compare telemetry, analyze clusters.
- **Reusable Outputs**: Clustered data and features saved as pickle files.

---

## Support

If you run into any issues or have questions:
- Email: [pesmithiii7@gmail.com](mailto:pesmithiii7@gmail.com)
- Documentation: [Project Guide](https://docs.google.com/document/d/1bUCOeN5bhuaDrrDMexeJ81TFGt67gbFEIRQ7dnIu1b4/edit?usp=sharing)
- Repository: [GitHub](https://github.com/PESIII23/f1-driving-style-analytics-tool)