"""Transmit message classes for sending commands to the PiPER arm."""

from typing import Literal

import can

from piper_kit.errors import (
    InvalidControlModeError,
    InvalidGripperEffortError,
    InvalidJointIdError,
    InvalidMoveModeError,
    InvalidMoveSpeedRateError,
)


class TransmitMessage(can.Message):
    """Base class for CAN messages sent to the PiPER robotic arm."""

    def __init__(  # noqa: PLR0913
        self,
        arbitration_id: int,
        data_0: int = 0x00,
        data_1: int = 0x00,
        data_2: int = 0x00,
        data_3: int = 0x00,
        data_4: int = 0x00,
        data_5: int = 0x00,
        data_6: int = 0x00,
        data_7: int = 0x00,
    ) -> None:
        """Initialize CAN message with arbitration ID and data bytes.

        Args:
            arbitration_id: CAN message ID
            data_0: Data byte 0 (default: 0x00)
            data_1: Data byte 1 (default: 0x00)
            data_2: Data byte 2 (default: 0x00)
            data_3: Data byte 3 (default: 0x00)
            data_4: Data byte 4 (default: 0x00)
            data_5: Data byte 5 (default: 0x00)
            data_6: Data byte 6 (default: 0x00)
            data_7: Data byte 7 (default: 0x00)

        """
        super().__init__(
            arbitration_id=arbitration_id,
            data=[data_0, data_1, data_2, data_3, data_4, data_5, data_6, data_7],
            is_extended_id=False,
        )


class MotionControlBMessage(TransmitMessage):
    """Message to configure motion control parameters for the robotic arm."""

    ID = 0x151

    MIN_MOVE_SPEED_RATE = 0
    MAX_MOVE_SPEED_RATE = 100

    ControlMode = Literal["standby", "can", "ethernet", "wifi", "offline"]
    MoveMode = Literal["end_pose", "joint", "linear", "circular"]

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
                raise InvalidControlModeError(mode)

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
            case "end_pose":
                return 0x00
            case "joint":
                return 0x01
            case "linear":
                return 0x02
            case "circular":
                return 0x03
            case _ as mode:
                raise InvalidMoveModeError(mode)

    def __init__(
        self,
        control_mode: ControlMode,
        move_mode: MoveMode,
        move_speed_rate: int,
    ) -> None:
        """Create motion control message.

        Args:
            control_mode: Control mode ('can', 'standby', etc.)
            move_mode: Movement mode ('joint', 'end_pose', etc.)
            move_speed_rate: Speed rate (0-100)

        Raises:
            InvalidControlModeError: If control_mode is not valid
            InvalidMoveModeError: If move_mode is not valid
            InvalidMoveSpeedRateError: If move_speed_rate is not in range 0-100

        """
        if not self.MIN_MOVE_SPEED_RATE <= move_speed_rate <= self.MAX_MOVE_SPEED_RATE:
            raise InvalidMoveSpeedRateError(move_speed_rate)

        super().__init__(
            self.ID,
            self.get_control_mode_byte(control_mode),
            self.get_move_mode_byte(move_mode),
            move_speed_rate,
        )


class EndPoseControlXyMessage(TransmitMessage):
    """Message for controlling X and Y positions of end-effector pose."""

    ID = 0x152

    def __init__(self, x: int, y: int) -> None:
        """Create message for controlling X and Y positions of end-effector pose.

        Args:
            x: Target X position in 0.001 mm.
            y: Target Y position in 0.001 mm.

        """
        super().__init__(
            self.ID,
            *x.to_bytes(4, signed=True),
            *y.to_bytes(4, signed=True),
        )


class EndPoseControlZpMessage(TransmitMessage):
    """Message for controlling Z position and pitch rotation of end-effector pose."""

    ID = 0x153

    def __init__(self, z: int, pitch: int) -> None:
        """Create message for controlling Z pos and pitch rotation of end-effector pose.

        Args:
            z: Target Z position in 0.001 mm.
            pitch: Target pitch rotation in 0.001 degrees.

        """
        super().__init__(
            self.ID,
            *z.to_bytes(4, signed=True),
            *pitch.to_bytes(4, signed=True),
        )


class EndPoseControlRyMessage(TransmitMessage):
    """Message for controlling roll and yaw rotations of end-effector pose."""

    ID = 0x154

    def __init__(self, roll: int, yaw: int) -> None:
        """Create message for controlling roll and yaw rotations of end-effector pose.

        Args:
            roll: Target roll rotation in 0.001 degrees.
            yaw: Target yaw rotation in 0.001 degrees.

        """
        super().__init__(
            self.ID,
            *roll.to_bytes(4, signed=True),
            *yaw.to_bytes(4, signed=True),
        )


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


class GripperControlMessage(TransmitMessage):
    """CAN message for controlling gripper position and effort."""

    ID = 0x159

    MIN_GRIPPER_EFFORT = 0
    MAX_GRIPPER_EFFORT = 5000

    def __init__(
        self,
        position: int,
        effort: int,
        *,
        enable: bool = False,
        clear_error: bool = False,
        set_zero: bool = False,
    ) -> None:
        """Initialize gripper control message.

        Args:
            position: Target gripper position
            effort: Effort/force to apply
            enable: Enable gripper control
            clear_error: Clear any error state
            set_zero: Set current position as zero reference

        """
        if not self.MIN_GRIPPER_EFFORT <= effort <= self.MAX_GRIPPER_EFFORT:
            raise InvalidGripperEffortError(effort)

        super().__init__(
            self.ID,
            *position.to_bytes(4, signed=True),
            *effort.to_bytes(2),
            (0x01 if enable else 0x00) | (0x02 if clear_error else 0x00),
            0xAE if set_zero else 0x00,
        )


class EnableJointMessage(TransmitMessage):
    """Message to enable or disable individual joints or all joints."""

    ID = 0x471

    MIN_JOINT_ID = 1
    MAX_JOINT_ID = 7

    JointId = Literal[1, 2, 3, 4, 5, 6, 7]

    def __init__(self, joint_id: JointId, *, enable: bool = True) -> None:
        """Create joint enable/disable message.

        Args:
            joint_id: Joint ID (1-6 for individual joints, 7 for all joints)
            enable: True to enable, False to disable

        Raises:
            InvalidJointIdError: If joint_id is not in range 1-7

        """
        if not self.MIN_JOINT_ID <= joint_id <= self.MAX_JOINT_ID:
            raise InvalidJointIdError(joint_id)

        super().__init__(self.ID, joint_id, 0x02 if enable else 0x01)


class JointConfigMessage(TransmitMessage):
    """Message to configure individual joints or all joints."""

    ID = 0x475

    MIN_JOINT_ID = 1
    MAX_JOINT_ID = 7

    JointId = Literal[1, 2, 3, 4, 5, 6, 7]

    def __init__(
        self, joint_id: JointId, *, set_zero: bool = False, clear_error: bool = False
    ) -> None:
        """Create joint config message.

        Args:
            joint_id: Joint ID (1-6 for individual joints, 7 for all joints)
            set_zero: Whether to set the current joint position as the zero position
            clear_error: Whether to clear the current joint error codes

        Raises:
            InvalidJointIdError: If joint_id is not in range 1-7

        """
        if not self.MIN_JOINT_ID <= joint_id <= self.MAX_JOINT_ID:
            raise InvalidJointIdError(joint_id)

        super().__init__(
            self.ID,
            joint_id,
            0xAE if set_zero else 0x00,
            0x00,
            0x7F,
            0xFF,
            0xAE if clear_error else 0x00,
        )


__all__ = [
    "EnableJointMessage",
    "EndPoseControlRyMessage",
    "EndPoseControlXyMessage",
    "EndPoseControlZpMessage",
    "GripperControlMessage",
    "JointConfigMessage",
    "JointControl12Message",
    "JointControl34Message",
    "JointControl56Message",
    "MotionControlBMessage",
    "TransmitMessage",
]
