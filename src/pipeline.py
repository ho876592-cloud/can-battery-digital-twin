
from pathlib import Path

import can
import cantools
import pandas as pd

from can_decoder import BatteryCANDecoder
from database import BatteryDatabase


def run_pipeline():
    project = Path(__file__).resolve().parents[1]

    csv_path = project / "data" / "battery_simulation.csv"
    dbc_path = project / "dbc" / "battery_can.dbc"
    db_path = project / "data" / "battery_full.db"

    samples = pd.read_csv(csv_path)

    dbc = cantools.database.load_file(str(dbc_path))
    decoder = BatteryCANDecoder(dbc_path)

    # Reset the generated full-simulation database.
    if db_path.exists():
        db_path.unlink()

    database = BatteryDatabase(db_path)

    frame_count = 0

    with can.Bus(
        channel="battery_full",
        interface="virtual"
    ) as tx_bus, can.Bus(
        channel="battery_full",
        interface="virtual"
    ) as rx_bus:

        for _, row in samples.iterrows():
            received_signals = {}

            messages = [
                ("Battery_Status", {
                    "PackVoltage": float(row["voltage_V"]),
                    "PackCurrent": float(row["current_A"]),
                    "SOC": float(row["soc_pct"]),
                }),
                ("Battery_Thermal", {
                    "PackTemperature": float(row["temperature_C"]),
                    "SOH": 100.0,
                }),
            ]

            for name, signals in messages:
                definition = dbc.get_message_by_name(name)

                frame = can.Message(
                    arbitration_id=definition.frame_id,
                    data=definition.encode(signals),
                    is_extended_id=False,
                )

                tx_bus.send(frame)
                received = rx_bus.recv(timeout=2.0)

                if received is None:
                    raise RuntimeError("CAN receive timeout")

                decoded = decoder.decode(received)

                if decoded is None:
                    raise RuntimeError("CAN decoding failed")

                if decoded["message_name"] != name:
                    raise RuntimeError("Unexpected CAN message")

                received_signals.update(decoded["signals"])
                frame_count += 1

            database.insert_measurement(
                time_s=float(row["time_s"]),
                voltage_V=received_signals["PackVoltage"],
                current_A=received_signals["PackCurrent"],
                soc_pct=received_signals["SOC"],
                temperature_C=received_signals["PackTemperature"],
                soh_pct=received_signals["SOH"],
            )

    stored = database.fetch_all()

    assert len(stored) == len(samples)
    assert frame_count == 2 * len(samples)

    print("Full CAN pipeline completed!")
    print("CSV samples:", len(samples))
    print("CAN frames processed:", frame_count)
    print("SQLite records:", len(stored))
    print("First measurement:", stored[0])
    print("Last measurement:", stored[-1])


if __name__ == "__main__":
    run_pipeline()
