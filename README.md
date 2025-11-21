# F1 Driving Style Analytics Tool 🏎️

Machine learning tool that clusters F1 drivers by driving style using telemetry data. Analyzes brake timing, throttle patterns, and cornering techniques independent of lap times.

## 🔍 Overview

Isolates driver behavior from car performance by clustering telemetry patterns. Built with Python, FastF1 API, and HDBSCAN clustering to identify distinct driving styles across 20+ F1 drivers.

## ✨ Key Features

- **📊 Multi-Driver Analysis**: Process entire F1 grid simultaneously in Jupyter notebook
- **🤖 ML Clustering**: HDBSCAN identifies driving style patterns and anomalies  
- **📈 Professional Visualizations**: Dark theme plots optimized for presentations
- **🔧 Advanced Features**: Brake timing, throttle ramps, G-forces, gear shifts

## 🚀 Quick Start

```bash
git clone https://github.com/PESIII23/f1-driving-style-analytics-tool.git
cd f1-driving-style-analytics-tool
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
jupyter notebook
```

Open `notebooks/01_multi_driver_gp_analysis.ipynb` and run all cells for complete analysis.

## 📊 Main Notebook Features

The `01_multi_driver_gp_analysis.ipynb` notebook is the core of this project and provides:

### 🏎️ Driver Processing Pipeline
- **20+ F1 Drivers**: Automated telemetry extraction for entire grid
- **Safety Car Filtering**: Removes distorted laps for clean analysis
- **Corner-Specific Analysis**: Focus on critical turns (e.g., Turn 10 at Bahrain)

### 📈 Advanced Visualizations
```python
# Multi-driver telemetry comparison
plots.plot_multiple_drivers_telemetry(
    dfs=all_driver_dataframes,
    drivers=all_driver_codes,
    telemetry_cols=[speed, throttle, brakes]
)

# Cluster distribution with anomaly analysis
plots.plot_cluster_distribution(
    df_clustered=clustered_data,
    title="Driving Style Clusters - Anomaly Detection"
)
```
- **Dark theme plots** for professional presentations
- **Multi-axis telemetry** showing speed, throttle, braking simultaneously
- **Color-coded by driver** for easy comparison
- **Cluster distribution charts** highlight anomalies with noise-to-signal analysis

### 🤖 Machine Learning Clustering
- **HDBSCAN Algorithm**: Identifies driving style patterns
- **Anomaly Detection**: Flags unusual laps as noise points
- **Feature Engineering**: Brake timing, throttle ramps, exit speeds
- **Cluster Distribution Analysis**: Visual breakdown of clusters vs anomalies
- **Clustering Accuracy**: Assess robustness with noise-to-signal ratios

### 🔧 Configurable Analysis
```python
year = 2025
grand_prix = "Bahrain"
session_type = "R"  # Race or Qualifying
critical_turn = [10]  # Corner to analyze
radius = 2500  # Telemetry capture radius
```

## 📁 Key Files

- `notebooks/01_multi_driver_gp_analysis.ipynb` - **Main analysis notebook**
- `src/models/clustering_hdbscan.py` - HDBSCAN clustering
- `src/viz/plots.py` - Visualization functions
- `src/preprocessing/telemetry_processing.py` - Data processing

## 🔧 Configuration & Usage

### Basic Configuration
```python
year = 2025
grand_prix = "Bahrain"
session_type = "R"      # "R" = Race, "Q" = Qualifying
critical_turn = [10]    # Corner to analyze
radius = 2500          # Telemetry capture radius
```

### Clustering Parameters (in `clustering_hdbscan.py`)
```python
min_cluster_size = 13  # Minimum points per cluster
min_samples = 3        # Core point threshold
```

### Feature Selection
Enable/disable features by commenting/uncommenting in `clustering_hdbscan.py`:
```python
# 'InitialBrakeTime',  # Brake timing analysis
# 'BrakeDuration',     # Brake duration patterns
# 'ThrottleRampTime',  # Throttle application
# 'ExitAccelDuration', # Corner exit acceleration
```

## 🔧 Troubleshooting

**Import Errors**
```bash
# Ensure you're in the project root directory
cd f1-driving-style-analytics-tool
python -c "import src.data.f1_data"  # Should not error
```

**Missing Data**
- FastF1 API requires internet connection
- Some sessions may not have complete telemetry data
- Check session availability on F1 official timing

**Clustering Results**
- Too many noise points? Reduce `min_cluster_size`
- Too few clusters? Increase `min_samples`
- Adjust feature selection for your analysis focus

## 📞 Support

- 📧 Email: [pesmithiii7@gmail.com]
- 🐛 Issues: [GitHub](https://github.com/PESIII23/f1-driving-style-analytics-tool)
- 📚 Documentation: [Project Guide](https://docs.google.com/document/d/1BunsD4oBivE5Oaoi5o8yKeI-t56p413B6HScvpEkVn8/edit?usp=sharing)

---

**Made with ❤️ for Formula 1 analytics and data science!**