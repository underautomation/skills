# System information and parameters

Read the software version, the axis names, the operating times and the system parameters (S1CG, RS...) of a Yaskawa controller.

Web page: https://underautomation.com/yaskawa/documentation/hses-system

This page shows how to read the identity and the configuration of a Yaskawa Motoman controller with the SDK: software version, axis names, operating times and system parameters. All these methods only read: they work in any mode.

## Software version and robot model

`GetSystemInformation()` reads the system software version, the model of the first robot (R1) and the version of its parameters.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_system_type_data import RobotSystemTypeData

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Software version, robot model and parameter version of the first robot (R1)
info = robot.high_speed_e_server.get_system_information(RobotSystemTypeData.Default)
print(f"{info.software_version} {info.name} {info.parameter}")

robot.disconnect()
```

Log these values with the data of your application: the answers of the controller can depend on its software version.

`GetSystemInformation(RobotSystemTypeData)` reads the same values for another robot, a station or an application, on the controllers that have several. In Python 2.2.0, only this form exists: pass `RobotSystemTypeData.Default` for the first robot.

## Axis names

`GetConfigurationInformation(group)` reads the names of the axes of a control group, for example `S L U R B T` for a 6 axis robot. Use it to check the number of axes before you read the joint positions.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_control_group import RobotControlGroup

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Names of the axes of the first robot, for example S, L, U, R, B, T
group = RobotControlGroup.DefaultRobotPulse
config = robot.high_speed_e_server.get_configuration_information(group)

print(" ".join(config.axes))

robot.disconnect()
```

`RobotControlGroup` selects the robot, the base axes or the station, and its number. See [Positions](hses-positions.md#other_control_groups).

## Operating times

`GetManagementTime(type, index)` reads an operating time of the controller: its start date and the elapsed time, as texts of the controller.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.management_time_type import ManagementTimeType

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Time since the control power was switched on
power = robot.high_speed_e_server.get_management_time(ManagementTimeType.ControlPowerOnTime)
print(f"Since {power.start_time}: {power.ellapse_time}")

# Servo power time and motion time of the first robot (index 1 is R1)
servo = robot.high_speed_e_server.get_management_time(ManagementTimeType.ServoPowerOnTimR1ToR8, 1)
motion = robot.high_speed_e_server.get_management_time(ManagementTimeType.MotionTimeR1ToR8, 1)
print(f"Servo on: {servo.ellapse_time}, moving: {motion.ellapse_time}")

robot.disconnect()
```

| `ManagementTimeType`           | Time                        | `index`                   |
| ------------------------------ | --------------------------- | ------------------------- |
| `ControlPowerOnTime`           | Control power on            | `0`                       |
| `ServoPowerOnTimR1ToR8`        | Servo power on of a robot   | `1` to `8` for R1 to R8   |
| `ServoPowerOnTimeS1ToS24`      | Servo power on of a station | `1` to `24` for S1 to S24 |
| `PlayBackTimeR1ToR8`           | Playback of a robot         | `1` to `8`                |
| `PlayBackTimeS1ToS24`          | Playback of a station       | `1` to `24`               |
| `MotionTimeR1ToR8`             | Motion of a robot           | `1` to `8`                |
| `OperationTimeApplication1To8` | Operation of an application | `1` to `8`                |

The totals (`ServoPowerOnTimeTotal`, `PlayBackTimeTotal`, `MotionTimeTotal`) take the index `0`. These times help to plan the maintenance, or to measure the use of a cell over a shift.

## System parameters

`GetSystemParameter(type, number, group)` reads one system parameter of the controller as an unsigned integer. For example, `RS029` and `RS214` must be `1` to overwrite files (see [Connect to your robot](connect.md#allow_the_file_overwrite)).

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.system_parameter_types import SystemParameterTypes

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Parameter RS029 of the controller (RS parameters have no group)
rs029 = robot.high_speed_e_server.get_system_parameter(SystemParameterTypes.RS, 29, 0)
print(f"RS029 = {rs029.value}")

# Parameter S1CG000 of the first robot (group 1)
s1cg = robot.high_speed_e_server.get_system_parameter(SystemParameterTypes.S1CG, 0, 1)
print(f"S1CG000 = {s1cg.value}")

robot.disconnect()
```

| `SystemParameterTypes`    | `group`                             |
| ------------------------- | ----------------------------------- |
| `S2C`, `S3C`, `S4C`, `RS` | `0`: these parameters have no group |
| `S1CG`, `AP`, `SE`        | The number of the group, from `1`   |

The meaning of each parameter is in the parameter manual of your controller. The SDK reads the parameters, it does not write them.

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**RobotSystemInformation** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotsysteminformation))

- `software_version: str (read only)`: Gets the controller software version string. Format typically includes model and version number. Maximum 24 characters.
- `name: str (read only)`: Gets the system/robot name or model identifier. Maximum 16 characters.
- `parameter: str (read only)`: Gets parameter file or configuration information. Maximum 8 characters.

**RobotAxisConfigData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotaxisconfigdata))

- `axes: typing.List[str] (read only)`: Gets the array containing all axis values. Index 0-5 typically represent robot axes (S, L, U, R, B, T). Index 6-7 may be used for additional axes if available.
- `axis1: str`: Gets or sets the value for axis 1 (typically S-axis / base rotation).
- `axis2: str`: Gets or sets the value for axis 2 (typically L-axis / lower arm).
- `axis3: str`: Gets or sets the value for axis 3 (typically U-axis / upper arm).
- `axis4: str`: Gets or sets the value for axis 4 (typically R-axis / wrist rotation).
- `axis5: str`: Gets or sets the value for axis 5 (typically B-axis / wrist bend).
- `axis6: str`: Gets or sets the value for axis 6 (typically T-axis / tool rotation).
- `axis7: str`: Gets or sets the value for axis 7 (optional additional axis).
- `axis8: str`: Gets or sets the value for axis 8 (optional additional axis).

**RobotManagementTimeData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotmanagementtimedata))

- `start_time: str (read only)`: Gets the start time of the tracked period. Format: "YYYY/MM/DD HH:MM" (16 characters).
- `ellapse_time: str (read only)`: Gets the elapsed time for the tracked metric. Format: "HHHH:MM:SS.ss" or similar time duration format (12 characters).

**ManagementTimeType** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#managementtimetype))

- ControlPowerOnTime: Total time the controller power has been on.
- ServoPowerOnTimeTotal: Total servo power on time across all robots.
- ServoPowerOnTimR1ToR8: Servo power on time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- ServoPowerOnTimeS1ToS24: Servo power on time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- PlayBackTimeTotal: Total playback time across all robots.
- PlayBackTimeR1ToR8: Playback time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- PlayBackTimeS1ToS24: Playback time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- MotionTimeTotal: Total motion time across all robots.
- MotionTimeR1ToR8: Motion time for robots R1 through R8. Pass the robot number (1 to 8) as index of GetManagementTime.
- MotionTimeS1ToS24: Motion time for stations S1 through S24. Pass the station number (1 to 24) as index of GetManagementTime.
- OperationTimeApplication1To8: Operation time for applications 1 through 8. Add application number (0-7) to get specific application.

**RobotSystemParamData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotsystemparamdata))

- `value: int (read only)`: Gets the raw system parameter value returned by the controller.

**SystemParameterTypes** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#systemparametertypes))

- S1CG: S1CxG. requires group number.
- S2C: S2C
- S3C: S3C
- S4C: S4C
- RS: RS
- AP: AxP. Requires a group number.
- SE: SxE. Requires a group number.
