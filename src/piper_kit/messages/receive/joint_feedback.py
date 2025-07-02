"""Joint feedback messages from the PiPER arm."""

import can

from .receive import ReceiveMessage


class JointFeedback12Message(ReceiveMessage):
    """Joint feedback message for joints 1 and 2."""

    ID = 0x2A5

    def __init__(self, msg: can.Message) -> None:
        """Parse joint feedback message for joints 1 and 2.

        Args:
            msg: CAN message containing joint position data

        """
        self.joint_1 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_2 = int.from_bytes(msg.data[4:8], signed=True)


class JointFeedback34Message(ReceiveMessage):
    """Joint feedback message for joints 3 and 4."""

    ID = 0x2A6

    def __init__(self, msg: can.Message) -> None:
        """Parse joint feedback message for joints 3 and 4.

        Args:
            msg: CAN message containing joint position data

        """
        self.joint_3 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_4 = int.from_bytes(msg.data[4:8], signed=True)


class JointFeedback56Message(ReceiveMessage):
    """Joint feedback message for joints 5 and 6."""

    ID = 0x2A7

    def __init__(self, msg: can.Message) -> None:
        """Parse joint feedback message for joints 5 and 6.

        Args:
            msg: CAN message containing joint position data

        """
        self.joint_5 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_6 = int.from_bytes(msg.data[4:8], signed=True)


__all__ = ["JointFeedback12Message", "JointFeedback34Message", "JointFeedback56Message"]
