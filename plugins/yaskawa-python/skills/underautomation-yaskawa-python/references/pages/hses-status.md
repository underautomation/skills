# Status and servo

Read the mode and the state of a Yaskawa controller, switch the servo power, hold the robot, select the cycle mode, lock the pendant and show a message on it.

Web page: https://underautomation.com/yaskawa/documentation/hses-status

This page shows how to read the state of a Yaskawa Motoman controller with the SDK, and how to change it: servo power, hold, cycle mode, pendant lock and pendant message. It covers every controller with the High Speed Ethernet Server.

## Read the status

`GetStatusInformation()` reads the mode, the execution state, the hold and the alarm flags in one request.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

status = robot.high_speed_e_server.get_status_information()

# Mode of the controller
print(f"Teach: {status.teach}, play: {status.play}, remote: {status.command_remote}")

# Cycle mode: step, one cycle or automatic (continuous)
print(f"Step: {status.step}, cycle: {status.cycle}, automatic: {status.automatic}")

# Execution
print(f"Running: {status.running}, servo on: {status.servo_on}")

# Hold, from the pendant, from an external signal or from a command
print(f"Hold: {status.in_hold_status_pendant} {status.in_hold_status_externally} {status.in_hold_status_by_command}")

# Alarm and error
print(f"Alarm: {status.alarming}, error: {status.error_occurring}")

robot.disconnect()
```

| Property                     | `true` when                                                          |
| ---------------------------- | -------------------------------------------------------------------- |
| `Teach`, `Play`              | The controller is in teach mode, in play mode                        |
| `CommandRemote`              | The controller accepts the commands of the PC                        |
| `Step`, `Cycle`, `Automatic` | The cycle mode: step, one cycle, continuous                          |
| `Running`                    | A job or a move is executed                                          |
| `ServoOn`                    | The servo power is on                                                |
| `InHoldStatusPendant`        | The hold button of the pendant is pressed                            |
| `InHoldStatusExternally`     | The external hold signal is on                                       |
| `InHoldStatusByCommand`      | A hold was sent by `SetHold(true)`                                   |
| `Alarming`                   | An alarm is active, see [Alarms](hses-alarms.md) |
| `ErrorOccurring`             | An error message is shown                                            |
| `InGuardSafeOperation`       | The robot is in guard safe operation                                 |

The status is a snapshot. To follow its changes, read it in a loop: see [Monitor the state of the robot](how-to-monitor-state.md).

## Servo power and hold

`SetServo(on)` switches the servo power, `SetHold(on)` holds the robot or releases the hold. Both need the remote mode.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Switch the servo power on. The SDK waits up to power_on_timeout_milliseconds (8 s)
robot.high_speed_e_server.set_servo(True)

# Hold the robot, then release the hold
robot.high_speed_e_server.set_hold(True)
robot.high_speed_e_server.set_hold(False)

# Switch the servo power off
robot.high_speed_e_server.set_servo(False)

robot.disconnect()
```

| Method                          | `true`                                            | `false`          |
| ------------------------------- | ------------------------------------------------- | ---------------- |
| `SetServo`                      | Servo power on                                    | Servo power off  |
| `SetHold`                       | Hold: the robot stops on its path, servo stays on | Release the hold |
| `SetTeachPendantLockState`      | Lock the pendant                                  | Unlock the pendant |

The servo power takes several seconds to come on. For `SetServo(true)` the SDK waits `PowerOnTimeoutMilliseconds` (8000 ms by default) instead of `DataTimeoutMilliseconds`.

`ServoCommand(OnOffCommandType, value)` of the previous versions does the same and still works. It is marked obsolete: use the methods above in new code. They have the same names on the [Ethernet Server](eserver-status.md).

## Lock the pendant

When a PC drives the cell, lock the pendant so that nobody changes the mode or starts a job from it at the same time.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Lock the programming pendant, so that nobody changes the mode or starts a job from it
robot.high_speed_e_server.set_teach_pendant_lock_state(True)

# Unlock it
robot.high_speed_e_server.set_teach_pendant_lock_state(False)

robot.disconnect()
```

## Cycle mode

`SetCycle(cycle)` selects how a job runs when it is started: step by step, one cycle, or in a loop.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.common.robot_cycle_type import RobotCycleType

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Execute the job step by step
robot.high_speed_e_server.set_cycle(RobotCycleType.Step)

# Execute the job once
robot.high_speed_e_server.set_cycle(RobotCycleType.OneCycle)

# Execute the job in a loop
robot.high_speed_e_server.set_cycle(RobotCycleType.Automatic)

robot.disconnect()
```

| `RobotCycleType` | The job runs                |
| ---------------- | --------------------------- |
| `Step`           | One line at each start      |
| `OneCycle`       | Once, then stops            |
| `Automatic`      | In a loop                   |

`SwitchingCommand(SwitchingCommands)` of the previous versions does the same and is marked obsolete.

## Message on the pendant

`Display(message)` shows a message to the operator on the programming pendant. The message has 24 characters at most: a longer one is cut.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))

# Show a message on the programming pendant, 24 characters at most
robot.high_speed_e_server.display("Part 42 done")

robot.disconnect()
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/underautomation.yaskawa.high_speed_e_server.internal.md#highspeedeserverclientbase-robothigh_speed_e_server))

- `display(message: str) -> RobotDataHeader`: Displays a popup message on the robot programming pendant. Message will appear as a notification to the operator.

**RobotStatusData** ([reference](../api/underautomation.yaskawa.high_speed_e_server.md#robotstatusdata))

- `step: bool (read only)`: Gets whether the robot is in step (single-step) execution mode. When true, the robot executes one instruction at a time.
- `cycle: bool (read only)`: Gets whether the robot is in cycle execution mode. When true, the robot executes one complete cycle then stops.
- `automatic: bool (read only)`: Gets whether the robot is in automatic operation mode. When true, the robot can operate automatically without pendant interaction.
- `running: bool (read only)`: Gets whether the robot is currently running (executing a job).
- `in_guard_safe_operation: bool (read only)`: Gets whether the robot is in guard safe operation mode. Indicates collaborative/safety-rated operation mode is active.
- `teach: bool (read only)`: Gets whether the robot is in teach mode. In teach mode, the robot can be manually positioned and jobs can be edited.
- `play: bool (read only)`: Gets whether the robot is in play mode. In play mode, the robot can execute programmed jobs.
- `command_remote: bool (read only)`: Gets whether remote command mode is enabled. When true, the robot accepts commands from external sources (including this API).
- `in_hold_status_pendant: bool (read only)`: Gets whether the robot is held by the programming pendant. Operator has pressed hold on the pendant.
- `in_hold_status_externally: bool (read only)`: Gets whether the robot is held by an external hold signal. External safety circuit has triggered a hold condition.
- `in_hold_status_by_command: bool (read only)`: Gets whether the robot is held by a command (software hold). A hold command was issued via the API or job instruction.
- `alarming: bool (read only)`: Gets whether an alarm is currently active. Check GetAlarm() for detailed alarm information.
- `error_occurring: bool (read only)`: Gets whether an error condition is occurring. Errors may prevent normal operation until resolved.
- `servo_on: bool (read only)`: Gets whether servo power is enabled. Servo must be ON for the robot to move.

**RobotCycleType** ([reference](../api/underautomation.yaskawa.common.md#robotcycletype))

- Step: Step mode : execute one instruction at a time.
- OneCycle: One cycle mode : execute one complete cycle then stop.
- Automatic: Automatic mode : continuous operation.
