"""Unknown message handling for unrecognized CAN messages."""

import can

from .receive import ReceiveMessage


class UnknownMessage(ReceiveMessage):
    """Container for unrecognized CAN messages."""

    def __init__(self, msg: can.Message) -> None:
        """Store unknown CAN message data.

        Args:
            msg: Unrecognized CAN message

        """
        self.arbitration_id = msg.arbitration_id
        self.data = msg.data


__all__ = ["UnknownMessage"]
