# Get the robot position

Read the joint positions and the TCP position of a UR cobot in C# or Python, with RTDE up to 500 Hz or with the Primary Interface.

Web page: https://underautomation.com/universal-robots/documentation/how-to-get-position

This article shows how to read the current position of a Universal Robots cobot from a PC, in C# or Python: the 6 joint positions and the position of the tool center point (TCP). It compares the interfaces that give it and shows a complete program.

## Which way to choose

| Way                | Frequency          | Joint positions             | TCP position                       | When                                       |
| ------------------ | ------------------ | --------------------------- | ---------------------------------- | ------------------------------------------ |
| RTDE               | Up to 500 Hz       | `ActualQ`                   | `ActualTcpPose`                    | Fast monitoring, logging, closed loop      |
| Primary Interface  | 10 Hz              | `JointData.Base.Position`...| `CartesianInfo.AsPose()`           | Display, no setup, enabled by default      |
| Forward kinematics | No robot           | Your values                 | `KinematicsUtils.ForwardKinematics`| Offline computation, simulation            |

RTDE also gives the target positions (`TargetQ`, `TargetTcpPose`), the speeds and the forces. The Primary Interface also gives the TCP offset of the active tool (`CartesianInfo.TCPOffsetX`...).

## Units

| Value                  | Unit                                                        |
| ---------------------- | ----------------------------------------------------------- |
| Joint positions        | rad                                                         |
| X, Y, Z of the TCP     | m, in the base frame of the robot                           |
| RX, RY, RZ of the TCP  | rad, a rotation vector, as in URScript and PolyScope        |

To get roll, pitch and yaw, call `FromRotationVectorToRPY()`. See [Convert position types](tools.md).

## Prerequisites

- RTDE: the service `RTDE` is enabled on the robot. The Primary Interface: the service `Primary Client Interface`. See [Prepare the robot](connect.md#prepare_the_robot).
- No remote control is needed to read data.

## Example

The program connects with RTDE at 125 Hz and the Primary Interface, and prints the positions given by both.

```python
import time
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.connect_parameters import ConnectParameters
from underautomation.universal_robots.rtde.rtde_output_data import RtdeOutputData

robot = UR()

parameters = ConnectParameters("192.168.0.1")

# RTDE: joint and tool positions, 125 times per second
parameters.rtde.enable = True
parameters.rtde.frequency = 125
parameters.rtde.output_setup.add(RtdeOutputData.ActualQ)
parameters.rtde.output_setup.add(RtdeOutputData.ActualTcpPose)

# The Primary Interface is enabled by default: 10 packages per second
robot.connect(parameters)

# Wait for the first packages
time.sleep(0.5)

# 1. RTDE. Joint positions in rad, tool center point in m and rad
q = robot.rtde.output_data_values.actual_q
tcp = robot.rtde.output_data_values.actual_tcp_pose
print(f"RTDE joints: {q.base:.4f} {q.shoulder:.4f} {q.elbow:.4f} {q.wrist1:.4f} {q.wrist2:.4f} {q.wrist3:.4f}")
print(f"RTDE TCP: X={tcp.x:.4f} Y={tcp.y:.4f} Z={tcp.z:.4f} RX={tcp.rx:.4f} RY={tcp.ry:.4f} RZ={tcp.rz:.4f}")

# 2. Primary Interface. Same values, less often
tcp_10hz = robot.primary_interface.cartesian_info.as_pose()
shoulder = robot.primary_interface.joint_data.shoulder.position
print(f"Primary Interface TCP: X={tcp_10hz.x:.4f} Y={tcp_10hz.y:.4f} Z={tcp_10hz.z:.4f}")

# The orientation as roll, pitch, yaw, in degrees
rpy = tcp.from_rotation_vector_to_rpy()
print(f"Roll={rpy.rx_degrees:.2f} Pitch={rpy.ry_degrees:.2f} Yaw={rpy.rz_degrees:.2f}")

robot.disconnect()
```

To follow the position continuously, use the event `OutputDataReceived` of RTDE: see [Receive data](rtde.md#receive_data).

## Troubleshooting

- **The values are 0 or `null`:** no package is received yet. Wait about 100 ms after the connection.
- **`ConnectException` on RTDE:** the service `RTDE` is disabled, or port 30004 is blocked.
- **The pose differs from PolyScope:** PolyScope shows the TCP of the active tool, in the base frame or in a feature. The SDK gives the TCP in the base frame.

## What to read next

- [RTDE](rtde.md): the setup and the events.
- [Kinematics](kinematics.md): from joint positions to a pose, and back.
- [Move the robot from a PC](how-to-move-robot.md).
