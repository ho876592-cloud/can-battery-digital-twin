
import sys
from pathlib import Path

import can
import cantools
import pandas as pd


PROJECT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT / "src"))

from can_decoder import BatteryCANDecoder


def test_virtual_can_integration():
    db = cantools.database.load_file(
        str(PROJECT / "dbc" / "battery_can.dbc")
    )
    decoder = BatteryCANDecoder(
        PROJECT / "dbc" / "battery_can.dbc"
    )

    data = pd.read_csv(
        PROJECT / "data" / "battery_simulation.csv"
    ).head(5)

    tx_bus = can.Bus(channel="battery_test", interface="virtual")
    rx_bus = can.Bus(channel="battery_test", interface="virtual")

    count = 0

    try:
        for _, row in data.iterrows():
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
                definition = db.get_message_by_name(name)

                frame = can.Message(
                    arbitration_id=definition.frame_id,
                    data=definition.encode(signals),
                    is_extended_id=False,
                )

                tx_bus.send(frame)
                received = rx_bus.recv(timeout=2.0)

                assert received is not None

                decoded = decoder.decode(received)

                assert decoded is not None
                assert decoded["message_name"] == name

                for signal, expected in signals.items():
                    actual = decoded["signals"][signal]
                    assert abs(actual - expected) <= 0.26

                count += 1

        assert count == 10

    finally:
        tx_bus.shutdown()
        rx_bus.shutdown()
