import can


class TransmitMessage(can.Message):
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
        super().__init__(
            arbitration_id=arbitration_id,
            data=[data_0, data_1, data_2, data_3, data_4, data_5, data_6, data_7],
            is_extended_id=False,
        )


__all__ = ["TransmitMessage"]
