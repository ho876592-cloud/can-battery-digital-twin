
from pathlib import Path

from database import BatteryDatabase
from battery_model import BatteryModel
from fault_detection import BatteryFaultDetector


def main():
    project = Path(__file__).resolve().parents[1]
    db_path = project / "data" / "battery_full.db"

    if not db_path.exists():
        raise FileNotFoundError(
            "Battery database not found. Run CAN-to-SQLite integration first."
        )

    database = BatteryDatabase(db_path)
    battery = BatteryModel()
    detector = BatteryFaultDetector()

    measurements = database.fetch_all()
    fault_count = 0

    print("CAN-Based EV Battery Digital Twin")
    print("=" * 45)

    for row in measurements:
        time_s, voltage, current, soc, temperature, soh = row

        battery.update(
            voltage_V=voltage,
            current_A=current,
            soc_pct=soc,
            temperature_C=temperature,
            soh_pct=soh,
        )

        faults = detector.check(battery.get_state())
        fault_count += len(faults)

        print(
            f"Time: {time_s:.0f}s | "
            f"Voltage: {voltage:.1f}V | "
            f"SOC: {soc:.1f}% | "
            f"Temperature: {temperature:.1f}C"
        )

        if faults:
            for fault in faults:
                print(f"  {fault['severity']}: {fault['code']}")
        else:
            print("  Status: NORMAL")

    print("=" * 45)
    print(f"Measurements processed: {len(measurements)}")
    print(f"Total faults detected: {fault_count}")


if __name__ == "__main__":
    main()
