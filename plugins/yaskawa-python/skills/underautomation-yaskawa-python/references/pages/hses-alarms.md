# Alarms

Read up to 4 alarms of a Yaskawa controller with their code, text and time, read the sub codes, then reset the alarms or cancel an error.

Web page: https://underautomation.com/yaskawa/documentation/hses-alarms

This page shows how to read the alarms of a Yaskawa Motoman controller with the SDK, and how to reset them from a PC. It covers every controller with the High Speed Ethernet Server.

## Read the alarms

The controller reports up to 4 alarms. `GetAlarm(which)` reads one of them, with its code, its text and the time it occurred.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_recent_alarm import RobotRecentAlarm

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# The controller reports up to 4 alarms, the most recent first
for which in RobotRecentAlarm:
    alarm = robot.high_speed_e_server.get_alarm(which)

    # Code 0 means that there is no alarm at this position
    if alarm.code == 0:
        continue

    print(f"{which.name}: {alarm.code} {alarm.text} at {alarm.occurring_time} (data {alarm.data}, type {alarm.type})")

robot.disconnect()
```

| Property        | Content                                                           |
| --------------- | ----------------------------------------------------------------- |
| `Code`          | Alarm number, as shown on the pendant. `0` when there is no alarm |
| `Data`          | Sub code of the alarm                                             |
| `Type`          | Type of the sub code                                              |
| `OccurringTime` | Date and time of the alarm, as a text of the controller           |
| `Text`          | Name of the alarm                                                 |

`RobotRecentAlarm.Latest` is the most recent alarm, `FourthLatest` the oldest of the four. `GetStatusInformation().Alarming` tells if an alarm is active, in one short request: test it first, then read the alarms.

The meaning of each code and the action to take are in the alarm manual of your controller.

## Read the sub codes

`GetAlarmExtended(which)` returns the same values, plus the texts of the sub codes. Use it to log the full context of an alarm.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_recent_alarm import RobotRecentAlarm

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Same as get_alarm, plus the sub code texts of the alarm
alarm = robot.high_speed_e_server.get_alarm_extended(RobotRecentAlarm.Latest)

print(f"{alarm.code} {alarm.text} at {alarm.occurring_time}")
print(f"Information: {alarm.additionnal_information}")
print(f"Sub data: {alarm.sub_data}")

robot.disconnect()
```

## Reset an alarm

`AlarmReset(type)` resets the alarms or cancels an error. It needs the remote mode. Remove the cause first: an alarm whose cause is still present comes back.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.alarm_reset_type import AlarmResetType

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

status = robot.high_speed_e_server.get_status_information()

# Reset the alarms, once their cause is removed
if status.alarming:
    robot.high_speed_e_server.alarm_reset(AlarmResetType.Reset)

# Cancel an error (a message that does not stop the controller)
if status.error_occurring:
    robot.high_speed_e_server.alarm_reset(AlarmResetType.Cancel)

robot.disconnect()
```

| `AlarmResetType` | Use                                                               |
| ---------------- | ----------------------------------------------------------------- |
| `Reset`          | Reset the alarms (`GetStatusInformation().Alarming`)              |
| `Cancel`         | Cancel an error message (`GetStatusInformation().ErrorOccurring`) |

A complete program, with the check after the reset, is in [Read and reset alarms](how-to-read-reset-alarms.md).

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/underautomation.yaskawa.high_speed_e_server.internal.md#highspeedeserverclientbase-robothigh_speed_e_server))

- `get_alarm(alarm: RobotRecentAlarm) -> RobotAlarmData`: Reads alarm information from the robot controller. Retrieves alarm code, type, occurrence time, and descriptive text.
- `alarm_reset(type: AlarmResetType) -> RobotDataHeader`: Resets alarms or cancels errors on the robot controller. Use Reset to clear alarm conditions after resolving the cause. Use Cancel for recoverable errors that don't require alarm reset.
- `get_alarm_extended(alarm: RobotRecentAlarm) -> RobotAlarmDataExtended`: Retrieves extended alarm information including sub-code character strings. Provides more detailed information than GetAlarm for troubleshooting.

**RobotAlarmData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotalarmdata))

- `code: int (read only)`: Gets the alarm code identifying the specific alarm type. Alarm codes are documented in the robot's maintenance manual.
- `data: int (read only)`: Gets additional alarm data providing context about the alarm. The meaning depends on the specific alarm code.
- `type: int (read only)`: Gets the alarm type/category classification.
- `occurring_time: str (read only)`: Gets the timestamp when the alarm occurred. Format: "YYYY/MM/DD HH:MM:SS" (16 characters).
- `text: str (read only)`: Gets the alarm message text describing the alarm condition. Maximum 32 characters.

**RobotAlarmDataExtended** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotalarmdataextended))

- `additionnal_information: str (read only)`: Gets additional information about the alarm condition. Maximum 16 characters.
- `sub_data: str (read only)`: Gets the sub-code data providing detailed error context. Maximum 96 characters.
- `sub_data_reverse: str (read only)`: Gets the reversed sub-code data. Maximum 96 characters.
- Inherited from [RobotAlarmData](../api/underautomation.yaskawa.high_speed_e_server.md#robotalarmdata): `code`, `data`, `type`, `occurring_time`, `text`

**RobotRecentAlarm** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotrecentalarm))

- Latest: The most recent (current) alarm.
- SecondLatest: The second most recent alarm.
- ThirdLatest: The third most recent alarm.
- FourthLatest: The fourth most recent alarm.

**AlarmResetType** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#alarmresettype))

- Reset: Reset the current alarm. Requires the alarm condition to be resolved.
- Cancel: Cancel the current error. Used for recoverable errors.
