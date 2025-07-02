from .transmit import TransmitMessage


class JointControl12Message(TransmitMessage):
    ID = 0x155

    def __init__(self, joint_1: int, joint_2: int) -> None:
        super().__init__(
            self.ID,
            *joint_1.to_bytes(4, signed=True),
            *joint_2.to_bytes(4, signed=True),
        )


class JointControl34Message(TransmitMessage):
    ID = 0x156

    def __init__(self, joint_3: int, joint_4: int) -> None:
        super().__init__(
            self.ID,
            *joint_3.to_bytes(4, signed=True),
            *joint_4.to_bytes(4, signed=True),
        )


class JointControl56Message(TransmitMessage):
    ID = 0x157

    def __init__(self, joint_5: int, joint_6: int) -> None:
        super().__init__(
            self.ID,
            *joint_5.to_bytes(4, signed=True),
            *joint_6.to_bytes(4, signed=True),
        )


__all__ = ["JointControl12Message", "JointControl34Message", "JointControl56Message"]
