from types import TracebackType
from typing import Self

import can

from .messages import (
    EnableJointMessage,
    JointControl12Message,
    JointControl34Message,
    JointControl56Message,
    MotionControlBMessage,
    MotorInfoBMessage,
    ReceiveMessage,
    UnknownMessage,
)


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

    def set_motion_control_b(
        self,
        move_mode: MotionControlBMessage.MoveMode,
        move_speed_rate: int,
        *,
        control_mode: MotionControlBMessage.ControlMode = "can",
    ) -> None:
        self.bus.send(MotionControlBMessage(control_mode, move_mode, move_speed_rate))

    def set_joint_control_12(self, joint_1: int, joint_2: int) -> None:
        self.bus.send(JointControl12Message(joint_1, joint_2))

    def set_joint_control_34(self, joint_3: int, joint_4: int) -> None:
        self.bus.send(JointControl34Message(joint_3, joint_4))

    def set_joint_control_56(self, joint_5: int, joint_6: int) -> None:
        self.bus.send(JointControl56Message(joint_5, joint_6))

    def set_joint_control(  # noqa: PLR0913
        self,
        joint_1: int,
        joint_2: int,
        joint_3: int,
        joint_4: int,
        joint_5: int,
        joint_6: int,
    ) -> None:
        self.set_joint_control_12(joint_1, joint_2)
        self.set_joint_control_34(joint_3, joint_4)
        self.set_joint_control_56(joint_5, joint_6)

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

    def read_message(self) -> ReceiveMessage:
        msg = self.bus.recv()
        match msg.arbitration_id:
            case _ if (
                MotorInfoBMessage.ID1 <= msg.arbitration_id <= MotorInfoBMessage.ID6
            ):
                return MotorInfoBMessage(msg)

            case _:
                return UnknownMessage(msg)

    def read_all_motor_info_bs(self) -> list[MotorInfoBMessage]:
        infos = [None] * 6
        while any(i is None for i in infos):
            match self.read_message():
                case MotorInfoBMessage() as msg:
                    infos[msg.motor_id - 1] = msg

        return infos


__all__ = ["PiperInterface"]
