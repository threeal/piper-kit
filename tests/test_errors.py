from piper_kit.errors import (
    InvalidControlModeError,
    InvalidGripperEffortError,
    InvalidJointIdError,
    InvalidMoveModeError,
    InvalidMoveSpeedRateError,
)


def test_invalid_control_mode_error() -> None:
    error = InvalidControlModeError("invalid")
    assert str(error) == "Invalid control mode: 'invalid'"


def test_invalid_gripper_effort_error() -> None:
    error = InvalidGripperEffortError("invalid")
    assert str(error) == "Invalid gripper effort: 'invalid'"


def test_invalid_joint_id_error() -> None:
    error = InvalidJointIdError("invalid")
    assert str(error) == "Invalid joint ID: 'invalid'"


def test_invalid_move_mode_error() -> None:
    error = InvalidMoveModeError("invalid")
    assert str(error) == "Invalid move mode: 'invalid'"


def test_invalid_move_speed_rate_error() -> None:
    error = InvalidMoveSpeedRateError("invalid")
    assert str(error) == "Invalid move speed rate: 'invalid'"
