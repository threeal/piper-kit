"""Base class for CAN messages transmitted to the PiPER arm."""

import can


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


__all__ = ["TransmitMessage"]
