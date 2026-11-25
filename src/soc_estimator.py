
class SOCEstimator:
    """SOC estimation using Coulomb Counting."""

    def __init__(self, capacity_Ah=60.0, initial_soc_pct=80.0):
        if capacity_Ah <= 0:
            raise ValueError("Capacity must be positive")

        if not 0 <= initial_soc_pct <= 100:
            raise ValueError("Initial SOC must be between 0 and 100")

        self.capacity_Ah = float(capacity_Ah)
        self.soc_pct = float(initial_soc_pct)

    def update(self, current_A, dt_s):
        if dt_s < 0:
            raise ValueError("Time interval cannot be negative")

        delta_soc = (
            current_A * dt_s
            / (3600 * self.capacity_Ah)
        ) * 100

        self.soc_pct -= delta_soc

        self.soc_pct = max(0.0, min(100.0, self.soc_pct))

        return self.soc_pct

    def get_soc(self):
        return self.soc_pct
