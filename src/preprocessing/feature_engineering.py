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
        
        g_force = abs(self.df[accel] / 9.80665)
        jerk_index = self.df.columns.get_loc(jerk)
        self.df.insert(jerk_index + 1, 'G-force (g)', g_force)

        return self
    
    def convert_sector_time_to_seconds(self, time_col='SectorTime (s)'): 
        """
        Returns dataframe with sector time converted to total seconds
        """ 
        self.df = self.df.copy() 
        self.df[time_col] = pd.to_timedelta(self.df[time_col].astype(str), errors='coerce').dt.total_seconds() 
        self.df[time_col] -= self.df[time_col].iloc[0]
        
        return self

    def steering_wheel_angle(self, 
                             x_col='X (1/10 m)', 
                             y_col='Y (1/10 m)', 
                             speed_col='Speed (m/s)', 
                             wheelbase=3.6, 
                             steering_ratio=15):
        """
        Calculates steering wheel angle based on changes in X and Y coordinates.
        """

        self.df = self.df.copy()

        # Compute differences (in 1/10 m)
        dx = self.df[x_col].diff()
        dy = self.df[y_col].diff()

        # Heading
        yaw = np.arctan2(dy, dx)

        # Time delta
        dt = self.df['SectorTime (s)'].diff().replace(0, np.nan)

        # Yaw rate
        yaw_np = yaw.to_numpy()
        dt_np = dt.to_numpy()

        yaw_rate = np.zeros_like(yaw_np)
        yaw_rate[1:] = (yaw_np[1:] - yaw_np[:-1]) / dt_np[1:]
        yaw_rate[0] = 0

        # Front wheel angle (using yaw_rate and speed)
        front_wheel_angle = np.arctan((wheelbase * yaw_rate) / self.df[speed_col])

        # Steering wheel angle in degrees
        self.df['Steering Wheel Angle (°)'] = np.degrees(front_wheel_angle * steering_ratio)
        self.df['Steering Wheel Angle (°)'] = self.df['Steering Wheel Angle (°)'].fillna(0)

        return self
    
    def get_features_df(self):
        """
        Returns new dataframe with invoked features appended
        """
        return self.df
    
    # def find_steering_wheel_angle(df, driver: str):
