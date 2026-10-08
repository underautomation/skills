# Position

Read the current joints and the Cartesian position of a Staubli robot, for the flange or a tool, in the world frame or in another frame.

Web page: https://underautomation.com/staubli/documentation/soap-position

This page shows how to read the current position of a Staubli robot on a CS8 or CS9 controller: the joint values, and the Cartesian position of the flange or of a tool, in the world or in another frame.

## Joints and Cartesian position

`GetCurrentCartesianJointPosition(robot)` returns the joints and the Cartesian position of the flange in the world frame, in one request.

```python
from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Joints and flange position of the first robot, in one request
position = controller.soap.get_current_cartesian_joint_position(0)

# Joint values, in radians
joints = list(position.joints_position)

# Flange position in the world frame: X, Y, Z in meters, Rx, Ry, Rz in radians
flange = position.cartesian_position
print(f"X={flange.x} Y={flange.y} Z={flange.z}")
print(f"Rx={flange.rx} Ry={flange.ry} Rz={flange.rz}")

controller.disconnect()
```

| Value                                | Unit    |
| ------------------------------------ | ------- |
| `JointsPosition`, one value per axis | radians |
| `X`, `Y`, `Z`                        | meters  |
| `Rx`, `Ry`, `Rz`                     | radians |

## Joints only

`GetCurrentJointPosition(robot)` returns only the joint values. Use it when you do not need the Cartesian position.

```python
import math

from underautomation.staubli.staubli_controller import StaubliController

controller = StaubliController()
controller.connect("192.168.0.254")

# Only the joints, in radians
joints = controller.soap.get_current_joint_position(0)

for i, joint in enumerate(joints):
    print(f"J{i + 1} = {math.degrees(joint):.2f} deg")

controller.disconnect()
```

## With a tool and a frame

By default, the Cartesian position is the one of the flange, in the world frame. Pass a tool and a frame to get the position of the tool center point in the frame of your part or table.

- `tool`: position of the tool center point, given in the flange frame.
- `frame`: position of the reference frame, given in the world frame.

```python
from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.soap.data.cartesian_position import CartesianPosition

controller = StaubliController()
controller.connect("192.168.0.254")

# Tool center point, given in the flange frame: 120 mm along Z
tool = CartesianPosition()
tool.z = 0.120

# Reference frame, given in the world frame: a table 500 mm in front of the robot
frame = CartesianPosition()
frame.x = 0.500

position = controller.soap.get_current_cartesian_joint_position(0, tool, frame)

# Position of the tool center point in the table frame
tcp = position.cartesian_position

controller.disconnect()
```

Pass `null` (`None` in Python) for the flange or for the world frame.

## Position of a joint configuration

To get the Cartesian position of joint values that are not the current ones, use the forward kinematics: see [Kinematics](soap-kinematics.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference



**CartesianJointPosition** ([reference](../api/underautomation.staubli.soap.data.md#cartesianjointposition))

- `CartesianJointPosition()`
- `joints_position: typing.List[float]`: The joint positions in radians.
- `cartesian_position: CartesianPosition`: The Cartesian position of the robot end effector.

**CartesianPosition** ([reference](../api/underautomation.staubli.soap.data.md#cartesianposition))

- `CartesianPosition()`: Initializes a new instance of the CartesianPosition class.
- `x: float`: X translation component (m).
- `y: float`: Y translation component (m).
- `z: float`: Z translation component (m).
- `rx: float`: Rotation around the X axis (radians).
- `ry: float`: Rotation around the Y axis (radians).
- `rz: float`: Rotation around the Z axis (radians).
