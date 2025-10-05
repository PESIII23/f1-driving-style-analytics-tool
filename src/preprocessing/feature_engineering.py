import pandas as pd

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

        g_force = self.df[accel] / 9.80665
        jerk_index = self.df.columns.get_loc(jerk)
        self.df.insert(jerk_index + 1, 'G-force (g)', g_force)

        return self
    
    def get_features_df(self):
        return self.df
    
    # def find_steering_wheel_angle(df, driver: str):
