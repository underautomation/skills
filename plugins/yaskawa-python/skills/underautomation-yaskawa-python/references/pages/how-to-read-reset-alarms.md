# Read and reset alarms

Detect an alarm of a Yaskawa controller, read its code and text, reset it and check the result, from C# or Python.

Web page: https://underautomation.com/yaskawa/documentation/how-to-read-reset-alarms

This article shows how to detect an alarm of a Yaskawa Motoman controller from a PC, read its code and its text, and reset it, in C# or Python. It gives a complete program that checks the result of the reset.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- To reset, the controller accepts the remote commands. Reading the alarms works in any mode.

## Alarm or error

| State                           | Detect                                  | Clear                               |
| ------------------------------- | --------------------------------------- | ----------------------------------- |
| Alarm: the controller stops     | `GetStatusInformation().Alarming`       | `AlarmReset(AlarmResetType.Reset)`  |
| Error: a message on the pendant | `GetStatusInformation().ErrorOccurring` | `AlarmReset(AlarmResetType.Cancel)` |

`GetAlarm` reads the code, the sub code, the time and the text of each alarm. `GetAlarmExtended` adds the texts of the sub codes.

## Example

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.alarm_reset_type import AlarmResetType
from underautomation.yaskawa.high_speed_e_server.robot_recent_alarm import RobotRecentAlarm

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))
hses = robot.high_speed_e_server

status = hses.get_status_information()

if status.alarming or status.error_occurring:
    # 1. Read the alarms, the latest first
    for which in RobotRecentAlarm:
        alarm = hses.get_alarm(which)
        if alarm.code != 0:
            print(f"{alarm.occurring_time} {alarm.code} {alarm.text}")

    # 2. Remove the cause on the cell, then reset
    hses.alarm_reset(AlarmResetType.Reset if status.alarming else AlarmResetType.Cancel)

    # 3. Check that the alarm is gone
    status = hses.get_status_information()
    print("The alarm is still active" if status.alarming else "Alarm reset")

robot.disconnect()
```

The program:

1. reads the status, and stops if there is no alarm and no error;
2. prints each alarm reported by the controller, the most recent first;
3. resets the alarm, or cancels the error;
4. reads the status again to check that the alarm is gone.

## Before the reset

A reset does not remove the cause of the alarm. If the cause is still present, the alarm comes back at once. Log the code and the text before the reset, and let an operator check the cell when the alarm concerns safety or a collision.

## With the Ethernet Server

The [Ethernet Server](ethernet-server.md) reads the error and the 4 alarms with their code, sub code and text in one call, `GetAlarmWithMessages()`. `AlarmReset()` resets the alarms and `ErrorCancel()` removes the error.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Active error and alarms, with their text
alarms = robot.e_server.get_alarm_with_messages()

if alarms.error is not None and alarms.error.code != 0:
    print(f"Error {alarms.error.code}: {alarms.error.message}")

for alarm in alarms.alarms:
    if alarm.code != 0:  # empty entries have the code 0
        print(f"Alarm {alarm.code} ({alarm.sub_code}): {alarm.message}")

# Reset the alarms, cancel the error (remote mode)
if alarms.alarm_count > 0:
    robot.e_server.alarm_reset()
robot.e_server.error_cancel()

robot.disconnect()
```

## Troubleshooting

- **The reset is refused:** the remote mode is off. See [Prepare the controller](connect.md#prepare_the_controller).
- **The alarm comes back:** its cause is still present. Look for the code in the alarm manual of your controller.
- **`Code` is `0`:** there is no alarm at this position of the list.

## What to read next

- [Alarms](hses-alarms.md): the reference of the alarm methods.
- [Monitor the state of the robot](how-to-monitor-state.md).
