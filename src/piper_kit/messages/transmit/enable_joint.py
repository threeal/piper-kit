"""Joint enable/disable messages for motor control."""

from typing import Literal

from .transmit import TransmitMessage


class EnableJointMessage(TransmitMessage):
    """Message to enable or disable individual joints or all joints."""

    ID = 0x471

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

    def __init__(self, joint_id: JointId, *, enable: bool = True) -> None:
        """Create joint enable/disable message.

        Args:
            joint_id: Joint ID (1-6 for individual joints, 7 for all joints)
            enable: True to enable, False to disable

        Raises:
            InvalidJointIdError: If joint_id is not in range 1-7

        """
        if not self.MIN_JOINT_ID <= joint_id <= self.MAX_JOINT_ID:
            raise self.InvalidJointIdError(joint_id)

        super().__init__(self.ID, joint_id, 0x02 if enable else 0x01)


__all__ = ["EnableJointMessage"]
