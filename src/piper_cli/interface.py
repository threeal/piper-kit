from types import TracebackType
from typing import Self

import can

from .messages import EnableJointMessage


class PiperInterface:
    def __init__(self, can_iface: str) -> None:
        self.bus = can.Bus(channel=can_iface, interface="socketcan")

    def __enter__(self) -> int:
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> Self:
        self.bus.shutdown()

    def enable_joint(
        self, joint_id: EnableJointMessage.JointId, *, enable: bool = True
    ) -> None:
        self.bus.send(EnableJointMessage(joint_id, enable=enable))

    def disable_joint(self, joint_id: EnableJointMessage.JointId) -> None:
        self.enable_joint(joint_id, enable=False)

    def enable_all_joints(self, *, enable: bool = True) -> None:
        self.enable_joint(7, enable=enable)

    def disable_all_joints(self) -> None:
        self.enable_all_joints(enable=False)


__all__ = ["PiperInterface"]
