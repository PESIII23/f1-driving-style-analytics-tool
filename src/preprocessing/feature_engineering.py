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
        self.df.loc[self.df.index[-1], 'Acceleration (m/s²)'] = self.df.loc[self.df.index[-3:].mean(), 'Acceleration (m/s²)']

        cols = self.df.columns.tolist()
        cols.remove('Acceleration (m/s²)')
        speed_index = cols.index(speed)
        cols.insert(speed_index + 1, 'Acceleration (m/s²)')
        self.df = self.df[cols]

        return self.df

    # def jerk(self):
    #     self.df['Jerk (m/s³)'] = ...
    #     return self.df
    
    # def find_steering_wheel_angle(df, driver: str):
