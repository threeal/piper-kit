# Piper Kit

A Python SDK and CLI toolkit for controlling the [AgileX PiPER](https://global.agilex.ai/products/piper) 6-DOF robotic arm via CAN bus communication.

This package provides direct low-level control through socketcan interface, enabling real-time joint positioning, motion control, and safety monitoring. Features both command-line tools for quick operations and a comprehensive Python API for programmatic control with automatic resource management.

## Installation

Install from PyPI:

```bash
pip install piper-kit
```

Or for development:

```bash
git clone https://github.com/threeal/piper-kit.git
cd piper-kit
uv sync
```

## Usage

### CLI Commands

Enable the robotic arm (moves to home position):

```bash
piper enable
# or specify CAN interface
piper enable can1
```

Disable the robotic arm (moves to safe position):

```bash
piper disable
# or specify CAN interface
piper disable can1
```

### Python SDK

```python
from piper_kit import PiperInterface

# Use context manager for proper cleanup
with PiperInterface('can0') as piper:
    # Enable all joints
    piper.enable_all_joints()

    # Set motion control
    piper.set_motion_control_b("joint", 20)

    # Control joint positions (6 joints: J1, J2, J3, J4, J5, J6)
    piper.set_joint_control(0, 0, 0, 0, 0, 0)
```

## License

This project is licensed under the terms of the [MIT License](./LICENSE).

Copyright © 2025 [Alfi Maulana](https://github.com/threeal)
