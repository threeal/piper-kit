import can

from piper_kit.messages.receive import (
    GripperFeedbackMessage,
    JointFeedback12Message,
    JointFeedback34Message,
    JointFeedback56Message,
    MotorInfoBMessage,
    UnknownMessage,
)


def test_unknown_message() -> None:
    msg = can.Message(arbitration_id=0x123, data=[0x01, 0x02, 0x03, 0x04])
    unknown = UnknownMessage(msg)
    assert unknown.arbitration_id == 0x123
    assert unknown.data == bytearray([0x01, 0x02, 0x03, 0x04])


class TestMotorInfoBMessage:
    def test_motor_info_b_message(self) -> None:
        msg = can.Message(
            arbitration_id=MotorInfoBMessage.ID1,
            data=[0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0],
        )
        motor_info = MotorInfoBMessage(msg)
        assert motor_info.motor_id == 1
        assert motor_info.bus_voltage == 4660
        assert motor_info.driver_temp == 22136
        assert motor_info.motor_temp == -102
        assert motor_info.driver_status.code == 0xBC
        assert motor_info.bus_current == 57072

    def test_driver_status(self) -> None:
        status = MotorInfoBMessage.DriverStatus(0b01010101)
        assert status.code == 0b01010101
        assert status.low_voltage is True
        assert status.motor_overheating is False
        assert status.driver_overcurrent is True
        assert status.driver_overheating is False
        assert status.collision_triggered is True
        assert status.driver_error is False
        assert status.driver_enabled is True
        assert status.stalling_triggered is False


class TestJointFeedbackMessages:
    def test_joint_feedback_12_message(self) -> None:
        msg = can.Message(
            arbitration_id=JointFeedback12Message.ID,
            data=[0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0],
        )
        joint_feedback = JointFeedback12Message(msg)
        assert joint_feedback.joint_1 == 305419896
        assert joint_feedback.joint_2 == -1698898192

    def test_joint_feedback_34_message(self) -> None:
        msg = can.Message(
            arbitration_id=JointFeedback34Message.ID,
            data=[0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0],
        )
        joint_feedback = JointFeedback34Message(msg)
        assert joint_feedback.joint_3 == 305419896
        assert joint_feedback.joint_4 == -1698898192

    def test_joint_feedback_56_message(self) -> None:
        msg = can.Message(
            arbitration_id=JointFeedback56Message.ID,
            data=[0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0],
        )
        joint_feedback = JointFeedback56Message(msg)
        assert joint_feedback.joint_5 == 305419896
        assert joint_feedback.joint_6 == -1698898192


class TestGripperFeedbackMessage:
    def test_gripper_feedback_message(self) -> None:
        msg = can.Message(
            arbitration_id=GripperFeedbackMessage.ID,
            data=[0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xF0],
        )
        gripper_feedback = GripperFeedbackMessage(msg)
        assert gripper_feedback.position == 305419896
        assert gripper_feedback.effort == 39612
        assert gripper_feedback.status.code == 0xDE

    def test_gripper_status(self) -> None:
        status = GripperFeedbackMessage.GripperStatus(0b01010101)
        assert status.code == 0b01010101
        assert status.low_voltage is True
        assert status.motor_overheating is False
        assert status.driver_overcurrent is True
        assert status.driver_overheating is False
        assert status.sensor_error is True
        assert status.driver_error is False
        assert status.driver_enabled is True
        assert status.is_zeroed is False
