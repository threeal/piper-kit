"""Gripper feedback message implementation."""

import can

from .receive import ReceiveMessage


class GripperFeedbackMessage(ReceiveMessage):
    """CAN message containing gripper position and status feedback."""

    ID = 0x2A8

    class GripperStatus:
        """Gripper status information parsed from status byte."""

        def __init__(self, code: int) -> None:
            """Parse gripper status from status code byte.

            Args:
                code: Status code byte containing bit flags

            """
            self.code = code
            self.low_voltage = bool(code & 1)
            self.motor_overheating = bool(code & 2)
            self.driver_overcurrent = bool(code & 4)
            self.driver_overheating = bool(code & 8)
            self.sensor_error = bool(code & 16)
            self.driver_error = bool(code & 32)
            self.driver_enabled = bool(code & 64)
            self.is_zeroed = bool(code & 128)

    def __init__(self, msg: can.Message) -> None:
        """Parse gripper feedback from CAN message.

        Args:
            msg: CAN message containing gripper feedback data

        """
        self.position = int.from_bytes(msg.data[0:4], signed=True)
        self.effort = int.from_bytes(msg.data[4:6])
        self.status = self.GripperStatus(msg.data[6])


__all__ = ["GripperFeedbackMessage"]
