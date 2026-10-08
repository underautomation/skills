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

```csharp
using UnderAutomation.UniversalRobots;
using UnderAutomation.UniversalRobots.Common;
using UnderAutomation.UniversalRobots.PrimaryInterface;

class HowToMonitorState
{
  static void Main(string[] args)
  {
    var robot = new UR();

    // Primary Interface and Dashboard Server
    robot.Connect("192.168.0.1");

    // Robot mode package, 10 times per second: print the changes only
    string last = null;
    robot.PrimaryInterface.RobotModeDataReceived += (sender, e) =>
    {
      string state =
        $"mode={e.RobotMode} powered={e.RobotPowerOn} running={e.ProgramRunning} " +
        $"paused={e.ProgramPaused} protective stop={e.ProtectiveStopped} " +
        $"emergency stop={e.EmergencyStopped} speed={e.TargetSpeedFraction:P0}";

      if (state != last) Console.WriteLine(DateTime.Now.ToString("HH:mm:ss.fff") + " " + state);
      last = state;
    };

    // Safety status, in the masterboard package
    robot.PrimaryInterface.MasterboardDataReceived += (sender, e) =>
    {
      if (e.Safetymode != SafetyStatus.Normal) Console.WriteLine("Safety: " + e.Safetymode);
    };

    // Lost connection: the property becomes false, there is no event
    while (robot.PrimaryInterface.Connected)
    {
      // Loaded program and its state, every 2 s
      var program = robot.Dashboard.GetProgramState();
      if (program.Succeed) Console.WriteLine(program.Value.Name + ": " + program.Value.State);

      Thread.Sleep(2000);
    }

    Console.WriteLine("Connection lost");
  }
}
```

The events run in a thread of the SDK. Keep them short, and copy the values you need to your own thread.

## Connection

`PrimaryInterface.Connected` and `Rtde.Connected` become `false` when the connection is lost: no event is raised and the SDK does not reconnect. Poll them, and call `Connect` again. `InternalErrorOccured` is raised for the errors of the background threads.

## What to read next

- [Read and reset alarms](how-to-read-reset-alarms.md): the messages of the controller and the safety status.
- [Primary Interface](data-streaming.md): the content of each package.
