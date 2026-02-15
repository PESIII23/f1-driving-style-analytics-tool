import pandas as pd
from src.utils import f1_pandas_helpers
from src.preprocessing import telemetry_cleaning, feature_engineering

def process_driver_telemetry(session, driver, safety_car_laps, corner_position_cleaned, critical_turn, radius, start, end):
    """
    Processes a single driver's telemetry to extract corner features, performance metrics, and EDA stats.

    Parameters:
        session: FastF1 session object
        driver: Driver code from F1Constants.DRIVERS
        safety_car_laps: list of lap numbers to exclude
        corner_position_cleaned: tuple/list with corner coordinates
        critical_turn: list/tuple with turn number(s)
        radius: radius around turn to isolate corner telemetry

    Returns:
        final_feature_df: pd.DataFrame containing combined EDA stats and performance metrics
        driver_laps_filtered:
        sector_timestamps_dict: dictionary of lap numbers and their sector timestamps
    """
    # pick laps for driver
    driver_laps = session.laps.pick_drivers(driver)
    driver_laps_filtered = f1_pandas_helpers.filter_driver_lap_data(driver_laps, safety_car_laps)

    # get sector timestamps
    sector_timestamps_dict = f1_pandas_helpers.get_valid_lap_sector_timestamps(driver_laps_filtered)

    # get telemetry for all valid laps
    driver_telemetry = f1_pandas_helpers.get_valid_lap_telemetry(driver_laps_filtered)

    # clean telemetry for each lap
    driver_telemetry_cleaned_list = [
        telemetry_cleaning.clean_driver_telemetry(lap_telemetry, driver)
        for lap_telemetry in driver_telemetry
    ]

    # filter cleaned telemetry down to sector timeframe
    sector_telemetry_list = []
    for lap_df in driver_telemetry_cleaned_list:
        lap_number = lap_df['LapNumber'].iloc[0]
        if lap_number in sector_timestamps_dict.keys():
            sector_start = sector_timestamps_dict[lap_number][start]
            sector_end = sector_timestamps_dict[lap_number][end]

            sector_telemetry = f1_pandas_helpers.filter_timestamp_range(
                lap_df,
                start=sector_start,
                end=sector_end,
                timestamp_col='SessionTime (s)'
            )
            sector_telemetry_list.append(sector_telemetry)

    # filter sector telemetry points that fall within the corner radius
    if (critical_turn != None) and radius > 0:
        corner_telemetry_list = [
            telemetry_cleaning.filter_corner_telemetry(
                sector_df,
                corner_position_cleaned,
                critical_turn,
                radius
            )
            for sector_df in sector_telemetry_list
        ]

        # derive features for each corner-isolated dataframe
        corner_telemetry_enriched_list = [
            feature_engineering.TelemetryFeatures(corner_df)
            .acceleration()
            .g_force()
            .convert_sector_time_to_seconds()
            .get_features_df()
            for corner_df in corner_telemetry_list
        ]

        # generate performance metrics
        performance_metrics_list = [
            feature_engineering.TelemetryFeatures.generate_telemetry_performance_metrics(corner_df)
            for corner_df in corner_telemetry_enriched_list
        ]
        
        performance_metrics_df = pd.DataFrame(performance_metrics_list)

        # calculate EDA stats
        eda_summary_list = [
            f1_pandas_helpers.get_driver_eda_stats(
                df=corner_df,
                driver=driver,
                critical_turn=critical_turn
            )
            for corner_df in corner_telemetry_enriched_list
        ]
        eda_summary_df = pd.concat(eda_summary_list, ignore_index=True)

        # combine EDA stats with performance metrics
        final_feature_df = pd.concat([eda_summary_df, performance_metrics_df.reset_index(drop=True)], axis=1)

        return final_feature_df, driver_laps_filtered, sector_timestamps_dict
    
    else:
        return sector_telemetry_list, driver_laps, driver_laps_filtered, sector_timestamps_dict



def get_fastest_lap_telemetry(processed_driver_data, driver_code, corner_position, critical_turn, radius, start, end):
    """
    Extracts corner-isolated telemetry for the fastest lap of a driver.
    
    Parameters:
        processed_driver_data: tuple
            Output from the driver preprocessing function: (final_feature_df, driver_laps_filtered, sector_timestamps_dict)
        driver_code: str
            Driver code (e.g., 'NOR', 'VER')
        corner_position: dict/array
            Coordinates of the corner for filtering telemetry
        critical_turn: list/tuple
            The turn number or identifier
        radius: float
            Radius for corner isolation
        s1_end_s2_start: str
            Key name for sector1 end / sector2 start timestamp in sector dict
        s2_end_s3_start: str
            Key name for sector2 end / sector3 start timestamp in sector dict

    Returns:
        corner_telemetry_enriched: if critical_turn required get Telemetry df filtered to the corner for the fastest lap
        sector_telemetry: if critical_turn not required, get Telemetry df for the fastest lap
    """
    # unpack processed data
    if (critical_turn != None) and radius > 0:
        _, driver_laps_filtered, sector_timestamps_dict = processed_driver_data
    else:
        _, _, driver_laps_filtered, sector_timestamps_dict = processed_driver_data

    # get fastest lap row
    fastest_lap_idx = driver_laps_filtered.loc[driver_laps_filtered['LapTime'].idxmin()]
    fastest_telemetry = fastest_lap_idx.get_telemetry()

    # clean telemetry
    fastest_telemetry_cleaned = telemetry_cleaning.clean_driver_telemetry(fastest_telemetry, driver_code)

    # get sector start and end timestamps
    fastest_lap_number = fastest_lap_idx['LapNumber']
    sector_start = sector_timestamps_dict[fastest_lap_number][start]
    sector_end = sector_timestamps_dict[fastest_lap_number][end]

    # filter telemetry by sector timestamps
    sector_telemetry = f1_pandas_helpers.filter_timestamp_range(
        fastest_telemetry_cleaned,
        start=sector_start,
        end=sector_end,
        timestamp_col='SessionTime (s)'
    )

    if (critical_turn != None) and (radius > 0):
        # filter telemetry points within corner radius
        corner_telemetry = telemetry_cleaning.filter_corner_telemetry(
            sector_telemetry,
            corner_position,
            critical_turn,
            radius
        )

        # derive features
        corner_telemetry_enriched = (
            feature_engineering.TelemetryFeatures(corner_telemetry)
            .acceleration()
            .g_force()
            .convert_sector_time_to_seconds()
            .get_features_df()
        )

        return corner_telemetry_enriched
    
    else:
        # add fastest lap number to the fastest lap telemetry df
        sector_telemetry = sector_telemetry.copy()
        sector_telemetry['LapNumber'] = fastest_lap_number
        return sector_telemetry