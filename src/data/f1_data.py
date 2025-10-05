# f1data.py
import fastf1

class F1Session:
    
    def __init__(self, year: int, gp: str, session: str):
        self.session = fastf1.get_session(year, gp, session)
        self.session.load(telemetry=True)
    
    def get_laps(self, driver: str=None):
        return self.session.laps.pick_drivers(driver) if driver else self.session.laps

    def get_fastest_lap(self, driver: str):
        return self.session.laps.pick_drivers(driver).pick_fastest()

    def get_telemetry(self, lap):
        return lap.get_telemetry()
    
    def get_car_data(self, driver: str):
        return self.session.car_data(driver)
    
    def get_weather_data(self):
        return self.session.weather_data()
    
    def get_circuit_info(self):
        return self.session.get_circuit_info()
    
    def __getattr__(self, name):
        return getattr(self.session, name)
