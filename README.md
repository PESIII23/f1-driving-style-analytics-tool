# Cadillac F1: Driving Style Analytics Tool

[Guide to My Project](https://docs.google.com/document/d/1BunsD4oBivE5Oaoi5o8yKeI-t56p413B6HScvpEkVn8/edit?usp=sharing)

## Business Need  
In the high-stakes environment of Formula 1, performance optimization hinges on understanding not only the car, but the driver's interaction with it. While lap time remains the ultimate metric, it is influenced by numerous external factors such as car performance, tire compound, track conditions, traffic, and more.  

## Objective  
To isolate and understand driver behavior, Cadillac F1 requires a telemetry-driven analytics tool that can cluster drivers by driving style, independent of lap time.  

## Features
- **Telemetry Data Pipeline:** From FastF1 API to clean, feature-rich datasets.
- **Exploratory Data Analysis:** Jupyter notebooks for sector and corner-level insights.
- **Clustering & Anomaly Detection:** Categorize driving styles and flag unusual laps.
- **Visualization:** Matplotlib and Seaborn plots for speed, acceleration, and more.
- **Extensible Foundation:** Easy to build on for future analytics and F1 workflow integration.

## Getting Started

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/GMMS_DSAT_FastF1.git
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
    Open `notebooks/01_single_race_eda.ipynb` and run the cells to explore the data.

4. **(Optional) VS Code:**  
   Open the folder in Visual Studio Code and use the built-in Jupyter support for interactive development.

## How to Use the Single Race EDA Notebook

The `notebooks/01_single_race_eda.ipynb` notebook allows you to perform exploratory data analysis on telemetry from a single F1 race session. Follow these steps:

1. **Select Race Parameters:**  
   At the top of the notebook, set the `year`, `grand_prix`, and `session_type` variables to choose which race and session you want to analyze. For example:
   ```python
   year = 2024
   grand_prix = f1_constants.F1Constants.LOCATIONS["Abu Dhabi"]
   session_type = f1_constants.F1Constants.SESSIONS["Q"]
   ```

2. **Identify Drivers:**
    You may need to update driver variable names and ensure they match each driver's code block for consistency and accurate data representation. This helps avoid errors and ensures the analysis is performed on the correct telemetry data for each driver.

3. **Select a Turn and Radius:**  
   Choose a turn number (`turn`) and a radius (`radius`) to focus your analysis. The radius determines how much telemetry data around the turn's coordinates is included, which is important for visualizing throttle and braking traces.

   Example:
   ```python
   turn = 16
   radius = 1500  # meters
   ```

4. **Run the Analysis:**  
   Execute the notebook cells to filter, clean, and analyze telemetry data for each driver. The notebook will generate summary statistics and visualizations for the selected turn and radius.

5. **Interpret Results:**  
   Use the output to compare driver performance, braking, throttle application, and other telemetry features around the selected turn.

**Tip:**  
You can easily change the year, grand prix, session type, turn, or radius and re-run the notebook to analyze different scenarios or compare across sessions.

## My Contribution
- Piloted the senior capstone project **a semester early**.
- Built a **driver telemetry analytics tool** using Python, Jupyter, Matplotlib, and Streamlit.
- Implemented **clustering and anomaly detection models** to categorize driving styles and flag outlier laps.
- Produced **insights on braking, throttle, and tire wear** patterns.
- Laid foundation for future teams to extend analysis and integrate results into F1 workflows.

## Key Takeaways
- Delivered a **full pipeline from telemetry to insights**.
- Showcased **analytics, ML, and visualization** for real-world problems.
- Early capstone demonstrates **initiative and project ownership**.

## Requirements
See `requirements.txt` for all dependencies.  
Python 3.9+ recommended.