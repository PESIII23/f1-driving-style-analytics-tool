# Cadillac F1: Driving Style Analytics Tool

[Guide to My Project](https://docs.google.com/document/d/1BunsD4oBivE5Oaoi5o8yKeI-t56p413B6HScvpEkVn8/edit?usp=sharing)

## Business Need
In Formula 1, optimizing performance means understanding both the car and the driver. Lap time is influenced by car setup, tire compound, track conditions, and more. To isolate driver behavior, Cadillac F1 needs a telemetry-driven analytics tool that clusters drivers by driving style, independent of lap time.

## Features
- **Telemetry Data Pipeline:** FastF1 API to clean, feature-rich datasets.
- **Exploratory Data Analysis:** Jupyter notebooks for sector and corner-level insights.
- **Clustering & Multi-axis Plots:** Categorize driving styles using HDBSCAN.
- **Visualization:** Matplotlib plots for speed, acceleration, and more.
- **Extensible Foundation:** Easy to build on for future analytics and F1 workflow integration.

## Getting Started

1. **Clone the repository:**
    ```sh
    git clone https://github.com/<yourusername>/GMMS_DSAT_FastF1.git
    cd GMMS_DSAT_FastF1
    ```
2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```
3. **Launch Jupyter Notebook:**
    ```sh
    jupyter notebook
    ```
    Open `notebooks/01_single_driver_eda.ipynb` or `02_multi_driver_analysis.ipynb` and run the cells to explore the data.
4. **(Optional) VS Code:**
   Open the folder in Visual Studio Code and use the built-in Jupyter support for interactive development.

## How to Use the Notebooks

- Set `year`, `grand_prix`, and `session_type` at the top of the notebook to select the race and session.
- Update driver variable names to match code blocks for consistency and accurate analysis.
- Choose a turn (`critical_turn`) and a radius (`radius`) to focus your analysis. Example:
    ```python
    critical_turn = 16
    radius = 2500
    ```
- Run the notebook cells to filter, clean, and analyze telemetry data for each driver. Visualizations and summary statistics will be generated for the selected turn and radius.
- Change parameters and re-run the notebook to analyze different scenarios or compare across sessions.

## Important Instructions

### Data Preparation & Setup
- Python 3.13+ recommended. See `requirements.txt` for dependencies.
- Keep the workspace structure as provided. Update import paths if you move files.

### Telemetry Analysis & Feature Engineering
- Use provided code blocks to extract, clean, and engineer telemetry features for each driver/session (Q2/Q3).
- The function `extract_driver_fastest_and_second_fastest_sector3_telemetry` returns a DataFrame with fastest and second fastest laps for each qualifying session. Filter this DataFrame to access telemetry for specific laps and drivers.
- Feature engineering is performed using `feature_engineering.TelemetryFeatures`. Use `.acceleration().jerk().g_force().convert_sector_time_to_seconds().get_features_df()` to generate feature DataFrames.

### Clustering & Visualization
- Use `src/models/clustering_hdbscan.py` for HDBSCAN clustering. Adjust `min_cluster_size` and `min_samples` as needed, and keep them consistent between clustering and plotting.
- Visualize results using plotting functions in `src/viz/plots.py` and notebook code blocks. Plot speed, throttle, RPM, and other telemetry features for all drivers and laps.

### Exporting & Further Analysis
- Clustered and EDA summary DataFrames are exported to `notebooks/exports/eda_summaries/` and `notebooks/exports/clustered_dfs/`.
- Extend analysis by adding new feature engineering, clustering, or visualizations as needed.

### Troubleshooting
- If you encounter import errors, check your working directory and dependencies.
- For missing data or feature engineering errors, ensure driver variable names and session selections are correct and consistent.

---

For questions or contributions, open an issue or pull request on GitHub.

## My Contribution
- Piloted the senior capstone project **a semester early**.
- Built a **driver telemetry analytics tool** using Python, Jupyter, and Matplotlib.
- Implemented **clustering and anomaly detection models** to categorize driving styles and flag outlier laps.
- Produced **insights on braking, throttle, and tire wear** patterns.
- Laid foundation for future teams to extend analysis and integrate results into F1 workflows.

## Key Takeaways
- Delivered a **full pipeline from telemetry to insights**.
- Showcased **analytics, ML, and visualization** for real-world problems.
- Early capstone demonstrates **initiative and project ownership**.

## Requirements
See `requirements.txt` for all dependencies.
Python 3.13+ recommended.
