
import can
import cantools
import pandas as pd


def simulate_can(csv_path, dbc_path, max_samples=5):
    db = cantools.database.load_file(str(dbc_path))
    data = pd.read_csv(csv_path)

    status_msg = db.get_message_by_name("Battery_Status")
    thermal_msg = db.get_message_by_name("Battery_Thermal")

    bus = can.Bus(
        channel="battery_virtual",
        interface="virtual",
        receive_own_messages=True
    )

    try:
        for _, row in data.head(max_samples).iterrows():

            status_payload = status_msg.encode({
                "PackVoltage": float(row["voltage_V"]),
                "PackCurrent": float(row["current_A"]),
                "SOC": float(row["soc_pct"])
            })

            thermal_payload = thermal_msg.encode({
                "PackTemperature": float(row["temperature_C"]),
                "SOH": 100.0
            })

            for msg_def, payload in [
                (status_msg, status_payload),
                (thermal_msg, thermal_payload)
            ]:
                frame = can.Message(
                    arbitration_id=msg_def.frame_id,
                    data=payload,
                    is_extended_id=False
                )

                bus.send(frame)

                received = bus.recv(timeout=1.0)

                if received is None:
                    raise TimeoutError("CAN frame not received")

                decoded = db.decode_message(
                    received.arbitration_id,
                    received.data
                )

                print(
                    f"t={row['time_s']:.0f}s "
                    f"CAN ID={hex(received.arbitration_id)} "
                    f"Data={received.data.hex()} "
                    f"Decoded={decoded}"
                )

    finally:
        bus.shutdown()
