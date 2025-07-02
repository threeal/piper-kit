from typing import Literal

from .transmit import TransmitMessage


class EnableJointMessage(TransmitMessage):
    ID = 0x471

    MIN_JOINT_ID = 1
    MAX_JOINT_ID = 7

    JointId = Literal[1, 2, 3, 4, 5, 6, 7]

    class InvalidJointIdError(ValueError):
        def __init__(self, joint_id: any) -> None:
            super().__init__(f"Invalid joint ID: {joint_id!r}")

    def __init__(self, joint_id: JointId, *, enable: bool = True) -> None:
        if not self.MIN_JOINT_ID <= joint_id <= self.MAX_JOINT_ID:
            raise self.InvalidJointIdError(joint_id)

        super().__init__(self.ID, joint_id, 0x02 if enable else 0x01)


__all__ = ["EnableJointMessage"]
