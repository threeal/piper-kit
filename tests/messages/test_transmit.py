import pytest

from piper_kit.errors import (
    InvalidControlModeError,
    InvalidGripperEffortError,
    InvalidJointIdError,
    InvalidMoveModeError,
    InvalidMoveSpeedRateError,
)
from piper_kit.messages.transmit import (
    EnableJointMessage,
    EndPoseControlRyMessage,
    EndPoseControlXyMessage,
    EndPoseControlZpMessage,
    GripperControlMessage,
    JointConfigMessage,
    JointControl12Message,
    JointControl34Message,
    JointControl56Message,
    MotionControlBMessage,
    TransmitMessage,
)


def test_transmit_message() -> None:
    msg = TransmitMessage(0x123, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08)
    assert msg.arbitration_id == 0x123
    assert list(msg.data) == [0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08]
    assert msg.is_extended_id is False


class TestMotionControlBMessage:
    def test_motion_control_b_message(self) -> None:
        msg = MotionControlBMessage("can", "joint", 50)
        assert msg.arbitration_id == MotionControlBMessage.ID
        assert list(msg.data) == [0x01, 0x01, 0x32, 0x00, 0x00, 0x00, 0x00, 0x00]

    def test_get_control_mode_byte(self) -> None:
        assert MotionControlBMessage.get_control_mode_byte("standby") == 0x00
        assert MotionControlBMessage.get_control_mode_byte("can") == 0x01
        assert MotionControlBMessage.get_control_mode_byte("ethernet") == 0x03
        assert MotionControlBMessage.get_control_mode_byte("wifi") == 0x04
        assert MotionControlBMessage.get_control_mode_byte("offline") == 0x07

        with pytest.raises(InvalidControlModeError):
            MotionControlBMessage.get_control_mode_byte("invalid")

    def test_get_move_mode_byte(self) -> None:
        assert MotionControlBMessage.get_move_mode_byte("end_pose") == 0x00
        assert MotionControlBMessage.get_move_mode_byte("joint") == 0x01
        assert MotionControlBMessage.get_move_mode_byte("linear") == 0x02
        assert MotionControlBMessage.get_move_mode_byte("circular") == 0x03

        with pytest.raises(InvalidMoveModeError):
            MotionControlBMessage.get_move_mode_byte("invalid")

    def test_invalid_move_speed_rate(self) -> None:
        with pytest.raises(InvalidMoveSpeedRateError):
            MotionControlBMessage("can", "joint", -1)

        with pytest.raises(InvalidMoveSpeedRateError):
            MotionControlBMessage("can", "joint", 101)


class TestEndPoseControlMessages:
    def test_end_pose_control_xy_message(self) -> None:
        msg = EndPoseControlXyMessage(1000, -2000)
        assert msg.arbitration_id == EndPoseControlXyMessage.ID
        assert list(msg.data) == [0x00, 0x00, 0x03, 0xE8, 0xFF, 0xFF, 0xF8, 0x30]

    def test_end_pose_control_zp_message(self) -> None:
        msg = EndPoseControlZpMessage(1000, -2000)
        assert msg.arbitration_id == EndPoseControlZpMessage.ID
        assert list(msg.data) == [0x00, 0x00, 0x03, 0xE8, 0xFF, 0xFF, 0xF8, 0x30]

    def test_end_pose_control_ry_message(self) -> None:
        msg = EndPoseControlRyMessage(1000, -2000)
        assert msg.arbitration_id == EndPoseControlRyMessage.ID
        assert list(msg.data) == [0x00, 0x00, 0x03, 0xE8, 0xFF, 0xFF, 0xF8, 0x30]


class TestJointControlMessages:
    def test_joint_control_12_message(self) -> None:
        msg = JointControl12Message(1000, -2000)
        assert msg.arbitration_id == JointControl12Message.ID
        assert list(msg.data) == [0x00, 0x00, 0x03, 0xE8, 0xFF, 0xFF, 0xF8, 0x30]

    def test_joint_control_34_message(self) -> None:
        msg = JointControl34Message(1000, -2000)
        assert msg.arbitration_id == JointControl34Message.ID
        assert list(msg.data) == [0x00, 0x00, 0x03, 0xE8, 0xFF, 0xFF, 0xF8, 0x30]

    def test_joint_control_56_message(self) -> None:
        msg = JointControl56Message(1000, -2000)
        assert msg.arbitration_id == JointControl56Message.ID
        assert list(msg.data) == [0x00, 0x00, 0x03, 0xE8, 0xFF, 0xFF, 0xF8, 0x30]


class TestGripperControlMessage:
    def test_gripper_control_message(self) -> None:
        msg = GripperControlMessage(
            1000, 2000, enable=True, clear_error=True, set_zero=True
        )
        assert msg.arbitration_id == GripperControlMessage.ID
        assert list(msg.data) == [0x00, 0x00, 0x03, 0xE8, 0x07, 0xD0, 0x03, 0xAE]

    def test_invalid_effort(self) -> None:
        with pytest.raises(InvalidGripperEffortError):
            GripperControlMessage(1000, -1)

        with pytest.raises(InvalidGripperEffortError):
            GripperControlMessage(1000, 5001)


class TestEnableJointMessage:
    def test_enable_joint_message(self) -> None:
        msg = EnableJointMessage(1)
        assert msg.arbitration_id == EnableJointMessage.ID
        assert list(msg.data) == [0x01, 0x02, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

    def test_invalid_joint_id(self) -> None:
        with pytest.raises(InvalidJointIdError):
            EnableJointMessage(0)

        with pytest.raises(InvalidJointIdError):
            EnableJointMessage(8)


class TestJointConfigMessage:
    def test_joint_config_message(self) -> None:
        msg = JointConfigMessage(1, set_zero=True, clear_error=True)
        assert msg.arbitration_id == JointConfigMessage.ID
        assert list(msg.data) == [0x01, 0xAE, 0x00, 0x7F, 0xFF, 0xAE, 0x00, 0x00]

    def test_invalid_joint_id(self) -> None:
        with pytest.raises(InvalidJointIdError):
            JointConfigMessage(0)

        with pytest.raises(InvalidJointIdError):
            JointConfigMessage(8)
