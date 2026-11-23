
class BatteryFaultDetector:
    """Rule-based diagnostics for simulated EV battery data."""

    def __init__(
        self,
        min_soc_pct=20.0,
        min_voltage_V=300.0,
        max_temperature_C=45.0,
        max_current_A=100.0,
    ):
        self.min_soc_pct = min_soc_pct
        self.min_voltage_V = min_voltage_V
        self.max_temperature_C = max_temperature_C
        self.max_current_A = max_current_A

    def check(self, battery_state):
        """Return detected faults as structured records."""
        faults = []

        if battery_state["soc_pct"] < self.min_soc_pct:
            faults.append({
                "code": "LOW_SOC",
                "severity": "WARNING",
                "message": "Battery state of charge is low",
            })

        if battery_state["voltage_V"] < self.min_voltage_V:
            faults.append({
                "code": "UNDERVOLTAGE",
                "severity": "WARNING",
                "message": "Battery pack voltage is below threshold",
            })

        if battery_state["temperature_C"] > self.max_temperature_C:
            faults.append({
                "code": "OVERTEMPERATURE",
                "severity": "CRITICAL",
                "message": "Battery temperature exceeds threshold",
            })

        if abs(battery_state["current_A"]) > self.max_current_A:
            faults.append({
                "code": "OVERCURRENT",
                "severity": "CRITICAL",
                "message": "Battery current exceeds threshold",
            })

        return faults
