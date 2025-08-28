# f1data.py
import fastf1

class F1Session:
    
    def __init__(self, year: int, gp: str, session: str):
        self.session = fastf1.get_session(year, gp, session)
        self.session.load()
    
    def get_laps(self, driver: str=None):
        return self.session.laps.pick_driver(driver) if driver else self.session.laps
    
    def get_fastest_lap(self, driver: str):
        return self.session.laps.pick_driver(driver).pick_fastest()
    
    def get_telemetry(self, lap):
        return lap.get_telemetry()
    
    # Delegate directly to session if needed
    def __getattr__(self, name):
        return getattr(self.session, name)
