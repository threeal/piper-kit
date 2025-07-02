import can

from .receive import ReceiveMessage


class MotorInfoBMessage(ReceiveMessage):
    ID0 = 0x260
    ID1 = 0x261
    ID2 = 0x262
    ID3 = 0x263
    ID4 = 0x264
    ID5 = 0x265
    ID6 = 0x266

    class DriverStatus:
        def __init__(self, code: int) -> None:
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
        self.motor_id = msg.arbitration_id - MotorInfoBMessage.ID0
        self.bus_voltage = int.from_bytes(msg.data[0:2])
        self.driver_temp = int.from_bytes(msg.data[2:4], signed=True)
        self.motor_temp = int.from_bytes(msg.data[4:5], signed=True)
        self.driver_status = MotorInfoBMessage.DriverStatus(msg.data[5])
        self.bus_current = int.from_bytes(msg.data[6:8])


__all__ = ["MotorInfoBMessage"]
