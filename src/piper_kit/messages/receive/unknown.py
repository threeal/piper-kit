import can

from .receive import ReceiveMessage


class UnknownMessage(ReceiveMessage):
    def __init__(self, msg: can.Message) -> None:
        self.arbitration_id = msg.arbitration_id
        self.data = msg.data


__all__ = ["UnknownMessage"]
