
class BatteryModel:
    """Track simulated EV battery measurements."""

    def __init__(self):
        self.voltage_V = None
        self.current_A = None
        self.soc_pct = None
        self.soh_pct = None
        self.temperature_C = None

    def update(
        self,
        voltage_V,
        current_A,
        soc_pct,
        temperature_C,
        soh_pct=100.0,
    ):
        if not 0 <= soc_pct <= 100:
            raise ValueError("SOC must be between 0 and 100%")

        if not 0 <= soh_pct <= 100:
            raise ValueError("SOH must be between 0 and 100%")

        self.voltage_V = float(voltage_V)
        self.current_A = float(current_A)
        self.soc_pct = float(soc_pct)
        self.temperature_C = float(temperature_C)
        self.soh_pct = float(soh_pct)

    def get_state(self):
        return {
            "voltage_V": self.voltage_V,
            "current_A": self.current_A,
            "soc_pct": self.soc_pct,
            "temperature_C": self.temperature_C,
            "soh_pct": self.soh_pct,
        }
