"""Receive message classes for reading feedback from the PiPER arm."""

import can


class ReceiveMessage:
    """Base class for CAN messages received from the PiPER robotic arm."""


class UnknownMessage(ReceiveMessage):
    """Container for unrecognized CAN messages."""

    def __init__(self, msg: can.Message) -> None:
        """Store unknown CAN message data.

        Args:
            msg: Unrecognized CAN message

        """
        self.arbitration_id = msg.arbitration_id
        self.data = msg.data


class MotorInfoBMessage(ReceiveMessage):
    """Motor information message containing status and diagnostic data."""

    ID0 = 0x260
    ID1 = 0x261
    ID2 = 0x262
    ID3 = 0x263
    ID4 = 0x264
    ID5 = 0x265
    ID6 = 0x266

    class DriverStatus:
        """Driver status information parsed from status byte."""

        def __init__(self, code: int) -> None:
            """Parse driver status from status code byte.

            Args:
                code: Status code byte containing bit flags

            """
            self.code = code
            self.low_voltage = bool(code & 1)
            self.motor_overheating = bool(code & 2)
            self.driver_overcurrent = bool(code & 4)
            self.driver_overheating = bool(code & 8)
            self.collision_triggered = bool(code & 16)
            self.driver_error = bool(code & 32)
            self.driver_enabled = bool(code & 64)
            self.stalling_triggered = bool(code & 128)

    def __init__(self, msg: can.Message) -> None:
        """Parse motor information from CAN message.

        Args:
            msg: CAN message containing motor diagnostic data

        """
        self.motor_id = msg.arbitration_id - MotorInfoBMessage.ID0
        self.bus_voltage = int.from_bytes(msg.data[0:2])
        self.driver_temp = int.from_bytes(msg.data[2:4], signed=True)
        self.motor_temp = int.from_bytes(msg.data[4:5], signed=True)
        self.driver_status = MotorInfoBMessage.DriverStatus(msg.data[5])
        self.bus_current = int.from_bytes(msg.data[6:8])


class JointFeedback12Message(ReceiveMessage):
    """Joint feedback message for joints 1 and 2."""

    ID = 0x2A5

    def __init__(self, msg: can.Message) -> None:
        """Parse joint feedback message for joints 1 and 2.

        Args:
            msg: CAN message containing joint position data

        """
        self.joint_1 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_2 = int.from_bytes(msg.data[4:8], signed=True)


class JointFeedback34Message(ReceiveMessage):
    """Joint feedback message for joints 3 and 4."""

    ID = 0x2A6

    def __init__(self, msg: can.Message) -> None:
        """Parse joint feedback message for joints 3 and 4.

        Args:
            msg: CAN message containing joint position data

        """
        self.joint_3 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_4 = int.from_bytes(msg.data[4:8], signed=True)


class JointFeedback56Message(ReceiveMessage):
    """Joint feedback message for joints 5 and 6."""

    ID = 0x2A7

    def __init__(self, msg: can.Message) -> None:
        """Parse joint feedback message for joints 5 and 6.

        Args:
            msg: CAN message containing joint position data

        """
        self.joint_5 = int.from_bytes(msg.data[0:4], signed=True)
        self.joint_6 = int.from_bytes(msg.data[4:8], signed=True)


class GripperFeedbackMessage(ReceiveMessage):
    """CAN message containing gripper position and status feedback."""

    ID = 0x2A8

    class GripperStatus:
        """Gripper status information parsed from status byte."""

        def __init__(self, code: int) -> None:
            """Parse gripper status from status code byte.

            Args:
                code: Status code byte containing bit flags

            """
            self.code = code
            self.low_voltage = bool(code & 1)
            self.motor_overheating = bool(code & 2)
            self.driver_overcurrent = bool(code & 4)
            self.driver_overheating = bool(code & 8)
            self.sensor_error = bool(code & 16)
            self.driver_error = bool(code & 32)
            self.driver_enabled = bool(code & 64)
            self.is_zeroed = bool(code & 128)

    def __init__(self, msg: can.Message) -> None:
        """Parse gripper feedback from CAN message.

        Args:
            msg: CAN message containing gripper feedback data

        """
        self.position = int.from_bytes(msg.data[0:4], signed=True)
        self.effort = int.from_bytes(msg.data[4:6])
        self.status = self.GripperStatus(msg.data[6])


__all__ = [
    "GripperFeedbackMessage",
    "JointFeedback12Message",
    "JointFeedback34Message",
    "JointFeedback56Message",
    "MotorInfoBMessage",
    "ReceiveMessage",
    "UnknownMessage",
]
