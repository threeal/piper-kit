from typing import Literal

from .transmit import TransmitMessage


class MotionControlBMessage(TransmitMessage):
    ID = 0x151

    MIN_MOVE_SPEED_RATE = 0
    MAX_MOVE_SPEED_RATE = 100

    ControlMode = Literal["standby", "can", "ethernet", "wifi", "offline"]
    MoveMode = Literal["position", "joint", "linear", "circular"]

    class InvalidControlModeError(ValueError):
        def __init__(self, mode: any) -> None:
            super().__init__(f"Invalid control mode: {mode!r}")

    class InvalidMoveModeError(ValueError):
        def __init__(self, mode: any) -> None:
            super().__init__(f"Invalid move mode: {mode!r}")

    class InvalidMoveSpeedRateError(ValueError):
        def __init__(self, rate: any) -> None:
            super().__init__(f"Invalid move speed rate: {rate!r}")

    @staticmethod
    def get_control_mode_byte(mode: ControlMode) -> int:
        match mode:
            case "standby":
                return 0x00
            case "can":
                return 0x01
            case "ethernet":
                return 0x03
            case "wifi":
                return 0x04
            case "offline":
                return 0x07
            case _ as mode:
                raise MotionControlBMessage.InvalidControlModeError(mode)

    @staticmethod
    def get_move_mode_byte(mode: MoveMode) -> int:
        match mode:
            case "position":
                return 0x00
            case "joint":
                return 0x01
            case "linear":
                return 0x02
            case "circular":
                return 0x03
            case _ as mode:
                raise MotionControlBMessage.InvalidMoveModeError(mode)

    def __init__(
        self,
        control_mode: ControlMode,
        move_mode: MoveMode,
        move_speed_rate: int,
    ) -> None:
        if not self.MIN_MOVE_SPEED_RATE <= move_speed_rate <= self.MAX_MOVE_SPEED_RATE:
            raise self.InvalidMoveSpeedRateError(move_speed_rate)

        super().__init__(
            self.ID,
            self.get_control_mode_byte(control_mode),
            self.get_move_mode_byte(move_mode),
            move_speed_rate,
        )


__all__ = ["MotionControlBMessage"]
