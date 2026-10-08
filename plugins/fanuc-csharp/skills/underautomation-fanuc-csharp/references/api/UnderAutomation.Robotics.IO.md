# UnderAutomation.Robotics.IO

## DigitalSignal

`class DigitalSignal`

Digital signal of a robot controller, identified by a group and an index. The names of the groups and the valid indexes depend on the robot.

- `DigitalSignal(string group, int index)`: Creates a digital signal
- `string Group { get; }`: Group of the signal, as defined by the robot
- `int Index { get; }`: Index of the signal in its group
