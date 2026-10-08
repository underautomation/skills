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

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;

class HowToReadResetAlarms
{
  static void Main(string[] args)
  {
    var robot = new UR();

    // Primary Interface and Dashboard Server
    robot.Connect("192.168.0.1");

    // Messages of the controller: errors with their code (C153A1...), program events
    robot.PrimaryInterface.KeyMessageReceived += (sender, e) =>
    {
      Console.WriteLine($"C{e.RobotMessageCode}A{e.RobotMessageArgument} {e.RobotMessageTitle}: {e.KeyTextMessage}");
    };

    // Errors of the running URScript program
    robot.PrimaryInterface.RuntimeExceptionMessageReceived += (sender, e) =>
    {
      Console.WriteLine($"Line {e.ScriptLineNumber}: {e.RuntimeExceptionTextMessage}");
    };

    // Popups shown on the teach pendant
    robot.PrimaryInterface.PopupMessageReceived += (sender, e) =>
    {
      Console.WriteLine($"Popup {e.PopupMessageTitle}: {e.PopupTextMessage} (error: {e.Error})");
    };

    Thread.Sleep(500);

    // State of the safety system
    SafetyStatus status = robot.Dashboard.GetSafetyStatus().Value;
    Console.WriteLine("Safety status: " + status);

    switch (status)
    {
      case SafetyStatus.ProtectiveStop:
        // Wait 5 s after the stop, as on the teach pendant
        Thread.Sleep(5000);
        robot.Dashboard.CloseSafetyPopup();
        robot.Dashboard.UnlockProtectiveStop();
        break;

      case SafetyStatus.Fault:
      case SafetyStatus.Violation:
        // Restarts the safety system: the arm is powered off
        robot.Dashboard.CloseSafetyPopup();
        robot.Dashboard.RestartSafety();
        break;
    }

    // Close the other popups of the teach pendant
    robot.Dashboard.ClosePopup();
  }
}
```

The messages are sent when they occur: start listening before the error. A message sent before the connection is not received.

## Safety

A protective stop or a fault has a cause: a collision, a limit, a wrong payload. Reset it from a PC only when the cause is known and removed, and when nobody is in the cell. The SDK does not replace the risk assessment of the cell.

## What to read next

- [Monitor the state of the robot](how-to-monitor-state.md): follow the modes and the safety status.
- [Dashboard Server](remote-commands.md): the safety commands.
