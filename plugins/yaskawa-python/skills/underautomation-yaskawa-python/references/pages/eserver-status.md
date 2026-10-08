# Status, alarms and servo

Read the state and the alarms with their text through the Ethernet Server, reset them, switch the servo, hold the robot, set the cycle, the mode and the pendant lock.

Web page: https://underautomation.com/yaskawa/documentation/eserver-status

This page shows how to read the state and the alarms of a Yaskawa Motoman controller through the Ethernet Server, and how to change the state: servo power, hold, cycle mode, operation mode, pendant lock and pendant message. It covers the YRC1000 and YRC1000micro controllers.

## Read the status

`GetStatusInformation()` reads the mode, the execution state, the hold and the alarm flags in one command.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

status = robot.e_server.get_status_information()

print(f"Teach: {status.teach}, play: {status.play}")
print(f"Remote: {status.command_remote}, servo: {status.servo_on}")
print(f"Running: {status.running}, speed limit: {status.speed_limit}")
print(f"Alarm: {status.alarming}, error: {status.error_occurring}")
print(f"Hold by pendant: {status.in_hold_status_pendant}, by command: {status.in_hold_status_by_command}")

robot.disconnect()
```

| Property                     | `true` when                                         |
| ---------------------------- | --------------------------------------------------- |
| `Teach`, `Play`              | The controller is in teach mode, in play mode       |
| `CommandRemote`              | The controller accepts the commands of the PC       |
| `Step`, `Cycle`, `Automatic` | The cycle mode: step, one cycle, continuous         |
| `Running`                    | A job or a move is executed                         |
| `SpeedLimit`                 | The speed is limited (teach mode safe speed)        |
| `ServoOn`                    | The servo power is on                               |
| `InHoldStatusPendant`        | The hold button of the pendant is pressed           |
| `InHoldStatusExternally`     | The external hold signal is on                      |
| `InHoldStatusByCommand`      | A hold was sent by `SetHold(true)`                  |
| `Alarming`                   | An alarm is active                                  |
| `ErrorOccurring`             | An error message is shown                           |

`RawData1` and `RawData2` hold the same flags as two numbers, to log them or compare two status reads in one test.

## Alarms

### Read the alarms with their text

`GetAlarmWithMessages()` reads the active error and the 4 alarms of the controller, with the code, the sub code and the text of each one.

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

| Property     | Content                                                         |
| ------------ | --------------------------------------------------------------- |
| `Error`      | The error message, if any. `Code` is 0 when there is no error   |
| `Alarms`     | 4 entries. An entry with the code 0 is empty                    |
| `AlarmCount` | Number of active alarms                                         |

`GetAlarm()` reads the codes only, in arrays: index 0 is the error, indexes 1 to 4 are the alarms. It is faster when the text is not needed.

### Reset an alarm

`AlarmReset()` resets the alarms, `ErrorCancel()` removes the error message. Both need the remote mode. The cause of the alarm must be removed first, or the alarm comes back.

## Servo, hold and cycle

Each command of this section needs the remote mode.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.common.robot_cycle_type import RobotCycleType
from underautomation.yaskawa.common.robot_mode import RobotMode

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Each command needs the remote mode
robot.e_server.set_servo(True)   # waits up to power_on_timeout_milliseconds
robot.e_server.set_hold(True)    # stop on the path, the servo stays on
robot.e_server.set_hold(False)

# Cycle mode of the next job start
robot.e_server.set_cycle(RobotCycleType.OneCycle)

# Teach or play mode (needs the external mode switch)
robot.e_server.set_mode(RobotMode.Play)

# Lock the pendant, show a message to the operator (30 characters)
robot.e_server.set_teach_pendant_lock_state(True)
robot.e_server.display("Cell driven by the PC")

robot.e_server.set_servo(False)

robot.disconnect()
```

| Method                              | Effect                                                                      |
| ----------------------------------- | --------------------------------------------------------------------------- |
| `SetServo(true)`, `SetServo(false)` | Servo power on or off. The SDK waits up to `PowerOnTimeoutMilliseconds`     |
| `SetHold(true)`, `SetHold(false)`   | Hold: the robot stops on its path, the servo stays on. Then release it      |
| `SetCycle(RobotCycleType)`          | `Step`, `OneCycle` or `Automatic` for the next job start                    |
| `SetMode(RobotMode)`                | `Teach` or `Play`                                                           |
| `SetTeachPendantLockState(true)`    | Locks the pendant and the I/O operation signals. The emergency stop stays active |
| `Display(message)`                  | Shows a message on the pendant, 30 characters at most                       |

`SetMode` works only when the external mode switch is enabled on the `OPERATING CONDITION` window of the controller. Otherwise the controller refuses it.

When a PC drives the cell, lock the pendant so that nobody changes the mode or starts a job from it at the same time.

## Reference

**Methods of HostControlClientBase** ([reference](../api/underautomation.yaskawa.host_control.internal.md#hostcontrolclientbase-robote_server))

- `display(message: str) -> HostControlResponse`: Displays a message on the remote display of the teach pendant. Command remote must be enabled on the controller.

**HostControlStatusData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolstatusdata))

- `step: bool (read only)`: Gets whether the robot is in step (single-step) execution mode. When true, the robot executes one instruction at a time.
- `cycle: bool (read only)`: Gets whether the robot is in cycle execution mode. When true, the robot executes one complete cycle then stops.
- `automatic: bool (read only)`: Gets whether the robot is in automatic operation mode. When true, the robot can operate automatically without pendant interaction.
- `running: bool (read only)`: Gets whether the robot is currently running (executing a job).
- `speed_limit: bool (read only)`: Gets whether speed limit is active.
- `teach: bool (read only)`: Gets whether the robot is in teach mode. In teach mode, the robot can be manually positioned and jobs can be edited.
- `play: bool (read only)`: Gets whether the robot is in play mode. In play mode, the robot can execute programmed jobs.
- `command_remote: bool (read only)`: Gets whether remote command mode is enabled. When true, the robot accepts commands from external sources (including this API).
- `servo_on: bool (read only)`: Gets whether servo power is enabled. Servo must be ON for the robot to move.
- `error_occurring: bool (read only)`: Gets whether an error condition is occurring. Errors may prevent normal operation until resolved.
- `alarming: bool (read only)`: Gets whether an alarm is currently active. Check GetAlarm() for detailed alarm information.
- `in_hold_status_by_command: bool (read only)`: Gets whether the robot is held by a command (software hold). A hold command was issued via the API or job instruction.
- `in_hold_status_externally: bool (read only)`: Gets whether the robot is held by an external hold signal. External safety circuit has triggered a hold condition.
- `in_hold_status_pendant: bool (read only)`: Gets whether the robot is held by the programming pendant. Operator has pressed hold on the pendant.
- `raw_data1: int (read only)`: Gets the first raw status word from the controller response.
- `raw_data2: int (read only)`: Gets the second raw status word from the controller response.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

**HostControlAlarmStringData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolalarmstringdata))

- `alarm_count: int (read only)`: Gets the number of active alarms (entries of alarms with a code other than 0).
- `error: HostControlAlarmEntry (read only)`: Gets the active error. Its code is 0 when no error is active.
- `alarms: typing.List[HostControlAlarmEntry] (read only)`: Gets the alarm entries with codes and text messages (always 4 entries, the code of an unused entry is 0).
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

**HostControlAlarmEntry** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolalarmentry))

- `code: int (read only)`: Gets the alarm code number.
- `sub_code: int (read only)`: Gets the alarm sub-code (data).
- `message: str (read only)`: Gets the alarm text message.

**HostControlAlarmData** ([reference](../api/underautomation.yaskawa.host_control.md#hostcontrolalarmdata))

- `codes: typing.List[int] (read only)`: Gets the codes (5 entries). Index 0 is the code of the active error, indexes 1 to 4 are the codes of the active alarms. A code of 0 means no error or no alarm.
- `data: typing.List[int] (read only)`: Gets the sub-codes (5 entries), at the same index as codes. Index 0 is the sub-code of the error, indexes 1 to 4 are the data of the alarms.
- Inherited from [HostControlResponse](../api/underautomation.yaskawa.host_control.md#hostcontrolresponse): `response_code`, `command`, `success`, `error_message`

**RobotCycleType** ([reference](../api/underautomation.yaskawa.common.md#robotcycletype))

- Step: Step mode : execute one instruction at a time.
- OneCycle: One cycle mode : execute one complete cycle then stop.
- Automatic: Automatic mode : continuous operation.

**RobotMode** ([reference](../api/underautomation.yaskawa.common.md#robotmode))

- Teach: Teach mode : robot can be manually positioned and jobs can be edited.
- Play: Play mode : robot can execute programmed jobs.

## What to read next

- [Jobs](eserver-jobs.md): select and start a job, wait for its end.
- [Read and reset alarms](how-to-read-reset-alarms.md): a complete program.
