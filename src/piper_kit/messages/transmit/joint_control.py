"""Joint control messages for commanding joint positions."""

from .transmit import TransmitMessage


class JointControl12Message(TransmitMessage):
    """Joint control message for joints 1 and 2."""

    ID = 0x155

    def __init__(self, joint_1: int, joint_2: int) -> None:
        """Create joint control message for joints 1 and 2.

        Args:
            joint_1: Target position for joint 1
            joint_2: Target position for joint 2

        """
        super().__init__(
            self.ID,
            *joint_1.to_bytes(4, signed=True),
            *joint_2.to_bytes(4, signed=True),
        )


class JointControl34Message(TransmitMessage):
    """Joint control message for joints 3 and 4."""

    ID = 0x156

    def __init__(self, joint_3: int, joint_4: int) -> None:
        """Create joint control message for joints 3 and 4.

        Args:
            joint_3: Target position for joint 3
            joint_4: Target position for joint 4

        """
        super().__init__(
            self.ID,
            *joint_3.to_bytes(4, signed=True),
            *joint_4.to_bytes(4, signed=True),
        )


class JointControl56Message(TransmitMessage):
    """Joint control message for joints 5 and 6."""

    ID = 0x157

    def __init__(self, joint_5: int, joint_6: int) -> None:
        """Create joint control message for joints 5 and 6.

        Args:
            joint_5: Target position for joint 5
            joint_6: Target position for joint 6

        """
        super().__init__(
            self.ID,
            *joint_5.to_bytes(4, signed=True),
            *joint_6.to_bytes(4, signed=True),
        )


__all__ = ["JointControl12Message", "JointControl34Message", "JointControl56Message"]
