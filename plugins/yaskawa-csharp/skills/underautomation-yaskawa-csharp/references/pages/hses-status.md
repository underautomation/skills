# Status and servo

Read the mode and the state of a Yaskawa controller, switch the servo power, hold the robot, select the cycle mode, lock the pendant and show a message on it.

Web page: https://underautomation.com/yaskawa/documentation/hses-status

This page shows how to read the state of a Yaskawa Motoman controller with the SDK, and how to change it: servo power, hold, cycle mode, pendant lock and pendant message. It covers every controller with the High Speed Ethernet Server.

## Read the status

`GetStatusInformation()` reads the mode, the execution state, the hold and the alarm flags in one request.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class StatusRead
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        RobotStatusData status = robot.HighSpeedEServer.GetStatusInformation();

        // Mode of the controller
        Console.WriteLine($"Teach: {status.Teach}, play: {status.Play}, remote: {status.CommandRemote}");

        // Cycle mode: step, one cycle or automatic (continuous)
        Console.WriteLine($"Step: {status.Step}, cycle: {status.Cycle}, automatic: {status.Automatic}");

        // Execution
        Console.WriteLine($"Running: {status.Running}, servo on: {status.ServoOn}");

        // Hold, from the pendant, from an external signal or from a command
        Console.WriteLine($"Hold: {status.InHoldStatusPendant} {status.InHoldStatusExternally} {status.InHoldStatusByCommand}");

        // Alarm and error
        Console.WriteLine($"Alarm: {status.Alarming}, error: {status.ErrorOccurring}");

        robot.Disconnect();
    }
}
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

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class StatusServo
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Switch the servo power on. The SDK waits up to PowerOnTimeoutMilliseconds (8 s)
        robot.HighSpeedEServer.SetServo(true);

        // Hold the robot, then release the hold
        robot.HighSpeedEServer.SetHold(true);
        robot.HighSpeedEServer.SetHold(false);

        // Switch the servo power off
        robot.HighSpeedEServer.SetServo(false);

        robot.Disconnect();
    }
}
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

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class StatusPendantLock
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Lock the programming pendant, so that nobody changes the mode or starts a job from it
        robot.HighSpeedEServer.SetTeachPendantLockState(true);

        // Unlock it
        robot.HighSpeedEServer.SetTeachPendantLockState(false);

        robot.Disconnect();
    }
}
```

## Cycle mode

`SetCycle(cycle)` selects how a job runs when it is started: step by step, one cycle, or in a loop.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class StatusCycleMode
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Execute the job step by step
        robot.HighSpeedEServer.SetCycle(RobotCycleType.Step);

        // Execute the job once
        robot.HighSpeedEServer.SetCycle(RobotCycleType.OneCycle);

        // Execute the job in a loop
        robot.HighSpeedEServer.SetCycle(RobotCycleType.Automatic);

        robot.Disconnect();
    }
}
```

| `RobotCycleType` | The job runs                |
| ---------------- | --------------------------- |
| `Step`           | One line at each start      |
| `OneCycle`       | Once, then stops            |
| `Automatic`      | In a loop                   |

`SwitchingCommand(SwitchingCommands)` of the previous versions does the same and is marked obsolete.

## Message on the pendant

`Display(message)` shows a message to the operator on the programming pendant. The message has 24 characters at most: a longer one is cut.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HighSpeedEServer;

public class StatusDisplay
{
    static void Main()
    {
        var robot = new YaskawaRobot();
        robot.Connect("192.168.0.1");

        // Show a message on the programming pendant, 24 characters at most
        robot.HighSpeedEServer.Display("Part 42 done");

        robot.Disconnect();
    }
}
```

## Try it in the demo application

Everything on this page can be tried without writing code, in the [demo application](demo-app.md).

## Reference

**Methods of HighSpeedEServerClientBase** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.Internal.md#highspeedeserverclientbase-robothighspeedeserver))

- `RobotDataHeader Display(string message)`: Displays a popup message on the robot programming pendant. Message will appear as a notification to the operator.
- `RobotStatusData GetStatusInformation()`: Reads the current operational status of the robot controller. Returns information about mode (teach/play), running state, hold status, alarms, and servo power.
- `RobotDataHeader SetCycle(RobotCycleType cycle)`: Sets the execution cycle type.
- `RobotDataHeader SetHold(bool enable)`: Sets the hold state of the robot.
- `RobotDataHeader SetServo(bool enable)`: Enables or disables servo power.
- `RobotDataHeader SetTeachPendantLockState(bool locked)`: Locks or unlocks the teach pendant.

**RobotStatusData** ([reference](../api/UnderAutomation.Yaskawa.HighSpeedEServer.md#robotstatusdata))

- `bool Alarming { get; }`: Gets whether an alarm is currently active. Check GetAlarm() for detailed alarm information.
- `bool Automatic { get; }`: Gets whether the robot is in automatic operation mode. When true, the robot can operate automatically without pendant interaction.
- `bool CommandRemote { get; }`: Gets whether remote command mode is enabled. When true, the robot accepts commands from external sources (including this API).
- `bool Cycle { get; }`: Gets whether the robot is in cycle execution mode. When true, the robot executes one complete cycle then stops.
- `bool ErrorOccurring { get; }`: Gets whether an error condition is occurring. Errors may prevent normal operation until resolved.
- `bool InGuardSafeOperation { get; }`: Gets whether the robot is in guard safe operation mode. Indicates collaborative/safety-rated operation mode is active.
- `bool InHoldStatusByCommand { get; }`: Gets whether the robot is held by a command (software hold). A hold command was issued via the API or job instruction.
- `bool InHoldStatusExternally { get; }`: Gets whether the robot is held by an external hold signal. External safety circuit has triggered a hold condition.
- `bool InHoldStatusPendant { get; }`: Gets whether the robot is held by the programming pendant. Operator has pressed hold on the pendant.
- `bool Play { get; }`: Gets whether the robot is in play mode. In play mode, the robot can execute programmed jobs.
- `bool Running { get; }`: Gets whether the robot is currently running (executing a job).
- `bool ServoOn { get; }`: Gets whether servo power is enabled. Servo must be ON for the robot to move.
- `bool Step { get; }`: Gets whether the robot is in step (single-step) execution mode. When true, the robot executes one instruction at a time.
- `bool Teach { get; }`: Gets whether the robot is in teach mode. In teach mode, the robot can be manually positioned and jobs can be edited.

**RobotCycleType** ([reference](../api/UnderAutomation.Yaskawa.Common.md#robotcycletype))

- Automatic: Automatic mode : continuous operation.
- OneCycle: One cycle mode : execute one complete cycle then stop.
- Step: Step mode : execute one instruction at a time.
