import can

from .receive import ReceiveMessage


class JointFeedback12Message(ReceiveMessage):
    ID = 0x2A5

    def __init__(self, msg: can.Message) -> None:
        self.joint_1 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_2 = int.from_bytes(msg.data[4:8], signed=True)


class JointFeedback34Message(ReceiveMessage):
    ID = 0x2A6

    def __init__(self, msg: can.Message) -> None:
        self.joint_3 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_4 = int.from_bytes(msg.data[4:8], signed=True)


class JointFeedback56Message(ReceiveMessage):
    ID = 0x2A7

    def __init__(self, msg: can.Message) -> None:
        self.joint_5 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_6 = int.from_bytes(msg.data[4:8], signed=True)


__all__ = ["JointFeedback12Message", "JointFeedback34Message", "JointFeedback56Message"]
