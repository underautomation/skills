# Get the robot position

Read the position of a Staubli robot from C# or Python: joints, flange or tool position, and which method to choose. Complete program included.

Web page: https://underautomation.com/staubli/documentation/how-to-get-position

This article shows how to read the current position of a Staubli robot from a PC, in C# or Python, on a CS8 or CS9 controller. It compares the three ways that the SDK offers, then gives a complete program that prints the position of a tool 10 times per second.

## Prerequisites

- The PC reaches the controller, and the SDK is connected: see [Connect to your robot](connect.md).
- Nothing else: reading the position does not need the remote mode, the power or a VAL 3 program.

## Which method to choose

| You need                                             | Method                                                 | Requests |
| ---------------------------------------------------- | ------------------------------------------------------ | -------- |
| The joint values only                                | `GetCurrentJointPosition(robot)`                       | 1        |
| The joints and the flange or tool position           | `GetCurrentCartesianJointPosition(robot, tool, frame)` | 1        |
| The Cartesian position of joint values that you have | `ForwardKinematics(robot, joints)`                     | 1        |

- For a Cartesian position, `GetCurrentCartesianJointPosition` is the right choice: it gives the joints too, in the same request.
- Pass a `tool` to get the position of the tool center point instead of the flange, and a `frame` to get it in the frame of your part instead of the world frame.
- `ForwardKinematics` returns a full frame with its rotation matrix, and the configuration of the arm. Use it for positions that are not the current one.

## Example

```python
import math
import time

from underautomation.staubli.staubli_controller import StaubliController
from underautomation.staubli.soap.data.cartesian_position import CartesianPosition

controller = StaubliController()
controller.connect("192.168.0.254")

# Tool center point, 150 mm along Z of the flange
tool = CartesianPosition()
tool.z = 0.150

# Read the position 10 times per second, for 5 seconds
for _ in range(50):
    position = controller.soap.get_current_cartesian_joint_position(0, tool, None)
    tcp = position.cartesian_position

    # Meters to millimeters, radians to degrees
    print(
        f"X={tcp.x * 1000:.1f} Y={tcp.y * 1000:.1f} Z={tcp.z * 1000:.1f} mm, "
        f"J1={math.degrees(position.joints_position[0]):.2f} deg"
    )

    time.sleep(0.1)

controller.disconnect()
```

The SDK gives meters and radians. The program converts them to millimeters and degrees to print them.

## Polling period

Each read is one request to the controller. Its duration depends on the network and on the load of the controller: measure it on your cell (with a `Stopwatch` in C#, `time.perf_counter()` in Python) before you choose the period of your loop. Do not read faster than you need.

## Troubleshooting

- **The Cartesian position does not match the pendant:** the pendant shows the position of the current tool in the current frame. Pass the same tool and frame to `GetCurrentCartesianJointPosition`.
- **`InvalidRobotIdCode`:** the `robot` argument does not match an arm of the controller. Use `0` for the first arm, and see `GetRobots()`.
- **Values look too small:** they are in meters and radians. Multiply by 1000 for millimeters, and by 180/π for degrees.

## What to read next

- [Position](soap-position.md): the reference of the position methods.
- [Kinematics](soap-kinematics.md): forward and inverse kinematics.
- [Move the robot from a PC](how-to-move-robot.md).
