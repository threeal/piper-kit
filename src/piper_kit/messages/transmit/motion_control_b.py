"""Motion control messages for setting arm movement parameters."""

from typing import Literal

from .transmit import TransmitMessage


class MotionControlBMessage(TransmitMessage):
    """Message to configure motion control parameters for the robotic arm."""

    ID = 0x151

    MIN_MOVE_SPEED_RATE = 0
    MAX_MOVE_SPEED_RATE = 100

    ControlMode = Literal["standby", "can", "ethernet", "wifi", "offline"]
    MoveMode = Literal["position", "joint", "linear", "circular"]

    class InvalidControlModeError(ValueError):
        """Raised when an invalid control mode is provided."""

        def __init__(self, mode: any) -> None:
            """Initialize with invalid control mode.

            Args:
                mode: The invalid control mode that was provided

            """
            super().__init__(f"Invalid control mode: {mode!r}")

    class InvalidMoveModeError(ValueError):
        """Raised when an invalid move mode is provided."""

        def __init__(self, mode: any) -> None:
            """Initialize with invalid move mode.

            Args:
                mode: The invalid move mode that was provided

            """
            super().__init__(f"Invalid move mode: {mode!r}")

    class InvalidMoveSpeedRateError(ValueError):
        """Raised when an invalid move speed rate is provided."""

        def __init__(self, rate: any) -> None:
            """Initialize with invalid move speed rate.

            Args:
                rate: The invalid move speed rate that was provided

            """
            super().__init__(f"Invalid move speed rate: {rate!r}")

    @staticmethod
    def get_control_mode_byte(mode: ControlMode) -> int:
        """Convert control mode to byte value.

        Args:
            mode: Control mode string

        Returns:
            Byte value for the control mode

        Raises:
            InvalidControlModeError: If mode is not valid

        """
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
        """Convert move mode to byte value.

        Args:
            mode: Move mode string

        Returns:
            Byte value for the move mode

        Raises:
            InvalidMoveModeError: If mode is not valid

        """
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
        """Create motion control message.

        Args:
            control_mode: Control mode ('can', 'standby', etc.)
            move_mode: Movement mode ('joint', 'position', etc.)
            move_speed_rate: Speed rate (0-100)

        Raises:
            InvalidControlModeError: If control_mode is not valid
            InvalidMoveModeError: If move_mode is not valid
            InvalidMoveSpeedRateError: If move_speed_rate is not in range 0-100

        """
        if not self.MIN_MOVE_SPEED_RATE <= move_speed_rate <= self.MAX_MOVE_SPEED_RATE:
            raise self.InvalidMoveSpeedRateError(move_speed_rate)

        super().__init__(
            self.ID,
            self.get_control_mode_byte(control_mode),
            self.get_move_mode_byte(move_mode),
            move_speed_rate,
        )


__all__ = ["MotionControlBMessage"]
