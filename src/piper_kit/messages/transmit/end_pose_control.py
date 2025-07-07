"""Messages for controlling position and rotation of end-effector pose."""

from .transmit import TransmitMessage


class EndPoseControlXyMessage(TransmitMessage):
    """Message for controlling X and Y positions of end-effector pose."""

    ID = 0x152

    def __init__(self, x: int, y: int) -> None:
        """Create message for controlling X and Y positions of end-effector pose.

        Args:
            x: Target X position in 0.001 mm.
            y: Target Y position in 0.001 mm.

        """
        super().__init__(
            self.ID,
            *x.to_bytes(4, signed=True),
            *y.to_bytes(4, signed=True),
        )


class EndPoseControlZpMessage(TransmitMessage):
    """Message for controlling Z position and pitch rotation of end-effector pose."""

    ID = 0x153

    def __init__(self, z: int, pitch: int) -> None:
        """Create message for controlling Z pos and pitch rotation of end-effector pose.

        Args:
            z: Target Z position in 0.001 mm.
            pitch: Target pitch rotation in 0.001 degrees.

        """
        super().__init__(
            self.ID,
            *z.to_bytes(4, signed=True),
            *pitch.to_bytes(4, signed=True),
        )


class EndPoseControlRyMessage(TransmitMessage):
    """Message for controlling roll and yaw rotations of end-effector pose."""

    ID = 0x154

    def __init__(self, roll: int, yaw: int) -> None:
        """Create message for controlling roll and yaw rotations of end-effector pose.

        Args:
            roll: Target roll rotation in 0.001 degrees.
            yaw: Target yaw rotation in 0.001 degrees.

        """
        super().__init__(
            self.ID,
            *roll.to_bytes(4, signed=True),
            *yaw.to_bytes(4, signed=True),
        )


__all__ = [
    "EndPoseControlRyMessage",
    "EndPoseControlXyMessage",
    "EndPoseControlZpMessage",
]
