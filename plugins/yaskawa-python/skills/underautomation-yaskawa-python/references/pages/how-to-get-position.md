# Get the robot position

Read the position of a Yaskawa robot from C# or Python: Cartesian position or joint pulses, which method to choose, and a polling loop. Complete program included.

Web page: https://underautomation.com/yaskawa/documentation/how-to-get-position

This article shows how to read the position of a Yaskawa Motoman robot from a PC, in C# or Python. It gives a complete program that reads the Cartesian position and the joint pulses, then polls the position 10 times per second.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- Nothing else: reading the position works in teach mode and in play mode, without the remote mode.

## Which method to choose

| Need                                       | Method                              | Unit                           |
| ------------------------------------------ | ----------------------------------- | ------------------------------ |
| Where the tool is, to log it or to compute | `GetRobotCartesianPosition()`       | mm and degrees, robot frame    |
| A position to send back with `MoveJoints`  | `GetRobotJointPosition()`           | Encoder pulses per axis        |
| The load of the axes during a move         | `GetTorque()`, `GetPositionError()` | Percent, pulses                |
| A position taught in a job                 | `ReadPositionVariable(n, 1)`        | Raw units of the `P` variable  |
| A second robot, base axes                  | `GetRobotPosition(group)`           | Pulses or raw Cartesian values |

## Example

```python
import time
from datetime import datetime
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Tool center point in the robot frame: mm and degrees
tcp = robot.high_speed_e_server.get_robot_cartesian_position()
print(f"X={tcp.x:.3f} Y={tcp.y:.3f} Z={tcp.z:.3f} Rx={tcp.rx:.4f} Ry={tcp.ry:.4f} Rz={tcp.rz:.4f}")
print(f"Tool {tcp.tool_number}, posture {tcp.form}")

# Joints: encoder pulses, one value per axis
joints = robot.high_speed_e_server.get_robot_joint_position()
print("Pulses:", list(joints.axes))

# Poll the position 10 times per second for 5 seconds
for _ in range(50):
    tcp = robot.high_speed_e_server.get_robot_cartesian_position()
    print(f"{datetime.now():%H:%M:%S.%f} X={tcp.x:.1f} Y={tcp.y:.1f} Z={tcp.z:.1f}")
    time.sleep(0.1)

robot.disconnect()
```

The program:

1. reads the Cartesian position of the tool, with its tool number and its posture;
2. reads the pulses of each axis;
3. reads the Cartesian position every 100 ms for 5 seconds.

## Polling period

Each read is one request and one answer over the network. On a local network, a request takes a few milliseconds: measure it on your cell before you choose the period. Read only what you need in a loop: the Cartesian position alone is one request, the position and the joints are two.

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) reads the same positions over TCP, and also in a user frame or in the tool frame. It also gives the posture of the arm and the temperature of the encoders.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.host_control.host_control_coordinate_system import HostControlCoordinateSystem

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Joints, in encoder pulses
joints = robot.e_server.get_robot_joint_position()
print(f"S={joints.s} L={joints.l} U={joints.u} R={joints.r} B={joints.b} T={joints.t}")

# Cartesian position in the base frame (default), mm and degrees
tcp = robot.e_server.get_robot_cartesian_position()
print(f"X={tcp.x} Y={tcp.y} Z={tcp.z} Rx={tcp.rx} Ry={tcp.ry} Rz={tcp.rz}")

# Posture of the arm and tool of the position
print(f"Front: {tcp.is_front}, upper arm: {tcp.is_upper_arm}, flip: {tcp.is_flip}, tool: {tcp.tool_number}")

# Same position in the robot frame, or in a user frame
in_robot = robot.e_server.get_robot_cartesian_position(HostControlCoordinateSystem.Robot)
in_user1 = robot.e_server.get_robot_cartesian_position(HostControlCoordinateSystem.User1)

# With the external axes (re, axis8...)
with_external = robot.e_server.get_robot_cartesian_position(HostControlCoordinateSystem.Base, True)

robot.disconnect()
```

## From joint angles, without the robot

To compute the position of the flange from joint angles in degrees, or every set of joint angles for a position, use the [offline kinematics](kinematics.md). The computation runs on the PC, without a connection.

## Troubleshooting

- **The values are all `0`:** check the control group and the number of axes with [GetConfigurationInformation](hses-system.md#axis_names).
- **The Cartesian position differs from the pendant:** compare the frame and the tool. `DataType` and `ToolNumber` give the ones of the answer.
- **The first call fails after a pause:** a `SocketException` means that the controller did not answer before `DataTimeoutMilliseconds`. Check the network, then call again.

## What to read next

- [Positions](hses-positions.md): the reference of the position methods.
- [Move the robot from a PC](how-to-move-robot.md).
