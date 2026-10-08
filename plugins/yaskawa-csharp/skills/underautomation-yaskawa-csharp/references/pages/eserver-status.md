# Status, alarms and servo

Read the state and the alarms with their text through the Ethernet Server, reset them, switch the servo, hold the robot, set the cycle, the mode and the pendant lock.

Web page: https://underautomation.com/yaskawa/documentation/eserver-status

This page shows how to read the state and the alarms of a Yaskawa Motoman controller through the Ethernet Server, and how to change the state: servo power, hold, cycle mode, operation mode, pendant lock and pendant message. It covers the YRC1000 and YRC1000micro controllers.

## Read the status

`GetStatusInformation()` reads the mode, the execution state, the hold and the alarm flags in one command.

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerStatus
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        HostControlStatusData status = robot.EServer.GetStatusInformation();

        Console.WriteLine($"Teach: {status.Teach}, play: {status.Play}");
        Console.WriteLine($"Remote: {status.CommandRemote}, servo: {status.ServoOn}");
        Console.WriteLine($"Running: {status.Running}, speed limit: {status.SpeedLimit}");
        Console.WriteLine($"Alarm: {status.Alarming}, error: {status.ErrorOccurring}");
        Console.WriteLine($"Hold by pendant: {status.InHoldStatusPendant}, by command: {status.InHoldStatusByCommand}");

        robot.Disconnect();
    }
}
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

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.HostControl;

public class EServerAlarms
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Active error and alarms, with their text
        HostControlAlarmStringData alarms = robot.EServer.GetAlarmWithMessages();

        if (alarms.Error != null && alarms.Error.Code != 0)
            Console.WriteLine($"Error {alarms.Error.Code}: {alarms.Error.Message}");

        foreach (HostControlAlarmEntry alarm in alarms.Alarms)
        {
            if (alarm.Code != 0) // empty entries have the code 0
                Console.WriteLine($"Alarm {alarm.Code} ({alarm.SubCode}): {alarm.Message}");
        }

        // Reset the alarms, cancel the error (remote mode)
        if (alarms.AlarmCount > 0) robot.EServer.AlarmReset();
        robot.EServer.ErrorCancel();

        robot.Disconnect();
    }
}
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

```csharp
using UnderAutomation.Yaskawa;
using UnderAutomation.Yaskawa.Common;

public class EServerServo
{
    static void Main()
    {
        var parameters = new ConnectParameters("192.168.0.1");
        parameters.EServer.Enable = true;
        var robot = new YaskawaRobot();
        robot.Connect(parameters);

        // Each command needs the remote mode
        robot.EServer.SetServo(true);   // waits up to PowerOnTimeoutMilliseconds
        robot.EServer.SetHold(true);    // stop on the path, the servo stays on
        robot.EServer.SetHold(false);

        // Cycle mode of the next job start
        robot.EServer.SetCycle(RobotCycleType.OneCycle);

        // Teach or play mode (needs the external mode switch)
        robot.EServer.SetMode(RobotMode.Play);

        // Lock the pendant, show a message to the operator (30 characters)
        robot.EServer.SetTeachPendantLockState(true);
        robot.EServer.Display("Cell driven by the PC");

        robot.EServer.SetServo(false);

        robot.Disconnect();
    }
}
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

**Methods of HostControlClientBase** ([reference](../api/UnderAutomation.Yaskawa.HostControl.Internal.md#hostcontrolclientbase-roboteserver))

- `HostControlResponse AlarmReset()`: Resets the current alarm condition. The cause of the alarm must be resolved before reset will succeed. Command remote must be enabled on the controller.
- `HostControlResponse Display(string message)`: Displays a message on the remote display of the teach pendant. Command remote must be enabled on the controller.
- `HostControlResponse ErrorCancel()`: Cancels the current error condition. Used for recoverable errors that don't require full alarm reset.
- `HostControlAlarmData GetAlarm()`: Reads the codes of the active error and alarms from the robot controller. Index 0 of the arrays is the error, indexes 1 to 4 are the alarms.
- `HostControlAlarmStringData GetAlarmWithMessages()`: Reads the active error and alarms with their text messages from the robot controller. Returns the error and up to 4 alarms, each with its code, sub-code and message.
- `HostControlStatusData GetStatusInformation()`: Reads the current operational status of the robot controller. Returns information about mode (teach/play), running state, hold status, alarms, and servo power.
- `HostControlResponse SetCycle(RobotCycleType cycle)`: Sets the execution cycle type (Step, One Cycle, or Automatic).
- `HostControlResponse SetHold(bool enable)`: Sets the hold state of the robot. When hold is ON, robot motion is paused. When OFF, motion can resume.
- `HostControlResponse SetMode(RobotMode mode)`: Sets the robot operation mode (Teach or Play).
- `HostControlResponse SetServo(bool enable)`: Enables or disables servo power. Servo must be ON for the robot to move. Uses extended timeout for power-on.
- `HostControlResponse SetTeachPendantLockState(bool locked)`: Locks or unlocks the operations from the teach pendant and from the I/O operation signals. The emergency stop of the teach pendant stays active. Command remote must be enabled on the controller.

**HostControlStatusData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolstatusdata))

- `bool Alarming { get; }`: Gets whether an alarm is currently active. Check GetAlarm() for detailed alarm information.
- `bool Automatic { get; }`: Gets whether the robot is in automatic operation mode. When true, the robot can operate automatically without pendant interaction.
- `bool CommandRemote { get; }`: Gets whether remote command mode is enabled. When true, the robot accepts commands from external sources (including this API).
- `bool Cycle { get; }`: Gets whether the robot is in cycle execution mode. When true, the robot executes one complete cycle then stops.
- `bool ErrorOccurring { get; }`: Gets whether an error condition is occurring. Errors may prevent normal operation until resolved.
- `bool InHoldStatusByCommand { get; }`: Gets whether the robot is held by a command (software hold). A hold command was issued via the API or job instruction.
- `bool InHoldStatusExternally { get; }`: Gets whether the robot is held by an external hold signal. External safety circuit has triggered a hold condition.
- `bool InHoldStatusPendant { get; }`: Gets whether the robot is held by the programming pendant. Operator has pressed hold on the pendant.
- `bool Play { get; }`: Gets whether the robot is in play mode. In play mode, the robot can execute programmed jobs.
- `int RawData1 { get; }`: Gets the first raw status word from the controller response.
- `int RawData2 { get; }`: Gets the second raw status word from the controller response.
- `bool Running { get; }`: Gets whether the robot is currently running (executing a job).
- `bool ServoOn { get; }`: Gets whether servo power is enabled. Servo must be ON for the robot to move.
- `bool SpeedLimit { get; }`: Gets whether speed limit is active.
- `bool Step { get; }`: Gets whether the robot is in step (single-step) execution mode. When true, the robot executes one instruction at a time.
- `bool Teach { get; }`: Gets whether the robot is in teach mode. In teach mode, the robot can be manually positioned and jobs can be edited.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

**HostControlAlarmStringData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolalarmstringdata))

- `int AlarmCount { get; }`: Gets the number of active alarms (entries of HostControlAlarmStringData.Alarms with a code other than 0).
- `HostControlAlarmEntry[] Alarms { get; }`: Gets the alarm entries with codes and text messages (always 4 entries, the code of an unused entry is 0).
- `HostControlAlarmEntry Error { get; }`: Gets the active error. Its code is 0 when no error is active.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

**HostControlAlarmEntry** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolalarmentry))

- `int Code { get; }`: Gets the alarm code number.
- `string Message { get; }`: Gets the alarm text message.
- `int SubCode { get; }`: Gets the alarm sub-code (data).

**HostControlAlarmData** ([reference](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolalarmdata))

- `int[] Codes { get; }`: Gets the codes (5 entries). Index 0 is the code of the active error, indexes 1 to 4 are the codes of the active alarms. A code of 0 means no error or no alarm.
- `int[] Data { get; }`: Gets the sub-codes (5 entries), at the same index as HostControlAlarmData.Codes. Index 0 is the sub-code of the error, indexes 1 to 4 are the data of the alarms.
- Inherited from [HostControlResponse](../api/UnderAutomation.Yaskawa.HostControl.md#hostcontrolresponse): `ResponseCode`, `Command`, `Success`, `ErrorMessage`

**RobotCycleType** ([reference](../api/UnderAutomation.Yaskawa.Common.md#robotcycletype))

- Automatic: Automatic mode : continuous operation.
- OneCycle: One cycle mode : execute one complete cycle then stop.
- Step: Step mode : execute one instruction at a time.

**RobotMode** ([reference](../api/UnderAutomation.Yaskawa.Common.md#robotmode))

- Play: Play mode : robot can execute programmed jobs.
- Teach: Teach mode : robot can be manually positioned and jobs can be edited.

## What to read next

- [Jobs](eserver-jobs.md): select and start a job, wait for its end.
- [Read and reset alarms](how-to-read-reset-alarms.md): a complete program.
