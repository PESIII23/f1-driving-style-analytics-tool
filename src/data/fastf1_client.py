import fastf1
import pandas as pd

class FastF1Client:
    """
    Client used to interact with FastF1 API data objects.
    """
    def __init__(self, year: int, gp: str, session: str):
        """
        Initialize a FastF1 client.
        :param year: Season year (e.g., 2024)
        :param gp: Grand Prix name (e.g., 'Monza', 'Bahrain')
        :param session: Session type ('FP1', 'FP2', 'FP3', 'Q', 'R')
        """
        self.year = year
        self.gp = gp
        self.session = session
        self.event = None

    def load_session(self):
        """Load the specified session data"""
        print(f"Loading {self.year} {self.gp} {self.session}")
        self.event = fastf1.get_session(self.year, self.gp, self.session)
        self.event.load()
        print("Session loaded successfully")

    def get_drivers(self):
        """Return the drivers participating in the session"""
        if not self.event:
            raise RuntimeError("Session not yet loaded. Call load_session()")
        return self.event.drivers
    
    def get_laps(self, driver: str=None) -> pd.DataFrame:
        """Return laps for a specific driver or all laps"""
        if not self.event:
            raise RuntimeError("Session not yet loaded. Call load_session()")
        if driver:
            return self.event.laps.pick_driver(driver)
        return self.event.laps
    
    def get_lap(self, driver: str, lap_number: int):
        """Return a specific lap for a driver"""
        laps = self.get_laps(driver)
        lap = laps[laps['LapNumber'] == lap_number]
        if lap.empty:
            raise ValueError(f"No lap number {lap_number} found for driver {driver}")
        return lap.iloc[0]

    def get_telemetry(self, driver: str):
        """Return telemetry for fastest lap of a driver"""
        laps = self.get_laps(driver)
        fast_lap = laps.pick_fastest()
        telemetry = fast_lap.get_telemetry()
        return telemetry

    def get_circuit_info(self):
        """Return information about the circuit"""
        if not self.event:
            raise RuntimeError("Session not loaded. Call load_session() first.")
        circuit = self.event.circuit_info
        return {
            "Name": circuit.Name,
            "Location": circuit.Location,
            "Country": circuit.Country,
            "Length_km": circuit.Length,
            "Turns": circuit.Turns
        }

    def get_results(self):
        """Return the results of the session"""
        if not self.event:
            raise RuntimeError("Session not loaded. Call load_session() first.")
        results_df = self.event.results
        if results_df is None:
            raise ValueError("Results data is not available for this session.")
        return results_df