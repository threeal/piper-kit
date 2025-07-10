"""PiPER Kit - SDK and CLI tools for AgileX PiPER robotic arm.

This package provides Python bindings for controlling the AgileX PiPER robotic arm
via CAN bus interface using the python-can library.

Example:
    Basic usage of the PiperInterface:

    >>> from piper_kit import PiperInterface
    >>> with PiperInterface('can0') as piper:
    ...     piper.enable_all_joints()
    ...     piper.set_motion_control_b("joint", 20)
    ...     piper.set_joint_control(0, 0, 0, 0, 0, 0)

"""

from types import TracebackType
from typing import Self

import can

from .messages import (
    EnableJointMessage,
    EndPoseControlRyMessage,
    EndPoseControlXyMessage,
    EndPoseControlZpMessage,
    GripperControlMessage,
    GripperFeedbackMessage,
    JointConfigMessage,
    JointControl12Message,
    JointControl34Message,
    JointControl56Message,
    JointFeedback12Message,
    JointFeedback34Message,
    JointFeedback56Message,
    MotionControlBMessage,
    MotorInfoBMessage,
    ReceiveMessage,
    UnknownMessage,
)


class PiperInterface:
    """Interface for controlling the AgileX PiPER robotic arm via CAN bus.

    This class provides methods for controlling joint positions, enabling/disabling
    joints, and reading feedback from the robotic arm through the CAN bus interface.

    Args:
        can_iface: CAN interface name (e.g., 'can0')

    """

    def __init__(self, can_iface: str) -> None:
        """Initialize PiperInterface with CAN interface."""
        self.bus = can.Bus(channel=can_iface, interface="socketcan")

    def __enter__(self) -> Self:
        """Enter context manager."""
        return self

    def __exit__(
        self,
        _exc_type: type[BaseException] | None,
        _exc_val: BaseException | None,
        _exc_tb: TracebackType | None,
    ) -> None:
        """Exit context manager and shutdown CAN bus."""
        self.bus.shutdown()

    def set_motion_control_b(
        self,
        move_mode: MotionControlBMessage.MoveMode,
        move_speed_rate: int,
        *,
        control_mode: MotionControlBMessage.ControlMode = "can",
    ) -> None:
        """Set motion control parameters for the robotic arm.

        Args:
            move_mode: Motion control mode ('joint' or other modes)
            move_speed_rate: Speed rate for movement (0-100)
            control_mode: Control mode ('can' by default)

        """
        self.bus.send(MotionControlBMessage(control_mode, move_mode, move_speed_rate))

    def set_end_pose_control_xy(self, x: int, y: int) -> None:
        """Set X and Y positions control of end-effector pose.

        Args:
            x: Target X position in 0.001 mm.
            y: Target Y position in 0.001 mm.

        """
        self.bus.send(EndPoseControlXyMessage(x, y))

    def set_end_pose_control_zp(self, z: int, pitch: int) -> None:
        """Set Z position and pitch rotation control of end-effector pose.

        Args:
            z: Target Z position in 0.001 mm.
            pitch: Target pitch rotation in 0.001 degrees.

        """
        self.bus.send(EndPoseControlZpMessage(z, pitch))

    def set_end_pose_control_ry(self, roll: int, yaw: int) -> None:
        """Set roll and yaw rotations control of end-effector pose.

        Args:
            roll: Target roll rotation in 0.001 degrees.
            yaw: Target yaw rotation in 0.001 degrees.

        """
        self.bus.send(EndPoseControlRyMessage(roll, yaw))

    def set_end_pose_control(  # noqa: PLR0913
        self,
        x: int,
        y: int,
        z: int,
        pitch: int,
        roll: int,
        yaw: int,
    ) -> None:
        """Set position and rotation control of end-effector pose.

        Args:
            x: Target X position in 0.001 mm.
            y: Target Y position in 0.001 mm.
            z: Target Z position in 0.001 mm.
            pitch: Target pitch rotation in 0.001 degrees.
            roll: Target roll rotation in 0.001 degrees.
            yaw: Target yaw rotation in 0.001 degrees.

        """
        self.set_end_pose_control_xy(x, y)
        self.set_end_pose_control_zp(z, pitch)
        self.set_end_pose_control_ry(roll, yaw)

    def set_joint_control_12(self, joint_1: int, joint_2: int) -> None:
        """Set position control for joints 1 and 2.

        Args:
            joint_1: Target position for joint 1
            joint_2: Target position for joint 2

        """
        self.bus.send(JointControl12Message(joint_1, joint_2))

    def set_joint_control_34(self, joint_3: int, joint_4: int) -> None:
        """Set position control for joints 3 and 4.

        Args:
            joint_3: Target position for joint 3
            joint_4: Target position for joint 4

        """
        self.bus.send(JointControl34Message(joint_3, joint_4))

    def set_joint_control_56(self, joint_5: int, joint_6: int) -> None:
        """Set position control for joints 5 and 6.

        Args:
            joint_5: Target position for joint 5
            joint_6: Target position for joint 6

        """
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
        """Set position control for all 6 joints simultaneously.

        Args:
            joint_1: Target position for joint 1
            joint_2: Target position for joint 2
            joint_3: Target position for joint 3
            joint_4: Target position for joint 4
            joint_5: Target position for joint 5
            joint_6: Target position for joint 6

        """
        self.set_joint_control_12(joint_1, joint_2)
        self.set_joint_control_34(joint_3, joint_4)
        self.set_joint_control_56(joint_5, joint_6)

    def set_gripper_control(
        self,
        position: int,
        effort: int,
        *,
        enable: bool = True,
        clear_error: bool = False,
        set_zero: bool = False,
    ) -> None:
        """Control gripper position and effort.

        Args:
            position: Target gripper position
            effort: Effort/force to apply
            enable: Enable gripper control
            clear_error: Clear any error state
            set_zero: Set current position as zero reference

        """
        self.bus.send(
            GripperControlMessage(
                position,
                effort,
                enable=enable,
                clear_error=clear_error,
                set_zero=set_zero,
            )
        )

    def enable_gripper(self, *, enable: bool = True) -> None:
        """Enable or disable gripper control.

        Args:
            enable: True to enable, False to disable

        """
        self.set_gripper_control(0, 0, enable=enable)

    def disable_gripper(self) -> None:
        """Disable gripper control."""
        self.enable_gripper(enable=False)

    def enable_joint(
        self, joint_id: EnableJointMessage.JointId, *, enable: bool = True
    ) -> None:
        """Enable or disable a specific joint.

        Args:
            joint_id: Joint ID (1-6) or 7 for all joints
            enable: True to enable, False to disable

        """
        self.bus.send(EnableJointMessage(joint_id, enable=enable))

    def disable_joint(self, joint_id: EnableJointMessage.JointId) -> None:
        """Disable a specific joint.

        Args:
            joint_id: Joint ID (1-6) or 7 for all joints

        """
        self.enable_joint(joint_id, enable=False)

    def enable_all_joints(self, *, enable: bool = True) -> None:
        """Enable or disable all joints simultaneously.

        Args:
            enable: True to enable, False to disable

        """
        self.enable_joint(7, enable=enable)

    def disable_all_joints(self) -> None:
        """Disable all joints simultaneously."""
        self.enable_all_joints(enable=False)

    def set_joint_config(
        self,
        joint_id: JointConfigMessage.JointId,
        *,
        set_zero: bool = False,
        clear_error: bool = False,
    ) -> None:
        """Set the configuration of a specific joint.

        Args:
            joint_id: Joint ID (1-6 for individual joints, 7 for all joints)
            set_zero: Whether to set the current joint position as the zero position
            clear_error: Whether to clear the current joint error codes

        """
        self.bus.send(
            JointConfigMessage(joint_id, set_zero=set_zero, clear_error=clear_error)
        )

    def set_all_joint_configs(
        self, *, set_zero: bool = False, clear_error: bool = False
    ) -> None:
        """Set the configuration of all joints.

        Args:
            set_zero: Whether to set the current joint position as the zero position
            clear_error: Whether to clear the current joint error codes

        """
        self.set_joint_config(7, set_zero=set_zero, clear_error=clear_error)

    def read_message(self) -> ReceiveMessage:
        """Read a single message from the CAN bus.

        Returns:
            Parsed message object (JointFeedback, GripperFeedback, MotorInfo, or
            Unknown)

        """
        msg = self.bus.recv()
        match msg.arbitration_id:
            case _ if (
                MotorInfoBMessage.ID1 <= msg.arbitration_id <= MotorInfoBMessage.ID6
            ):
                return MotorInfoBMessage(msg)

            case JointFeedback12Message.ID:
                return JointFeedback12Message(msg)

            case JointFeedback34Message.ID:
                return JointFeedback34Message(msg)

            case JointFeedback56Message.ID:
                return JointFeedback56Message(msg)

            case GripperFeedbackMessage.ID:
                return GripperFeedbackMessage(msg)

            case _:
                return UnknownMessage(msg)

    def read_all_motor_info_bs(self) -> list[MotorInfoBMessage]:
        """Read motor information from all 6 joints.

        Blocks until motor info is received from all joints.

        Returns:
            List of 6 MotorInfoBMessage objects containing status and diagnostic info

        """
        infos = [None] * 6
        while any(i is None for i in infos):
            match self.read_message():
                case MotorInfoBMessage() as msg:
                    infos[msg.motor_id - 1] = msg

        return infos

    def read_all_joint_feedbacks(self) -> list[int]:
        """Read current position feedback from all 6 joints.

        Blocks until feedback is received from all joints.

        Returns:
            List of 6 joint positions [joint1, joint2, joint3, joint4, joint5, joint6]

        """
        feedbacks = [None] * 6
        while any(f is None for f in feedbacks):
            match self.read_message():
                case JointFeedback12Message() as msg:
                    feedbacks[0] = msg.joint_1
                    feedbacks[1] = msg.joint_2

                case JointFeedback34Message() as msg:
                    feedbacks[2] = msg.joint_3
                    feedbacks[3] = msg.joint_4

                case JointFeedback56Message() as msg:
                    feedbacks[4] = msg.joint_5
                    feedbacks[5] = msg.joint_6

        return feedbacks

    def read_gripper_feedback(self) -> GripperFeedbackMessage:
        """Read position feedback from the gripper.

        Blocks until gripper feedback is received.

        Returns:
            A GripperFeedbackMessage containing the current gripper position.

        """
        feedback = None
        while feedback is None:
            match self.read_message():
                case GripperFeedbackMessage() as msg:
                    feedback = msg

        return feedback


__all__ = ["PiperInterface"]
