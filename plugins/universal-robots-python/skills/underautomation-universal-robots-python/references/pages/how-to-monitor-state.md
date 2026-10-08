# Monitor the state of the robot

Follow the robot mode, the program, the stops, the safety status and the connection of a UR cobot in C# or Python.

Web page: https://underautomation.com/universal-robots/documentation/how-to-monitor-state

This article shows how to follow the state of a Universal Robots cobot from a PC, in C# or Python: robot mode, power, program, protective and emergency stops, safety status and connection. It compares the interfaces and gives a program that prints each change.

## Which way to choose

| Way               | Frequency     | What it gives                                                                               |
| ----------------- | ------------- | ------------------------------------------------------------------------------------------- |
| Primary Interface | 10 Hz, events | `RobotModeData`: robot mode, power, program running or paused, stops, speed fraction. `MasterboardData.Safetymode` |
| RTDE              | Up to 500 Hz  | `RobotMode`, `SafetyMode`, `SafetyStatus`, `RuntimeState`, `RobotStatusBits`, `SpeedScaling`, as numbers |
| Dashboard Server  | When you ask  | `GetRobotMode()`, `GetProgramState()` with the name of the program, `GetSafetyStatus()`, `IsInRemoteControl()`, `GetOperationalMode()` |
| REST API          | When you ask  | `GetProgramState()` on PolyScope X                                                          |

The Primary Interface gives typed values and events, with no setup. RTDE gives the same states as numbers, faster: see the [RTDE guide](https://www.universal-robots.com/articles/ur/interface-communication/real-time-data-exchange-rtde-guide/) of Universal Robots for their values. The Dashboard Server adds the name of the loaded program and the remote control.

## Prerequisites

- The services `Primary Client Interface` and `Dashboard Server` are enabled: see [Prepare the robot](connect.md#prepare_the_robot).
- No remote control is needed to read the state.

## Example

The program prints the robot mode package when it changes, the safety status when it is not normal, and the loaded program every 2 s, until the connection is lost.

```python
import time
from datetime import datetime
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.common.safety_status import SafetyStatus

robot = UR()

# Primary Interface and Dashboard Server
robot.connect("192.168.0.1")

# Robot mode package, 10 times per second: print the changes only
last = [""]

def on_robot_mode(sender, e):
    m = robot.primary_interface.robot_mode_data
    state = (f"mode={m.robot_mode} powered={m.robot_power_on} running={m.program_running} "
             f"paused={m.program_paused} protective stop={m.protective_stopped} "
             f"emergency stop={m.emergency_stopped} speed={m.target_speed_fraction:.0%}")
    if state != last[0]:
        print(datetime.now().strftime("%H:%M:%S.%f")[:-3], state)
    last[0] = state

robot.primary_interface.robot_mode_data_received(on_robot_mode)

# Safety status, in the masterboard package
def on_masterboard(sender, e):
    safety = robot.primary_interface.masterboard_data.safetymode
    if safety != SafetyStatus.Normal:
        print("Safety:", safety)

robot.primary_interface.masterboard_data_received(on_masterboard)

# Lost connection: the property becomes False, there is no event
while robot.primary_interface.connected:
    # Loaded program and its state, every 2 s
    program = robot.dashboard.get_program_state()
    if program.succeed:
        print(f"{program.value.name}: {program.value.state}")
    time.sleep(2)

print("Connection lost")
```

The events run in a thread of the SDK. Keep them short, and copy the values you need to your own thread.

## Connection

`PrimaryInterface.Connected` and `Rtde.Connected` become `false` when the connection is lost: no event is raised and the SDK does not reconnect. Poll them, and call `Connect` again. `InternalErrorOccured` is raised for the errors of the background threads.

## What to read next

- [Read and reset alarms](how-to-read-reset-alarms.md): the messages of the controller and the safety status.
- [Primary Interface](data-streaming.md): the content of each package.
