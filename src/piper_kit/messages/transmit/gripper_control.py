"""Gripper control message implementation."""

from .transmit import TransmitMessage


class GripperControlMessage(TransmitMessage):
    """CAN message for controlling gripper position and effort."""

    ID = 0x159

    MIN_GRIPPER_EFFORT = 0
    MAX_GRIPPER_EFFORT = 5000

    class InvalidGripperEffortError(ValueError):
        """Raised when an invalid gripper effort is provided."""

        def __init__(self, effort: any) -> None:
            """Initialize with invalid gripper effort.

            Args:
                effort: The invalid gripper effort that was provided

            """
            super().__init__(f"Invalid gripper effort: {effort!r}")

    def __init__(
        self,
        position: int,
        effort: int,
        *,
        enable: bool = False,
        clear_error: bool = False,
        set_zero: bool = False,
    ) -> None:
        """Initialize gripper control message.

        Args:
            position: Target gripper position
            effort: Effort/force to apply
            enable: Enable gripper control
            clear_error: Clear any error state
            set_zero: Set current position as zero reference

        """
        if not self.MIN_GRIPPER_EFFORT <= effort <= self.MAX_GRIPPER_EFFORT:
            raise self.InvalidGripperEffortError(effort)

        super().__init__(
            self.ID,
            *position.to_bytes(4, signed=True),
            *effort.to_bytes(2),
            (0x01 if enable else 0x00) | (0x02 if clear_error else 0x00),
            0xAE if set_zero else 0x00,
        )


__all__ = ["GripperControlMessage"]
