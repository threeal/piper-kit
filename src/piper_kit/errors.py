"""Exception classes for the PiPER Kit package."""


class InvalidControlModeError(ValueError):
    """Raised when an invalid control mode is provided."""

    def __init__(self, mode: any) -> None:
        """Initialize with invalid control mode.

        Args:
            mode: The invalid control mode that was provided

        """
        super().__init__(f"Invalid control mode: {mode!r}")


class InvalidGripperEffortError(ValueError):
    """Raised when an invalid gripper effort is provided."""

    def __init__(self, effort: any) -> None:
        """Initialize with invalid gripper effort.

        Args:
            effort: The invalid gripper effort that was provided

        """
        super().__init__(f"Invalid gripper effort: {effort!r}")


class InvalidJointIdError(ValueError):
    """Raised when an invalid joint ID is provided."""

    def __init__(self, joint_id: any) -> None:
        """Initialize with invalid joint ID.

        Args:
            joint_id: The invalid joint ID that was provided

        """
        super().__init__(f"Invalid joint ID: {joint_id!r}")


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


__all__ = [
    "InvalidControlModeError",
    "InvalidGripperEffortError",
    "InvalidJointIdError",
    "InvalidMoveModeError",
    "InvalidMoveSpeedRateError",
]
