
import cantools


class BatteryCANDecoder:
    """Decode simulated battery CAN frames using a DBC."""

    def __init__(self, dbc_path):
        self.db = cantools.database.load_file(str(dbc_path))

    def decode(self, message):
        if message.is_extended_id or message.is_remote_frame:
            return None

        try:
            definition = self.db.get_message_by_frame_id(
                message.arbitration_id
            )
        except KeyError:
            return None

        if len(message.data) != definition.length:
            raise ValueError("Invalid CAN payload length")

        signals = definition.decode(
            message.data,
            decode_choices=False
        )

        return {
            "can_id": message.arbitration_id,
            "message_name": definition.name,
            "signals": signals
        }
