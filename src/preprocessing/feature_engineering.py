import pandas as pd
import numpy as np

class TelemetryFeatures:
    def __init__(self, df):
        self.df = df

    def acceleration(self, speed='Speed (m/s)', sector_time='SectorTime (s)'):
        """
        Calculates acceleration as ΔSpeed / ΔSectorTime, inserts the resulting column
        immediately after the speed column, and sets the final row to the average of 
        the previous three acceleration values to produce a realistic ending.
        """
        self.df = self.df.copy()
        self.df[speed] = pd.to_numeric(self.df[speed], errors='coerce')
        self.df[sector_time] = pd.to_timedelta(self.df[sector_time], errors='coerce')
        self.df['Acceleration (m/s²)'] = (self.df[speed].shift(-1) - self.df[speed])/(self.df[sector_time].shift(-1) - self.df[sector_time]).dt.total_seconds()
        self.df.loc[self.df.index[-1], 'Acceleration (m/s²)'] = self.df['Acceleration (m/s²)'].iloc[-3:].mean()

        cols = self.df.columns.tolist()
        cols.remove('Acceleration (m/s²)')
        speed_index = cols.index(speed)
        cols.insert(speed_index + 1, 'Acceleration (m/s²)')
        self.df = self.df[cols]

        return self

    def jerk(self, accel='Acceleration (m/s²)', sector_time='SectorTime (s)'):
        """
        Calculates jerk as ΔAcceleration / ΔSectorTime, inserts the resulting column
        immediately after the acceleration column, and sets the final row to the average of 
        the previous three jerk values to produce a realistic ending.
        """

        self.df = self.df.copy()
        self.df[accel] = pd.to_numeric(self.df[accel], errors='coerce')
        self.df[sector_time] = pd.to_timedelta(self.df[sector_time], errors='coerce')

        self.df['Jerk (m/s³)'] = (self.df[accel].shift(-1) - self.df[accel])/(self.df[sector_time].shift(-1) - self.df[sector_time]).dt.total_seconds()
        self.df.loc[self.df.index[-1], 'Jerk (m/s³)'] = self.df['Jerk (m/s³)'].iloc[-3:].mean()

        cols = self.df.columns.tolist()
        cols.remove('Jerk (m/s³)')
        accel_index = cols.index(accel)
        cols.insert(accel_index + 1, 'Jerk (m/s³)')
        self.df = self.df[cols]

        return self
    
    def g_force(self, accel='Acceleration (m/s²)', jerk='Jerk (m/s³)'):
        """
        Converts acceleration to g-force.
        """
        self.df = self.df.copy()
        g_force = abs(self.df[accel] / 9.80665)
        jerk_index = self.df.columns.get_loc(jerk)
        self.df.insert(jerk_index + 1, 'G-force (g)', g_force)

        return self
    
    def convert_sector_time_to_seconds(self, time_col='SectorTime (s)'):
        """
        Returns dataframe with sector time converted to total seconds (float)
        """
        self.df = self.df.copy()
        # Only convert to timedelta if not already numeric
        if not pd.api.types.is_numeric_dtype(self.df[time_col]):
            self.df[time_col] = pd.to_timedelta(self.df[time_col].astype(str), errors='coerce').dt.total_seconds()
        self.df[time_col] = self.df[time_col] - self.df[time_col].iloc[0]
        return self

    def steering_wheel_angle(self, 
                            x_col='X (1/10 m)', 
                            y_col='Y (1/10 m)', 
                            speed_col='Speed (m/s)', 
                            wheelbase=3.6, 
                            steering_ratio=15):

        df = self.df.copy()

        # Convert from tenths of meters to meters
        dx = df[x_col].diff() / 10
        dy = df[y_col].diff() / 10

        # Heading angle
        yaw = np.arctan2(dy, dx)

        # Time delta (stabilized)
        dt = df['SectorTime (s)'].diff().clip(lower=1e-4)

        # Yaw rate (rad/s)
        yaw_rate = yaw.diff() / dt
        yaw_rate = yaw_rate.fillna(0)

        # Front wheel angle (rad)
        front_wheel_angle = np.arctan((wheelbase * yaw_rate) / df[speed_col].clip(lower=0.1))

        # Steering wheel angle (deg)
        df['Steering Wheel Angle (°)'] = np.degrees(front_wheel_angle) * steering_ratio
        df['Steering Wheel Angle (°)'] = df['Steering Wheel Angle (°)'].fillna(0)

        self.df = df
        return self

    
    def get_features_df(self):
        """
        Returns new dataframe with invoked features appended
        """
        return self.df
    
    # def find_steering_wheel_angle(df, driver: str):
