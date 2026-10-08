# Monitor the state of the robot

Poll the mode, the servo, the hold, the alarms and the job of a Yaskawa controller, and print each change of state.

Web page: https://underautomation.com/yaskawa/documentation/how-to-monitor-state

This article shows how to follow the state of a Yaskawa Motoman controller from a PC, in C# or Python. It gives a complete program that reads the mode, the servo, the hold, the alarm and the job every 200 ms, and prints each change.

## Prerequisites

- The SDK is connected to the controller: see [Connect to your robot](connect.md).
- Nothing else: all these reads work in any mode.

## What to read

| Information                        | Method                              |
| ---------------------------------- | ----------------------------------- |
| Mode, servo, running, hold, alarm  | `GetStatusInformation()`            |
| Name and line of the executing job | `GetExecutingJobInformation()`      |
| Code and text of the alarm         | `GetAlarm(RobotRecentAlarm.Latest)` |
| Position of the robot              | `GetRobotCartesianPosition()`       |
| Variables written by the job       | `ReadInteger`, `ReadByte`...        |

The SDK has no event: it reads when you call it. A monitor is a loop that reads, compares with the last value, and reacts to the changes.

## Example

```python
import time
from datetime import datetime
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters
from underautomation.yaskawa.high_speed_e_server.robot_recent_alarm import RobotRecentAlarm

robot = YaskawaRobot()
robot.connect(ConnectParameters("192.168.0.1"))
hses = robot.high_speed_e_server

last = None

# Poll every 200 ms for 1 minute and print each change
for _ in range(300):
    status = hses.get_status_information()
    job = hses.get_executing_job_information()

    mode = "PLAY" if status.play else "TEACH" if status.teach else "?"
    hold = status.in_hold_status_pendant or status.in_hold_status_externally or status.in_hold_status_by_command
    state = (f"{mode} servo={'on' if status.servo_on else 'off'} running={status.running} "
             f"hold={hold} alarm={status.alarming} job={job.name}")

    if state != last:
        print(f"{datetime.now():%H:%M:%S} {state}")

        if status.alarming:
            alarm = hses.get_alarm(RobotRecentAlarm.Latest)
            print(f"  alarm {alarm.code}: {alarm.text}")

        last = state

    time.sleep(0.2)

robot.disconnect()
```

The program builds a line of text from the status and the job, and prints it only when it changes. When an alarm is active, it also prints the latest alarm.

## Polling period

Each read is one request. Two reads every 200 ms is 10 requests per second. Choose the period from what you need to see: 100 ms to 500 ms for a supervision screen, a few seconds for a log.

Run the loop in its own thread, so that the user interface stays responsive. One `YaskawaRobot` can be used by several threads: the SDK sends one request at a time.

## With the Ethernet Server

The same loop works with the [Ethernet Server](ethernet-server.md): `GetStatusInformation()` has the same flags. A call takes about 20 ms on a YRC1000micro, against 10 ms with the High Speed Ethernet Server: keep a polling period of 100 ms or more. To write the loop once for both protocols, use the common interfaces, see [Choose a protocol](protocols.md#write_code_for_both_protocols).

The Ethernet Server also reads the temperature of the encoders and the maximum torque of each axis, to follow the robot over a shift.

```python
from underautomation.yaskawa.yaskawa_robot import YaskawaRobot
from underautomation.yaskawa.connect_parameters import ConnectParameters

parameters = ConnectParameters("192.168.0.1")
parameters.e_server.enable = True
robot = YaskawaRobot()
robot.connect(parameters)

# Torque of each axis, in percent of the rated torque
torque = robot.e_server.get_torque()
max_torque = robot.e_server.get_max_torque()

# Temperature of the encoder of each axis, in degrees Celsius
temperatures = robot.e_server.get_encoder_temperature()

for axis in range(6):
    print(f"Axis {axis + 1}: {torque.values[axis]} % (max {max_torque.values[axis]} %), {temperatures.values[axis]} C")

robot.disconnect()
```

## Troubleshooting

- **A `SocketException` from time to time:** a request did not get its answer before `DataTimeoutMilliseconds`. Catch it in the loop, count the failures, and report a lost connection after several failures in a row.
- **The job name is empty:** no job is selected.

## What to read next

- [Status and servo](hses-status.md): all the flags of the status.
- [Read and reset alarms](how-to-read-reset-alarms.md).
