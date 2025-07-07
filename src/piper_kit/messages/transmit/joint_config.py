"""Messages for configuring joints."""

from typing import Literal

from .transmit import TransmitMessage


class JointConfigMessage(TransmitMessage):
    """Message to configure individual joints or all joints."""

    ID = 0x475

    MIN_JOINT_ID = 1
    MAX_JOINT_ID = 7

    JointId = Literal[1, 2, 3, 4, 5, 6, 7]

    class InvalidJointIdError(ValueError):
        """Raised when an invalid joint ID is provided."""

        def __init__(self, joint_id: any) -> None:
            """Initialize with invalid joint ID.

            Args:
                joint_id: The invalid joint ID that was provided

            """
            super().__init__(f"Invalid joint ID: {joint_id!r}")

    def __init__(
        self, joint_id: JointId, *, set_zero: bool = False, clear_error: bool = False
    ) -> None:
        """Create joint config message.

        Args:
            joint_id: Joint ID (1-6 for individual joints, 7 for all joints)
            set_zero: Whether to set the current joint position as the zero position
            clear_error: Whether to clear the current joint error codes

        Raises:
            InvalidJointIdError: If joint_id is not in range 1-7

        """
        if not self.MIN_JOINT_ID <= joint_id <= self.MAX_JOINT_ID:
            raise self.InvalidJointIdError(joint_id)

        super().__init__(
            self.ID,
            joint_id,
            0xAE if set_zero else 0x00,
            0x00,
            0x7F,
            0xFF,
            0xAE if clear_error else 0x00,
        )


__all__ = ["JointConfigMessage"]
