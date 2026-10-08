# Read and reset alarms

Read the error messages, the program errors and the safety status of a UR cobot in C# or Python, and reset a protective stop or a safety fault.

Web page: https://underautomation.com/universal-robots/documentation/how-to-read-reset-alarms

This article shows how to read the errors of a Universal Robots cobot from a PC, in C# or Python, and how to reset a protective stop or a safety fault. On a UR controller, an alarm is a message of the controller, an error of the robot program, or a stop of the safety system.

## What to read

| Information                               | Interface         | SDK                                                        |
| ----------------------------------------- | ----------------- | ---------------------------------------------------------- |
| Messages of the controller, with a code   | Primary Interface | `KeyMessageReceived`: `RobotMessageCode`, `RobotMessageArgument`, `RobotMessageTitle`, `KeyTextMessage` |
| Errors of the URScript program            | Primary Interface | `RuntimeExceptionMessageReceived`: line, column, text      |
| Popups of the teach pendant               | Primary Interface | `PopupMessageReceived`: title, text, `Error`, `Warning`    |
| Protective stop, emergency stop           | Primary Interface | `RobotModeData.ProtectiveStopped`, `EmergencyStopped`      |
| State of the safety system                | Dashboard Server  | `GetSafetyStatus()`: `Normal`, `ProtectiveStop`, `Fault`... |
| Text messages of the program (`textmsg`)  | Primary Interface | `TextMessageReceived`                                      |

The code of a message, for example C153A1, is `RobotMessageCode` (153) and `RobotMessageArgument` (1). The meaning of each code is in the documentation of Universal Robots for your robot.

## How to reset

| State                        | Reset                                                                   |
| ---------------------------- | ----------------------------------------------------------------------- |
| `ProtectiveStop`             | Wait 5 s, then `CloseSafetyPopup()` and `UnlockProtectiveStop()`        |
| `Fault`, `Violation`         | Remove the cause, then `CloseSafetyPopup()` and `RestartSafety()`. The arm is powered off |
| `SystemEmergencyStop`, `RobotEmergencyStop` | Release the emergency stop button, on the robot. No remote reset |
| A popup of the program       | `ClosePopup()`                                                          |

On PolyScope X, the REST API has `UnlockProtectiveStop()` and `RestartSafety()`.

## Prerequisites

- The Primary Interface and the Dashboard Server are enabled on the robot: see [Prepare the robot](connect.md#prepare_the_robot).
- To reset, the robot is in remote control.

## Example

The program prints the messages of the controller and of the program, reads the safety status, and resets a protective stop or a fault.

```python
import time
from underautomation.universal_robots.ur import UR
from underautomation.universal_robots.common.safety_status import SafetyStatus
from underautomation.universal_robots.primary_interface.key_message_event_args import KeyMessageEventArgs
from underautomation.universal_robots.primary_interface.runtime_exception_message_event_args import RuntimeExceptionMessageEventArgs
from underautomation.universal_robots.primary_interface.popup_message_event_args import PopupMessageEventArgs

robot = UR()

# Primary Interface and Dashboard Server
robot.connect("192.168.0.1")

# Messages of the controller: errors with their code (C153A1...), program events
def on_key_message(sender, e):
    m = KeyMessageEventArgs(e._instance)
    print(f"C{m.robot_message_code}A{m.robot_message_argument} {m.robot_message_title}: {m.key_text_message}")

# Errors of the running URScript program
def on_runtime_exception(sender, e):
    m = RuntimeExceptionMessageEventArgs(e._instance)
    print(f"Line {m.script_line_number}: {m.runtime_exception_text_message}")

# Popups shown on the teach pendant
def on_popup(sender, e):
    m = PopupMessageEventArgs(e._instance)
    print(f"Popup {m.popup_message_title}: {m.popup_text_message} (error: {m.error})")

robot.primary_interface.key_message_received(on_key_message)
robot.primary_interface.runtime_exception_message_received(on_runtime_exception)
robot.primary_interface.popup_message_received(on_popup)

time.sleep(0.5)

# State of the safety system
status = robot.dashboard.get_safety_status().value
print("Safety status:", status)

if status == SafetyStatus.ProtectiveStop:
    # Wait 5 s after the stop, as on the teach pendant
    time.sleep(5)
    robot.dashboard.close_safety_popup()
    robot.dashboard.unlock_protective_stop()
elif status in (SafetyStatus.Fault, SafetyStatus.Violation):
    # Restarts the safety system: the arm is powered off
    robot.dashboard.close_safety_popup()
    robot.dashboard.restart_safety()

# Close the other popups of the teach pendant
robot.dashboard.close_popup()
```

The messages are sent when they occur: start listening before the error. A message sent before the connection is not received.

## Safety

A protective stop or a fault has a cause: a collision, a limit, a wrong payload. Reset it from a PC only when the cause is known and removed, and when nobody is in the cell. The SDK does not replace the risk assessment of the cell.

## What to read next

- [Monitor the state of the robot](how-to-monitor-state.md): follow the modes and the safety status.
- [Dashboard Server](remote-commands.md): the safety commands.
