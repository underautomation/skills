# underautomation.robotics.io

## DigitalSignal

`from underautomation.robotics.io.digital_signal import DigitalSignal`

Digital signal of a robot controller, identified by a group and an index. The names of the groups and the valid indexes depend on the robot.

- `DigitalSignal(group: str, index: int)`: Creates a digital signal
- `group: str (read only)`: Group of the signal, as defined by the robot
- `index: int (read only)`: Index of the signal in its group
