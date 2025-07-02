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

from .interface import PiperInterface

__all__ = ["PiperInterface"]
